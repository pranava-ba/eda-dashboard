# EDA Dashboard

An exploratory-data-analysis tool for tabular datasets — built around an insurance-churn
example, but works with any Excel or CSV file. It ships **two ways from one codebase**:

- **🖥️ Desktop app** — a native PyQt6 window, packaged to a standalone Windows `.exe`.
- **🌐 Live web demo** — the same UI running entirely in the browser via
  [Pyodide](https://pyodide.org) (Python compiled to WebAssembly). No server, no install.

```{admonition} Try it now
:class: tip
**Live demo:** <https://pranava-ba.github.io/eda-dashboard/>
```

![EDA Dashboard — univariate analysis](https://raw.githubusercontent.com/pranava-ba/eda-dashboard/main/images/i2.png)

## What it does

- Load Excel/CSV, confirm variable types, and pick a target (Quantity of Interest).
- **Univariate** summaries + interactive Plotly charts, optionally split by the target.
- **Multivariate** analysis of 2–4 variables — scatter/regression, correlation heatmap,
  grouped boxplots, cross-tabs.
- **Statistical tests** (t-test / ANOVA / chi-square / correlation) with plain-language callouts.
- **Missing-data** handling and **PDF/HTML** report export.

```{toctree}
:maxdepth: 2
:caption: Documentation

installation
quickstart
features
architecture
building
```
