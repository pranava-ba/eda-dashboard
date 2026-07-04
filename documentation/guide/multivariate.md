# Multivariate Analysis

*"Multivariate"* means **several variables together**. This tab answers the second big question:
*how do columns relate to one another (and to the target)?* You choose 2–4 variables and the app
automatically produces **every relevant comparison**, each with its own chart, table, and
statistical test.

## Setting it up

1. Choose how many variables to include: **2**, **3**, or **4**.
2. For each slot, pick a **KPI group** and a **variable**. (You can't pick the same one twice.)
3. Optionally set the **Cat × Cat style** (grouped or stacked bars) and the **Numeric × target**
   chart style.
4. Click **Analyze**.

The app looks at the *types* of the variables you chose and builds the appropriate analyses.
With **With target** on, it also compares each variable against the target.

## What gets produced

### Numeric × Numeric — scatter plot + correlation

For every pair of number columns you get a **scatter plot**: one dot per row, positioned by the
two variables. Patterns to look for:

- Dots drifting **up to the right** → the two rise together (positive relationship).
- Dots drifting **down to the right** → one rises as the other falls (negative).
- A shapeless **cloud** → little or no linear relationship.

A dashed **trend line** is fitted through the dots, and the legend shows **r**, the correlation
(−1 to +1). With **With target** on, dots are coloured by group.

![Scatter of income vs credit score, with a correlation card and heatmap](../images/i4.png)

When you pick **three or more** numeric variables, you also get a **correlation heatmap** — a
grid where each cell is the correlation between two variables, coloured from blue (negative)
through white (none) to red (positive). It's the fastest way to spot which pairs move together.

### Numeric × Categorical — boxplots by group

Pair a number with a category and you get a **boxplot per category** (see
{doc}`univariate` for how to read a box), plus a table of each group's count, mean, median, and
spread. This shows whether the number differs across groups — e.g. does credit score vary by
occupation?

### Categorical × Categorical — grouped bars + cross-tab

Pair two categories and you get a **bar chart** (grouped or stacked) and a **cross-tabulation** —
a grid counting how many rows fall into each combination. Good for questions like "which policy
types are most common in each city?"

### Everything × target

With **With target** on, each chosen variable is additionally compared against the target, so a
single run can tell you how several factors each relate to churn.

## Reading the test cards

Every comparison is paired with a **statistical test** stating whether the relationship is real.
Don't skip it — a striking-looking chart can still be within the range of random noise.
{doc}`statistical-tests` explains each test and how to interpret the p-value.

```{admonition} A sensible workflow
:class: tip
Start with the two or three variables that looked promising in {doc}`univariate`, add the
target, and run. Read the charts for the *shape* of each relationship and the test cards for
whether it's *trustworthy*. Then swap in other variables to test new hunches.
```

**Next:** deal with blanks in real data → {doc}`missing-data`.
