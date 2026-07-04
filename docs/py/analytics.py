"""
analytics.py — pure data/stat logic for the EDA Dashboard.

No Qt, no I/O side effects beyond reading a file. Everything returns plain,
JSON-serialisable Python structures so it can be handed straight to the
front-end over QWebChannel. Keeping this layer framework-free means it can be
unit-tested on its own and reused outside the GUI.
"""
from __future__ import annotations

import math
import numpy as np
import pandas as pd
from scipy import stats

# ──────────────────────────────────────────────────────────────────────────────
# Known "Insurance Churn" schema — used for churn-first auto-detection.
# If the loaded file matches, we pre-populate the target + KPI groups. Otherwise
# the app falls back to a generic "pick your own target/groups" mode.
# ──────────────────────────────────────────────────────────────────────────────
CHURN_QOI = "Churn"
CHURN_EXCLUDE = ["Date of Birth"]
CHURN_GROUPS = {
    "Demography": [
        "Age at Issuance", "Gender", "Marital Status",
        "Financial Dependents", "Occupation", "Major Life Events", "Location",
    ],
    "Financial": [
        "Income (INR p.a.)", "Sum Assured (INR)",
        "Premium (INR p.a.)", "Bank Balance (INR)", "Credit Score",
    ],
    "Policy Characteristics": [
        "Policy Type", "Time Since Issuance", "Payment Frequency",
        "Payment Method", "Missed Payments", "Purchase Channel",
    ],
}

# Low-cardinality numeric columns below this many distinct values default to
# "categorical" on load (the user can always override in the Types tab).
CATEGORICAL_NUNIQUE_THRESHOLD = 12


