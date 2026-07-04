# Univariate Analysis

*"Univariate"* means **one variable at a time**. This tab answers the first question of any
analysis: *what does each column look like on its own?* You pick a variable and get a summary
table plus a chart tailored to its type.

Use the **KPI group** dropdown to narrow the list, then the **Variable** dropdown to choose a
column.

## Numeric variables

For a number column (income, age, credit score…) you get:

### The summary table

A list of descriptive statistics. Here's how to read each one:

| Statistic | Meaning in plain words |
|-----------|------------------------|
| **Count** | how many values there are |
| **Missing** | how many rows are blank |
| **Min / Max** | the smallest and largest values |
| **Q1, Median, Q3** | the 25th, 50th, 75th percentiles — e.g. Median = the middle value |
| **Mean** | the arithmetic average |
| **Std Dev** | the spread — how far values typically sit from the mean |
| **Skewness** | lopsidedness: `0` ≈ symmetric, positive = a long tail to the right |
| **Kurtosis** | how heavy the tails are (how often extreme values occur) |

```{admonition} Mean vs. median — a quick tell
:class: tip
If the **mean is much bigger than the median**, a few very large values are pulling the average
up (positive skew). Income usually does this: most people cluster low, a few earn a lot. That
gap is itself a useful insight.
```

### The histogram

A **histogram** shows the *distribution* — the shape of the data. The range of values is sliced
into bins along the bottom; the height of each bar is how many values fall in that bin. Tall
bars mark the most common values; a long low tail marks rare extremes.

The orange line laid over it is a **normal curve** (a "bell curve") with the same mean and
spread. It's a reference: if the bars roughly follow the curve, the data is bell-shaped; if they
lean to one side, it's skewed.

## Categorical variables

For a label column (gender, occupation, policy type…) you get a **counts table** — each category
with its count and percentage — and a chart chosen automatically by how many categories there
are:

- **2 categories** → a **pie** chart
- **3–4 categories** → a **donut** chart
- **5+ categories** → a **bar** chart (easier to compare many slices)

![A categorical variable shown as a donut chart](../images/i3.png)

The top-bar **Measure** control switches these between **Count** (how many) and **Proportion**
(what share of the total).

## Turning on "With target"

Flip the **Target** control to **With target** and the view splits by the outcome so you can
*compare groups*. This is where insights live.

### Numeric variable, with target

You choose the chart style:

Boxplot
: A compact summary of a distribution for each target group, drawn as a box. The **box** spans
the middle 50% of values (Q1 to Q3); the **line inside** is the median; the **whiskers** reach
the typical range; **dots** beyond them are outliers. Two boxes side by side let you compare, at
a glance, whether one group tends higher than the other and which is more spread out.

Overlapping histogram
: The two groups' distributions drawn on the same axes in different colours, so you can see where
they overlap and where they diverge.

![Income boxplots for stayed vs left, with a t-test](../images/i2.png)

Below the chart, a **statistical test** card tells you whether the difference between groups is
real or could be chance — see {doc}`statistical-tests`.

### Categorical variable, with target

You get a **grouped bar chart**: each category split into the target's groups, so you can see,
say, whether "Gig Work" customers churn more than "Employed" ones. It comes with a chi-square
test.

```{admonition} How to actually use this screen
:class: note
Walk through your variables one by one with **With target** on. Any time the two groups look
clearly different *and* the test says "significant", you've found a factor worth noting. The
{doc}`multivariate` tab then lets you study several such factors together.
```

**Next:** compare multiple variables at once → {doc}`multivariate`.
