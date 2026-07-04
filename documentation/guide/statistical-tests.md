# Statistical Tests

Charts show you a *pattern*. A **statistical test** tells you whether that pattern is likely
**real** or could just be **random luck**. The app runs the correct test for every comparison
automatically and writes the conclusion in a sentence — but understanding that sentence turns you
from someone who *reads* charts into someone who can *trust* them.

## The idea in 60 seconds

Suppose leavers *look* like they have lower balances than stayers. Could that gap appear by pure
chance, even if balance had nothing to do with churning? A test estimates exactly that risk and
reports it as a **p-value**.

```{admonition} What the p-value means
:class: important
The **p-value** is the probability of seeing a difference **at least this big** if there were
**really no difference at all**.

- **p < 0.05** → unlikely to be luck → **statistically significant** (a probable real effect).
- **p ≥ 0.05** → could easily be luck → **not significant** on this data.

The 0.05 line is a convention, not a law. The app also flags stronger evidence at p < 0.01 and
p < 0.001.
```

Each test card shows the **test name**, a few key **numbers**, and a plain-language
**interpretation** — read that sentence first, then the numbers.

## The four tests, and when each runs

The app picks the test from the *types* of the variables being compared.

### Correlation — two numeric variables

*Do these two numbers move together?*

- **Pearson r** — strength/direction of a **straight-line** link, −1 to +1.
- **Spearman ρ** — the same but on **ranks**, so it also catches "always increasing" links that
  aren't perfectly straight.
- **p-value** — is the correlation distinguishable from zero?

Rough reading of |r|: `<0.1` negligible · `0.1–0.3` weak · `0.3–0.5` moderate · `0.5–0.7` strong ·
`>0.7` very strong.

> **Example:** *Sum Assured vs Premium* → r = 0.90, p < 0.001 → a very strong, real relationship.
> *Income vs Credit Score* → r = 0.005, p = 0.88 → no relationship worth mentioning.

### Welch's t-test — one number across two groups

*Do two groups have different averages?* Runs when you compare a numeric variable across a target or
category with **exactly two groups**.

- **t** — the gap relative to the noise (bigger = more separated).
- **p-value** — is the gap significant?

> **Example:** *Bank Balance by Churn* → means ₹140,499 vs ₹139,677, p = 0.93 → the averages are
> effectively identical; balance doesn't distinguish leavers from stayers here.

### One-way ANOVA — one number across 3+ groups

The t-test's big sibling, for **three or more** groups (e.g. Credit Score across three occupations).
Reports an **F** statistic and a p-value; a significant result means *at least one* group's average
stands apart.

### Chi-square — two categorical variables

*Are two categories related, or independent?* Runs for category-vs-category, including any category
against the target.

- **χ²** — how far the observed counts are from "no relationship".
- **dof** — degrees of freedom (table-size context for χ²).
- **p-value** — is the association significant?
- **Cramér's V** — the **strength** of the association, 0 (none) to 1 (total).

> **Example:** *Missed Payments vs Churn* → p = 0.71 → not significant, despite the bars appearing
> to rise. See the pitfall below.

## Effect size: significant vs *important*

A p-value tells you an effect is probably **real**. It says nothing about whether it's **big**. With
enough rows, a trivial difference becomes "significant". So always pair the p-value with an effect
size:

- **r** (correlation) — how strong the linear link is.
- **Cramér's V** (chi-square) — how strong the category association is.
- For a target, **how far a group sits from the baseline** (here 48.6%).

*Time Since Issuance* is statistically significant against churn (p = 0.029) yet has Cramér's V ≈
0.08 — real, but far too weak to act on.

## The classic pitfall: reading trends in small groups

```{admonition} A chart pattern is a hypothesis, not a conclusion
:class: warning
In the sample, churn appears to climb with missed payments — ~45% at 1 missed up to ~59% at 4
missed. Compelling! But the test returns **p = 0.71 (not significant)**, because only **17
customers** missed 4 payments. In a group that small, a swing to 59% is easily chance. The eye
invents trends in noise, especially in thin groups — **confirm with the test every time.**
```

## Assumptions (the short version)

You don't need to check these to use the app, but they're good to know:

- **t-test / ANOVA** compare *averages*, so they're most meaningful for roughly symmetric data. For
  very skewed variables, also eyeball the boxplots — the median may tell a different story than the
  mean.
- **Chi-square** needs a reasonable number of rows per cell; very sparse tables make it unreliable
  (another reason to watch tiny categories).
- **Correlation (Pearson)** measures *straight-line* association only; a curved relationship can
  have r ≈ 0. The Spearman value helps flag monotone-but-curved cases.

## The habit to build

Read every comparison in two passes: **(1) the chart** for the shape and size of the effect, **(2)
the test card** for whether it's real. Believe a finding only when it is *both* significant *and*
sizeable. The {doc}`../tutorial` puts this into practice end to end.