# ══════════════════════════════════════════════════════════════════════════════
# JSON sanitising — numpy/NaN are not valid JSON
# ══════════════════════════════════════════════════════════════════════════════
def clean(obj):
    """Recursively convert numpy scalars, NaN/inf, timestamps → JSON-safe."""
    if isinstance(obj, dict):
        return {str(k): clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [clean(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        f = float(obj)
        return None if (math.isnan(f) or math.isinf(f)) else f
    if isinstance(obj, float):
        return None if (math.isnan(obj) or math.isinf(obj)) else obj
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, (pd.Timestamp,)):
        return obj.isoformat()
    if obj is pd.NaT:
        return None
    return obj


# ══════════════════════════════════════════════════════════════════════════════
# Loading & schema detection
# ══════════════════════════════════════════════════════════════════════════════
def read_any(path: str) -> pd.DataFrame:
    """Read .xlsx/.xls/.csv into a DataFrame."""
    lower = path.lower()
    if lower.endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    if lower.endswith(".csv"):
        return pd.read_csv(path)
    if lower.endswith(".tsv"):
        return pd.read_csv(path, sep="\t")
    raise ValueError("Unsupported file type. Use .xlsx, .xls, .csv or .tsv")


def detect_schema(df: pd.DataFrame) -> dict:
    """
    Churn-first, but flexible.

    Returns dict with:
      matched      – bool, True if this looks like the insurance-churn dataset
      qoi          – suggested target column (or None)
      groups       – {group_name: [cols]} for the KPI grouping
      exclude      – columns to drop by default (e.g. Date of Birth)
    """
    known = {c for g in CHURN_GROUPS.values() for c in g} | {CHURN_QOI}
    overlap = known & set(df.columns)
    matched = CHURN_QOI in df.columns and len(overlap) >= max(6, len(known) // 2)

    if matched:
        groups = {
            g: [c for c in cols if c in df.columns]
            for g, cols in CHURN_GROUPS.items()
        }
        return {
            "matched": True,
            "qoi": CHURN_QOI,
            "groups": groups,
            "exclude": [c for c in CHURN_EXCLUDE if c in df.columns],
        }

    # Generic fallback: no target chosen yet, everything in one group.
    return {
        "matched": False,
        "qoi": None,
        "groups": {},
        "exclude": [],
    }


def infer_type(series: pd.Series) -> str:
    """Auto-detect 'numeric' vs 'categorical' for the initial guess."""
    if pd.api.types.is_datetime64_any_dtype(series):
        return "categorical"
    if pd.api.types.is_numeric_dtype(series):
        if series.nunique(dropna=True) > CATEGORICAL_NUNIQUE_THRESHOLD:
            return "numeric"
        return "categorical"
    return "categorical"


def python_dtype_label(series: pd.Series) -> str:
    """Human-friendly dtype string for the Types table."""
    dt = series.dtype
    if pd.api.types.is_datetime64_any_dtype(dt):
        return "datetime"
    if pd.api.types.is_bool_dtype(dt):
        return "bool"
    if pd.api.types.is_integer_dtype(dt):
        return "int"
    if pd.api.types.is_float_dtype(dt):
        return "float"
    return "str"


def overview(df: pd.DataFrame, col_types: dict) -> dict:
    """Dataset-level summary + per-column metadata for the Load tab."""
    n_missing = int(df.isnull().sum().sum())
    columns = []
    for c in df.columns:
        s = df[c]
        non_null = int(s.count())
        sample = s.dropna()
        columns.append({
            "name": c,
            "dtype": python_dtype_label(s),
            "type": col_types.get(c, infer_type(s)),
            "non_null": non_null,
            "missing": int(s.isnull().sum()),
            "unique": int(s.nunique(dropna=True)),
            "sample": "" if sample.empty else str(sample.iloc[0]),
        })
    return {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "numeric_cols": sum(1 for c in df.columns
                            if pd.api.types.is_numeric_dtype(df[c])),
        "missing": n_missing,
        "missing_cells_pct": round(100 * n_missing / max(1, df.size), 2),
        "columns": columns,
    }


# ══════════════════════════════════════════════════════════════════════════════
# Summaries
# ══════════════════════════════════════════════════════════════════════════════
def numeric_summary(series: pd.Series) -> list[dict]:
    s = series.dropna()
    if s.empty:
        return []
    rows = [
        ("Count", f"{s.count():,}"),
        ("Missing", f"{series.isnull().sum():,}"),
        ("Min", f"{s.min():,.2f}"),
        ("Q1 (25%)", f"{s.quantile(0.25):,.2f}"),
        ("Median", f"{s.median():,.2f}"),
        ("Mean", f"{s.mean():,.2f}"),
        ("Q3 (75%)", f"{s.quantile(0.75):,.2f}"),
        ("Max", f"{s.max():,.2f}"),
        ("Std Dev", f"{s.std():,.2f}"),
        ("Skewness", f"{s.skew():.2f}"),
        ("Kurtosis", f"{s.kurt():.2f}"),
    ]
    return [{"stat": k, "value": v} for k, v in rows]


def categorical_summary(series: pd.Series) -> list[dict]:
    s = series.dropna()
    vc = s.value_counts()
    total = vc.sum()
    out = []
    for cat, cnt in vc.items():
        out.append({
            "category": str(cat),
            "count": int(cnt),
            "pct": round(100 * cnt / total, 2) if total else 0.0,
        })
    return out


# ══════════════════════════════════════════════════════════════════════════════
# Statistical tests (with plain-language interpretation)
# ══════════════════════════════════════════════════════════════════════════════
def _sig_text(p):
    if p is None:
        return "Test could not be computed."
    if p < 0.001:
        return "Very strong evidence of an association (p < 0.001)."
    if p < 0.01:
        return "Strong evidence of an association (p < 0.01)."
    if p < 0.05:
        return "Statistically significant association (p < 0.05)."
    return f"No statistically significant association (p = {p:.3f})."


def corr_test(x: pd.Series, y: pd.Series) -> dict:
    """Pearson + Spearman correlation with p-values."""
    sub = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(sub) < 3 or sub["x"].nunique() < 2 or sub["y"].nunique() < 2:
        return {"name": "Correlation", "ok": False,
                "interpretation": "Not enough variation to compute correlation."}
    r, p = stats.pearsonr(sub["x"], sub["y"])
    rho, _ = stats.spearmanr(sub["x"], sub["y"])
    strength = ("negligible" if abs(r) < 0.1 else "weak" if abs(r) < 0.3
                else "moderate" if abs(r) < 0.5 else "strong" if abs(r) < 0.7
                else "very strong")
    direction = "positive" if r >= 0 else "negative"
    return {
        "name": "Pearson correlation",
        "ok": True,
        "stats": [
            {"label": "Pearson r", "value": round(r, 3)},
            {"label": "Spearman ρ", "value": round(rho, 3)},
            {"label": "p-value", "value": _fmt_p(p)},
            {"label": "n", "value": len(sub)},
        ],
        "interpretation": f"{strength.capitalize()} {direction} linear relationship. "
                          + _sig_text(p),
    }


def num_cat_test(num: pd.Series, cat: pd.Series) -> dict:
    """t-test (2 groups) or one-way ANOVA (3+ groups)."""
    sub = pd.DataFrame({"n": num, "c": cat}).dropna()
    groups = [g["n"].values for _, g in sub.groupby("c") if len(g) >= 2]
    if len(groups) < 2:
        return {"name": "Group difference", "ok": False,
                "interpretation": "Need at least two groups with data."}
    if len(groups) == 2:
        stat, p = stats.ttest_ind(groups[0], groups[1], equal_var=False)
        name = "Welch's t-test"
        stat_label = "t"
    else:
        stat, p = stats.f_oneway(*groups)
        name = "One-way ANOVA"
        stat_label = "F"
    return {
        "name": name,
        "ok": True,
        "stats": [
            {"label": stat_label, "value": round(float(stat), 3)},
            {"label": "p-value", "value": _fmt_p(p)},
            {"label": "groups", "value": len(groups)},
        ],
        "interpretation": "Group means differ. " + _sig_text(p)
                          if p is not None and p < 0.05
                          else "Group means are similar. " + _sig_text(p),
    }


def cat_cat_test(a: pd.Series, b: pd.Series) -> dict:
    """Chi-square test of independence + Cramér's V effect size."""
    sub = pd.DataFrame({"a": a, "b": b}).dropna()
    ct = pd.crosstab(sub["a"], sub["b"])
    if ct.shape[0] < 2 or ct.shape[1] < 2:
        return {"name": "Chi-square", "ok": False,
                "interpretation": "Need at least a 2×2 table."}
    chi2, p, dof, _ = stats.chi2_contingency(ct)
    n = ct.values.sum()
    min_dim = min(ct.shape) - 1
    cramers_v = math.sqrt(chi2 / (n * min_dim)) if n and min_dim else 0.0
    return {
        "name": "Chi-square test",
        "ok": True,
        "stats": [
            {"label": "χ²", "value": round(chi2, 3)},
            {"label": "dof", "value": int(dof)},
            {"label": "p-value", "value": _fmt_p(p)},
            {"label": "Cramér's V", "value": round(cramers_v, 3)},
        ],
        "interpretation": _sig_text(p),
    }


def _fmt_p(p):
    if p is None or (isinstance(p, float) and (math.isnan(p))):
        return None
    return "<0.001" if p < 0.001 else round(float(p), 4)


# ══════════════════════════════════════════════════════════════════════════════
# Missing-data handling
# ══════════════════════════════════════════════════════════════════════════════
def missing_overview(df: pd.DataFrame) -> dict:
    rows = []
    for c in df.columns:
        m = int(df[c].isnull().sum())
        if m:
            rows.append({
                "column": c,
                "missing": m,
                "pct": round(100 * m / len(df), 2),
            })
    rows.sort(key=lambda r: r["missing"], reverse=True)
    return {
        "total_missing": int(df.isnull().sum().sum()),
        "rows_with_missing": int(df.isnull().any(axis=1).sum()),
        "columns": rows,
    }


def apply_missing(df: pd.DataFrame, col_types: dict, strategy: str,
                  scope_cols: list[str] | None = None) -> pd.DataFrame:
    """
    Return a new DataFrame with the chosen missing-data strategy applied.
    strategy ∈ {drop_rows, drop_cols, mean, median, mode, zero}
    """
    out = df.copy()
    cols = scope_cols or list(out.columns)

    if strategy == "drop_rows":
        return out.dropna(subset=cols)
    if strategy == "drop_cols":
        drop = [c for c in cols if out[c].isnull().any()]
        return out.drop(columns=drop)

    for c in cols:
        if not out[c].isnull().any():
            continue
        is_num = pd.api.types.is_numeric_dtype(out[c])
        if strategy == "mean" and is_num:
            out[c] = out[c].fillna(out[c].mean())
        elif strategy == "median" and is_num:
            out[c] = out[c].fillna(out[c].median())
        elif strategy == "zero" and is_num:
            out[c] = out[c].fillna(0)
        elif strategy == "mode":
            mode = out[c].mode(dropna=True)
            if not mode.empty:
                out[c] = out[c].fillna(mode.iloc[0])
        else:  # non-numeric column under a numeric strategy → fall back to mode
            mode = out[c].mode(dropna=True)
            if not mode.empty:
                out[c] = out[c].fillna(mode.iloc[0])
    return out
