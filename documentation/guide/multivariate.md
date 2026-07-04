# Multivariate Analysis

*"Multivariate"* means **several variables together**. This tab answers the second big question:
*how do columns relate to one another, and to the target?* You choose 2–4 variables and the app
automatically produces **every relevant comparison** — each with a chart, a table, and a
statistical test — so you don't have to know in advance which combinations to try.

## Setting it up

1. Choose how many variables: **2**, **3**, or **4**.
2. For each slot, pick a **KPI group** then a **variable** (you can't pick the same one twice).
3. Optionally set **Cat × Cat style** (grouped or stacked bars) and the **Numeric × target** chart.
4. Click **Analyze**.

The app inspects the *types* you chose and builds the right analyses. Turn on **With target** to
also compare each variable against the outcome.

---

## Numeric × Numeric — scatter + correlation

For each pair of numbers you get a **scatter plot**: one dot per row, placed by the two values.
Read the *shape of the cloud*:

- Dots rising **left→right** → the two increase together (**positive**).
- Dots falling **left→right** → one rises as the other falls (**negative**).
- A round, shapeless blob → **little or no** linear relationship.

A dashed **trend line** is fitted through the dots and the legend shows **r**, the correlation
coefficient (−1 to +1).

### Worked example: a strong link vs no link

In the sample, plot **Sum Assured vs Premium**: the dots form a tight upward band and the card
reports **Pearson r ≈ 0.90** — a **very strong positive** relationship. It's intuitive: a policy
that guarantees a bigger payout costs a bigger premium.

Now plot **Income vs Credit Score**: a formless cloud, **r ≈ 0.00** — these two are essentially
**unrelated**. Same chart type, opposite stories — and the number tells you which is which.

![Scatter, summary and the correlation heatmap](../images/i4.png)

### The correlation heatmap

Pick **three or more** numeric variables and you also get a **heatmap** — a grid where each cell is
the correlation between two variables, coloured **blue (negative) → white (none) → red
(positive)**. The diagonal is always 1 (a variable with itself). It's the fastest way to scan many
pairs at once: the Sum Assured × Premium cell blazes red, while most others are pale — exactly what
you'd expect.

```{admonition} Correlation ≠ causation
:class: important
A strong correlation means two things *move together*, not that one *causes* the other. Ice-cream
sales and drowning deaths correlate (both rise in summer); neither causes the other. Use
correlation to find leads, not to prove mechanisms.
```

---

## Numeric × Categorical — boxplots by group

Pair a number with a category and you get a **boxplot per category** (see {doc}`univariate` for how
to read a box) plus a table of each group's count, mean, median, and spread. This reveals whether
the number differs across groups — *does credit score vary by occupation? does premium differ by
policy type?* A one-way ANOVA (or t-test for two groups) accompanies it.

---

## Categorical × Categorical — grouped bars + cross-tab

Pair two categories and you get a **bar chart** (grouped or stacked, your choice) and a
**cross-tabulation** — a grid counting rows in each combination. Good for questions like *"which
purchase channels dominate each policy type?"* A chi-square test reports whether the two are
related.

- **Grouped** bars sit side by side — best for comparing exact heights.
- **Stacked** bars sum to the whole — best for seeing composition.

---

## Everything × target

With **With target** on, each chosen variable is *also* compared against the target, so a single
run can screen several candidate drivers of churn at once — each with its own test card. This is the
efficient way to ask "which of these five things relates to leaving?" in one click.

## Reading the results well

- Let the **charts** show you the *shape* of a relationship.
- Let the **test cards** tell you whether it's *trustworthy* (a shapely scatter of 20 points can
  still be luck).
- Check the **effect size** (r for correlations, Cramér's V for categories) to judge whether a
  *real* relationship is also *large enough to matter*.

The {doc}`../tutorial` walks through a full multivariate hunt, including why several convincing-looking
comparisons turn out to be noise.
