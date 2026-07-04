# Statistical Tests

Charts show you a *pattern*. A **statistical test** tells you whether that pattern is likely
**real** or could just be **random luck**. This app runs the correct test for every comparison
automatically and writes the conclusion in a sentence, so you don't need to compute anything —
but it helps to understand what the sentence means.

## The idea in 60 seconds

Suppose leavers *look* like they have lower balances than stayers. Could that gap appear by pure
chance, even if balance had nothing to do with churning? A test estimates exactly that risk and
reports it as a **p-value**.

```{admonition} What the p-value means
:class: important
The **p-value** is the probability of seeing a difference **at least this big** if there were
**really no difference at all**.

- **p < 0.05** → unlikely to be luck → we call it **statistically significant** (a probable real
  effect).
- **p ≥ 0.05** → could easily be luck → **not significant** on this data.

The 0.05 line is a common convention, not a law of nature. The app also flags stronger evidence
at p < 0.01 and p < 0.001.
```

Each test card shows the **test name**, a few key **numbers**, and a plain-language
**interpretation**. The interpretation sentence is the part to read first.

## The tests this app uses

Which test runs depends on the *types* of the variables being compared — the app picks for you.

### Correlation — for two numeric variables

Answers: *do these two numbers move together?* Reported values:

- **Pearson r** — strength and direction of a **straight-line** relationship, from −1 to +1.
- **Spearman ρ** — the same idea but based on **ranks**, so it also catches "always increasing"
  relationships that aren't perfectly straight.
- **p-value** — whether that correlation is distinguishable from zero.

Rough reading of |r|: under 0.1 negligible · 0.1–0.3 weak · 0.3–0.5 moderate · 0.5–0.7 strong ·
above 0.7 very strong.

> *Example:* "Pearson r 0.005 · p-value 0.8795 → Negligible positive linear relationship. No
> statistically significant association." Translation: income and credit score are essentially
> unrelated in this data.

### Welch's t-test — one number across two groups

Answers: *do two groups have different averages?* Used automatically when you compare a numeric
variable across a target (or category) that has **exactly two groups** — e.g. income for
*stayed* vs *left*.

- **t** — how large the gap is relative to the noise (bigger = more separated).
- **p-value** — whether that gap is significant.

> *Example:* "t −0.159 · p-value 0.8739 → Group means are similar. No statistically significant
> association." Translation: average income is about the same whether or not customers churned.

### One-way ANOVA — one number across three or more groups

The same question as the t-test, but for **3+ groups** (e.g. credit score across three
occupations). Reports an **F** statistic and a p-value. A significant result means *at least one*
group's average stands out from the rest.

### Chi-square test — for two categorical variables

Answers: *are two categories related, or independent?* Used for category-vs-category comparisons,
including a category vs the target.

- **χ² (chi-square)** — how far the observed counts are from what you'd expect if the two were
  unrelated.
- **dof** — degrees of freedom (depends on the table size; context for χ²).
- **p-value** — whether the association is significant.
- **Cramér's V** — the **strength** of the association, from 0 (none) to 1 (total). Because a big
  table can be "significant" yet weak, V tells you if it also *matters*.

> *Example:* a low p-value with Cramér's V = 0.08 means "the link is real but very weak."

## The most important habit

```{admonition} Significant ≠ large ≠ important
:class: warning
A small p-value says an effect is probably **real**, not that it's **big** or **useful**. With
1,000+ rows, even a trivial difference can be "significant". Always pair the verdict with the
chart and the effect size (r, or Cramér's V): *is the difference both real and large enough to
act on?*
```

**Next:** clean up blanks before trusting your numbers → {doc}`missing-data`.
