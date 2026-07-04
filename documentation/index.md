# EDA Dashboard

**EDA Dashboard** is a point-and-click tool for understanding a spreadsheet of data. You give it an
Excel or CSV file; it gives you tables, charts, and plain-language statistics that reveal what's
*in* the data and how the columns relate to one another — **no coding required**.

It ships with an example about **customer churn** (whether insurance customers leave), but it works
with **any** tabular dataset.

```{admonition} Try it right now — nothing to install
:class: tip
Open the live demo: **<https://pranava-ba.github.io/eda-dashboard/>** and click
**Use sample data**. It runs entirely inside your browser.
```

![The dashboard analysing a variable, split by the target](images/i2.png)

## Choose your starting point

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 🧠 I'm new to data analysis
Start with {doc}`concepts` — it explains datasets, variables, "churn", and p-values from scratch,
assuming zero background. Then follow the {doc}`tutorial`.
:::

:::{grid-item-card} 🚀 I just want to use it
Jump to {doc}`installation` and the five-minute {doc}`quickstart`. Reach for the **User Guide** when
you want detail on a specific screen.
:::

:::{grid-item-card} 📊 I want a worked example
The {doc}`tutorial` investigates "what makes customers leave?" end to end — with real numbers, real
findings, and how to avoid over-reading a coincidence.
:::

:::{grid-item-card} 📖 I need a reference
The {doc}`reference/dataset` documents every column of the sample; the {doc}`glossary` defines every
term; the {doc}`faq` covers common questions.
:::

::::

## What you can do with it

- **Describe one column at a time** — the shape, average, and spread of a number, or the category
  breakdown of a label. → {doc}`guide/univariate`
- **Compare two or more columns** — do income and credit score move together? do leavers differ from
  stayers? → {doc}`guide/multivariate`
- **Get real statistics, explained** — every comparison carries the right test and a sentence saying
  what it means. → {doc}`guide/statistical-tests`
- **Clean and export** — handle missing values and save any view to PDF/HTML. →
  {doc}`guide/missing-data`, {doc}`guide/exporting`

```{toctree}
:maxdepth: 2
:caption: Getting Started
:hidden:

concepts
installation
quickstart
```

```{toctree}
:maxdepth: 2
:caption: Tutorial
:hidden:

tutorial
```

```{toctree}
:maxdepth: 2
:caption: User Guide
:hidden:

guide/loading-data
guide/variable-types
guide/univariate
guide/multivariate
guide/statistical-tests
guide/missing-data
guide/exporting
```

```{toctree}
:maxdepth: 1
:caption: Reference
:hidden:

reference/dataset
glossary
faq
architecture
```
