"""
core.py — EdaCore: the pure, framework-free engine.

Holds the data state and all orchestration (load → types → univariate →
multivariate → missing) and returns plain Python dicts. No Qt, no browser, no
I/O beyond reading a file path.

Both front-ends drive this same object:
  • the desktop app  (app/backend.py wraps it in a QObject)
  • the web demo      (Pyodide calls it directly in the browser)

Mutating calls set `self.last_toast = (message, level)`; the caller decides how
to surface it (Qt signal, or a JS toast).
"""
from __future__ import annotations

import os

import pandas as pd

from . import analytics as A
from . import viz as V


def _df_to_table(df: pd.DataFrame, index_label: str = "") -> dict:
    """DataFrame → {columns, rows} for HTML tables (index becomes first column)."""
    df = df.reset_index()
    if index_label:
        df = df.rename(columns={df.columns[0]: index_label})
    cols = [str(c) for c in df.columns]
    rows = []
    for _, r in df.iterrows():
        row = []
        for v in r.tolist():
            if isinstance(v, float):
                row.append(None if pd.isna(v) else round(v, 3))
            elif isinstance(v, int):
                row.append(v)
            else:
                row.append(str(v))
        rows.append(row)
    return {"columns": cols, "rows": rows}


class EdaCore:
    def __init__(self):
        self.df_original: pd.DataFrame | None = None
        self.df: pd.DataFrame | None = None
        self.col_types: dict = {}
        self.qoi: str | None = None
        self.groups: dict = {}
        self.filename: str = ""
        self.last_toast: tuple[str, str] | None = None

    # ── helpers ────────────────────────────────────────────────────────────
    def _toast(self, msg: str, level: str = "info"):
        self.last_toast = (msg, level)

    def _qoi_groups(self):
        if self.qoi is None or self.df is None:
            return None
        return self.df[self.qoi].astype(str)

    def _pool(self, group: str) -> list[str]:
        if group in ("All", "", None):
            return [c for c in self.df.columns if c != self.qoi]
        return [c for c in self.groups.get(group, []) if c in self.df.columns]

    # ── loading ────────────────────────────────────────────────────────────
    def load_file(self, path: str, display_name: str | None = None) -> dict:
        try:
            raw = A.read_any(path)
        except Exception as e:
            self._toast(f"Could not read file: {e}", "error")
            return {"ok": False, "error": str(e)}

        schema = A.detect_schema(raw)
        raw = raw.drop(columns=schema["exclude"], errors="ignore")

        self.df_original = raw.copy()
        self.df = raw.copy()
        self.filename = display_name or os.path.basename(path)
        self.qoi = schema["qoi"]
        self.groups = schema["groups"]
        self.col_types = {c: A.infer_type(raw[c]) for c in raw.columns}

        self._toast(
            f"Recognised the Insurance-Churn schema — target set to “{self.qoi}”."
            if schema["matched"] else
            "Loaded. Pick your target column in the Variable Types tab.",
            "success")
        return self.get_state()

    # ── state ──────────────────────────────────────────────────────────────
    def get_state(self) -> dict:
        if self.df is None:
            return {"ok": True, "has_data": False}
        return {
            "ok": True,
            "has_data": True,
            "filename": self.filename,
            "qoi": self.qoi,
            "qoi_nunique": int(self.df[self.qoi].nunique()) if self.qoi else 0,
            "groups": self.groups,
            "overview": A.overview(self.df, self.col_types),
            "col_types": self.col_types,
            "all_columns": list(self.df.columns),
        }

    def set_qoi(self, col: str) -> dict:
        if self.df is None or col not in self.df.columns:
            return {"ok": False, "error": "Invalid column"}
        self.qoi = col
        self._toast(f"Target set to “{col}”.", "success")
        return self.get_state()

    def apply_types(self, mapping: dict) -> dict:
        changed = []
        for col, new_type in mapping.items():
            if col not in self.df.columns:
                continue
            try:
                src = self.df_original[col].reindex(self.df.index)
                if new_type == "numeric":
                    self.df[col] = pd.to_numeric(src, errors="coerce")
                else:
                    self.df[col] = src.astype(str)
                if new_type != self.col_types.get(col):
                    changed.append(col)
                self.col_types[col] = new_type
            except Exception as e:
                self._toast(f"Could not convert {col}: {e}", "error")
        self._toast(
            f"Applied types ({len(changed)} changed)." if changed
            else "Types confirmed — no changes needed.", "success")
        return self.get_state()

    def reset(self) -> dict:
        if self.df_original is None:
            return {"ok": False}
        self.df = self.df_original.copy()
        self.col_types = {c: A.infer_type(self.df[c]) for c in self.df.columns}
        self._toast("Reset to originally-loaded data.", "info")
        return self.get_state()

    def group_columns(self, group: str) -> dict:
        return {"columns": self._pool(group)}

    # ── univariate ─────────────────────────────────────────────────────────
    def univariate(self, var: str, with_qoi: bool, measure: str,
                   plot_mode: str) -> dict:
        if self.df is None or var not in self.df.columns:
            return {"ok": False}
        series = self.df[var]
        is_qoi = (var == self.qoi)
        vtype = "categorical" if is_qoi else self.col_types.get(var, "categorical")
        use_qoi = with_qoi and not is_qoi and self.qoi is not None

        resp = {"ok": True, "var": var, "vtype": vtype, "is_qoi": is_qoi,
                "stat": None, "chart": None, "summary": None, "plot_options": []}

        if vtype == "numeric":
            resp["summary"] = {"kind": "numeric", "rows": A.numeric_summary(series)}
            if use_qoi:
                resp["plot_options"] = ["Boxplot", "Overlapping Histogram"]
                mode = "hist" if plot_mode == "Overlapping Histogram" else "box"
                resp["chart"] = V.numeric_by_group(series, self._qoi_groups(), var, mode)
                resp["stat"] = A.num_cat_test(series, self._qoi_groups())
            else:
                resp["chart"] = V.numeric_hist(series, var)
        else:
            resp["summary"] = {"kind": "categorical", "rows": A.categorical_summary(series)}
            if use_qoi:
                resp["chart"] = V.categorical_by_group(series, self._qoi_groups(), var, measure)
                resp["stat"] = A.cat_cat_test(series, self._qoi_groups())
            else:
                resp["chart"] = V.categorical_bar(series, var)
                resp["chart"]["measure"] = measure
        return resp

    # ── multivariate ───────────────────────────────────────────────────────
    def multivariate(self, args: dict) -> dict:
        if self.df is None:
            return {"ok": False}
        sel = [v for v in args.get("vars", []) if v in self.df.columns]
        sel = list(dict.fromkeys(sel))
        with_qoi = bool(args.get("with_qoi", False)) and self.qoi is not None
        measure = args.get("measure", "Count")
        plot_mode = args.get("plot_mode", "Boxplot")
        stacked = bool(args.get("stacked", False))

        if len(sel) < 2:
            return {"ok": False, "error": "Select at least 2 distinct variables."}

        num = [v for v in sel if self.col_types.get(v) == "numeric"]
        cat = [v for v in sel if self.col_types.get(v) == "categorical"]
        blocks = []

        # NUM × NUM
        for i in range(len(num)):
            for j in range(i + 1, len(num)):
                x, y = num[i], num[j]
                sub = self.df[[x, y]].dropna()
                blocks.append({
                    "section": "Numeric × Numeric",
                    "title": f"{x}  ×  {y}",
                    "charts": [V.scatter(self.df, x, y,
                                         self._qoi_groups() if with_qoi else None)],
                    "table": {"title": "Summary",
                              **_df_to_table(sub.describe().T.round(2), "Variable")},
                    "stat": A.corr_test(self.df[x], self.df[y]),
                })
        heat = V.corr_heatmap(self.df, num)
        if heat:
            blocks.append({"section": "Numeric × Numeric", "title": "Correlation heatmap",
                           "charts": [heat], "table": None, "stat": None})

        # NUM × CAT
        for n in num:
            for c in cat:
                sub = self.df[[n, c]].dropna()
                grp = sub.groupby(c)[n].agg(
                    Count="count", Mean="mean", Median="median",
                    Std="std", Min="min", Max="max").round(2)
                blocks.append({
                    "section": "Numeric × Categorical",
                    "title": f"{n}  ×  {c}",
                    "charts": [V.numeric_by_group(self.df[n], self.df[c].astype(str), n, "box")],
                    "table": {"title": f"{n} by {c}", **_df_to_table(grp, c)},
                    "stat": A.num_cat_test(self.df[n], self.df[c]),
                })

        # CAT × CAT
        for i in range(len(cat)):
            for j in range(i + 1, len(cat)):
                a, b = cat[i], cat[j]
                ct = V.crosstab(self.df[a], self.df[b], a, b, measure, stacked)
                tbl = ct.pop("table")
                blocks.append({
                    "section": "Categorical × Categorical",
                    "title": f"{a}  ×  {b}",
                    "charts": [ct],
                    "table": {"title": "Cross-tabulation",
                              "columns": [a + " \\ " + b] + tbl["columns"],
                              "rows": [[idx] + row for idx, row
                                       in zip(tbl["index"], tbl["rows"])]},
                    "stat": A.cat_cat_test(self.df[a], self.df[b]),
                })

        # VARIABLES × QoI
        if with_qoi:
            q = self._qoi_groups()
            for v in sel:
                vt = self.col_types.get(v, "categorical")
                if vt == "numeric":
                    mode = "hist" if plot_mode == "Overlapping Histogram" else "box"
                    chart = V.numeric_by_group(self.df[v], q, v, mode)
                    stat = A.num_cat_test(self.df[v], q)
                    tmp = pd.DataFrame({"v": self.df[v], "q": q}).dropna()
                    grp = tmp.groupby("q")["v"].agg(
                        Count="count", Mean="mean", Median="median", Std="std").round(2)
                    table = {"title": f"{v} by {self.qoi}", **_df_to_table(grp, self.qoi)}
                else:
                    chart = V.categorical_by_group(self.df[v], q, v, measure)
                    stat = A.cat_cat_test(self.df[v], q)
                    table = None
                blocks.append({
                    "section": f"Variables × {self.qoi}",
                    "title": f"{v}  ×  {self.qoi}",
                    "charts": [chart], "table": table, "stat": stat,
                })

        return {"ok": True, "blocks": blocks,
                "plot_options": ["Boxplot", "Overlapping Histogram"]}

    # ── missing data ───────────────────────────────────────────────────────
    def missing_overview(self) -> dict:
        if self.df is None:
            return {"ok": False}
        return {"ok": True, **A.missing_overview(self.df)}

    def apply_missing(self, strategy: str, cols: list | None) -> dict:
        if self.df is None:
            return {"ok": False}
        before = int(self.df.isnull().sum().sum())
        self.df = A.apply_missing(self.df, self.col_types, strategy, cols)
        after = int(self.df.isnull().sum().sum())
        self._toast(f"Applied “{strategy}”. Missing cells: {before:,} → {after:,}.",
                    "success")
        return self.get_state()
