# Quick Start

The app is organised as a left-to-right workflow across five tabs. Two **global controls**
sit in the top bar and affect every tab:

- **Measure** — show **Count** or **Proportion** (%) in categorical charts.
- **Target** — analyse **With target** (split by the Quantity of Interest) or **Without target**.

## 1. Load data

Open the **Load** tab and either **Browse files** (Excel/CSV) or click **Use sample data** to
try the bundled insurance-churn dataset. You'll see row/column counts, missing-cell totals,
and a per-column overview.

If the file matches the known churn schema, the target is set to `Churn` automatically;
otherwise you'll be prompted to choose a target.

## 2. Confirm variable types

On the **Types** tab, review each column's detected dtype and its analysis role
(**numeric** or **categorical**). Override anything that's misclassified, choose the target
column, then **Apply**.

```{warning}
Forcing a text column (e.g. "7+ months") to **numeric** will blank it out — set roles
thoughtfully before analysing.
```

## 3. Univariate analysis

On the **Univariate** tab, choose a KPI group and variable:

- **Numeric** variables show a statistics table and a histogram with a fitted normal curve.
- **Categorical** variables show counts/proportions as a pie, donut, or bar chart.
- Turn on **With target** to split the view (boxplots / overlapping histograms / grouped
  bars) and get a **statistical test** with a significance callout.

## 4. Multivariate analysis

On the **Multivariate** tab, pick **2–4** variables. Every relevant pairing renders
automatically:

- **Numeric × Numeric** — scatter + regression line, plus a correlation heatmap.
- **Numeric × Categorical** — grouped boxplots + group summary.
- **Categorical × Categorical** — grouped/stacked bars + cross-tabulation.
- With **With target** on, each variable is also compared against the target.

## 5. Missing data & export

- The **Missing** tab lists missing values per column and lets you drop or impute
  (mean / median / mode / zero).
- Use **⬇ PDF** or **⬇ HTML** in the top bar to export the current view as a report.
