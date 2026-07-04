# Features

## Data loading & schema detection

- Reads Excel (`.xlsx`, `.xls`) and CSV/TSV.
- **Churn-first but flexible:** if the file matches the insurance-churn schema, the target and
  KPI groups (Demography / Financial / Policy Characteristics) are pre-filled. Otherwise the
  app falls back to a generic mode where you pick the target yourself.
- Automatic type inference (numeric vs categorical) with per-column override.

## Univariate analysis

| Variable kind | Summary | Chart |
|---------------|---------|-------|
| Numeric | count, quartiles, mean, std, skewness, kurtosis | histogram + fitted normal curve |
| Categorical | value counts + proportions | pie / donut / bar (auto by cardinality) |

With **With target** enabled, numeric variables render boxplots or overlapping histograms per
target group, and categorical variables render grouped bars.

## Multivariate analysis

Select 2–4 variables; the app enumerates and renders every relevant pairing:

- **Scatter + regression** for numeric pairs, with an `r` value and optional colour-by-target.
- **Correlation heatmap** across all selected numeric variables.
- **Grouped boxplots** for numeric × categorical pairs, with a per-group summary table.
- **Grouped/stacked bars + cross-tab** for categorical pairs.

## Statistical tests

Every comparison is accompanied by an appropriate test and a plain-language interpretation.

| Relationship | Test | Statistics reported |
|--------------|------|---------------------|
| Numeric × Numeric | Pearson & Spearman correlation | r, ρ, p-value, n |
| Numeric × Categorical (2 groups) | Welch's t-test | t, p-value |
| Numeric × Categorical (3+ groups) | One-way ANOVA | F, p-value |
| Categorical × Categorical | Chi-square of independence | χ², dof, p-value, Cramér's V |

Guards are in place for degenerate inputs (constant columns, too few groups), so the app
never crashes on an awkward variable combination.

## Missing data

- Overview of missing values per column (count and percentage).
- Strategies: drop rows, drop columns, or impute with mean / median / mode / zero.

## Export & theming

- Export the current view to **PDF** (via the print engine) or a self-contained **HTML** file.
- **Light / dark** theme toggle; charts re-theme to match.
- Responsive layout that collapses to a single column on narrow windows.
