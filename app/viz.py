"""
viz.py — build chart *data payloads* (not images).

Each function returns a plain dict describing what to plot. The front-end
(charts.js) turns these into themed Plotly traces, so all styling/interactivity
lives in JS and all the number-crunching lives here in Python.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def _vals(series: pd.Series) -> list:
    return [None if (isinstance(v, float) and np.isnan(v)) else v
            for v in series.tolist()]


# ── Univariate ────────────────────────────────────────────────────────────────
def numeric_hist(series: pd.Series, varname: str) -> dict:
    """Histogram + fitted normal curve."""
    s = series.dropna()
    mu, sigma = float(s.mean()), float(s.std())
    if sigma and len(s) > 1:
        x = np.linspace(s.min(), s.max(), 200)
        y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
        curve = {"x": x.tolist(), "y": y.tolist()}
    else:
        curve = None
    return {"kind": "hist_norm", "values": _vals(s), "curve": curve,
            "mu": mu, "sigma": sigma, "xlabel": varname}


def numeric_by_group(series: pd.Series, group: pd.Series, varname: str,
                     mode: str = "box") -> dict:
    """Box (mode='box') or overlapping histogram (mode='hist') per group."""
    sub = pd.DataFrame({"v": series, "g": group}).dropna()
    groups = []
    for name, chunk in sub.groupby("g"):
        groups.append({"name": str(name), "values": _vals(chunk["v"])})
    return {"kind": "box_by_group" if mode == "box" else "overlap_hist",
            "groups": groups, "label": varname}


def categorical_bar(series: pd.Series, varname: str) -> dict:
    """Category counts + proportions. Front-end decides bar/pie/donut by count."""
    vc = series.dropna().value_counts()
    total = int(vc.sum())
    return {
        "kind": "cat_bar",
        "categories": [str(c) for c in vc.index],
        "counts": [int(v) for v in vc.values],
        "pcts": [round(100 * int(v) / total, 2) if total else 0 for v in vc.values],
        "label": varname,
        "n_cats": int(vc.shape[0]),
    }


def categorical_by_group(series: pd.Series, group: pd.Series, varname: str,
                         measure: str = "Count") -> dict:
    """Grouped bars: category × group (e.g. by Churn)."""
    sub = pd.DataFrame({"v": series, "g": group}).dropna()
    ct = sub.groupby(["v", "g"]).size().unstack(fill_value=0)
    if measure == "Proportion":
        ct = (ct.div(ct.sum(axis=1), axis=0) * 100).round(2)
    series_list = [{"name": str(col), "values": [float(x) for x in ct[col].values]}
                   for col in ct.columns]
    return {
        "kind": "grouped_bar",
        "categories": [str(i) for i in ct.index],
        "series": series_list,
        "label": varname,
        "measure": measure,
    }


# ── Multivariate ──────────────────────────────────────────────────────────────
def scatter(df: pd.DataFrame, xvar: str, yvar: str,
            qoi: pd.Series | None = None) -> dict:
    """Scatter with optional colour-by-QoI + regression line."""
    from scipy import stats as _stats
    sub = df[[xvar, yvar]].dropna()
    payload = {"kind": "scatter", "xlabel": xvar, "ylabel": yvar, "groups": []}

    if qoi is not None:
        q = qoi.reindex(sub.index)
        for name, idx in q.groupby(q).groups.items():
            payload["groups"].append({
                "name": str(name),
                "x": _vals(sub.loc[idx, xvar]),
                "y": _vals(sub.loc[idx, yvar]),
            })
    else:
        payload["groups"].append({
            "name": "All", "x": _vals(sub[xvar]), "y": _vals(sub[yvar]),
        })

    # Regression line (guarded)
    if len(sub) >= 2 and sub[xvar].nunique() >= 2:
        slope, intercept, r, p, _ = _stats.linregress(sub[xvar], sub[yvar])
        xr = np.linspace(sub[xvar].min(), sub[xvar].max(), 100)
        payload["reg"] = {"x": xr.tolist(), "y": (slope * xr + intercept).tolist(),
                          "r": round(float(r), 3)}
    return payload


def corr_heatmap(df: pd.DataFrame, cols: list[str]) -> dict | None:
    if len(cols) < 2:
        return None
    corr = df[cols].dropna().corr().round(2)
    return {
        "kind": "heatmap",
        "labels": [str(c) for c in corr.columns],
        "z": [[None if pd.isna(v) else float(v) for v in row] for row in corr.values],
    }


def crosstab(a: pd.Series, b: pd.Series, alabel: str, blabel: str,
             measure: str = "Count", stacked: bool = False) -> dict:
    sub = pd.DataFrame({"a": a, "b": b}).dropna()
    ct = pd.crosstab(sub["a"], sub["b"])
    plot = ct.copy()
    if measure == "Proportion":
        plot = (plot.div(plot.sum(axis=1), axis=0) * 100).round(2)
    return {
        "kind": "grouped_bar",
        "stacked": stacked,
        "categories": [str(i) for i in plot.index],
        "series": [{"name": str(c), "values": [float(x) for x in plot[c].values]}
                   for c in plot.columns],
        "xlabel": alabel,
        "measure": measure,
        # raw crosstab table for display
        "table": {
            "index": [str(i) for i in ct.index],
            "columns": [str(c) for c in ct.columns],
            "rows": [[int(x) for x in row] for row in ct.values],
        },
    }
