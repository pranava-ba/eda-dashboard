# Variable Types

The **Types** tab is a quick but important checkpoint. Here you tell the app two things: which
column is your **target**, and whether each column is **numeric** or **categorical**. Every chart
and statistic downstream depends on these choices.

## Why the type matters

The app treats the two kinds of variable completely differently (recap from {doc}`../concepts`):

- A **numeric** column gets averages, quartiles, histograms, and boxplots.
- A **categorical** column gets counts, proportions, and pie/bar charts.

Pick the wrong kind and the output stops making sense — imagine trying to average the word
"Male", or drawing a pie chart of 1,000 distinct incomes.

## Choosing the target

At the top of the screen, set the **target column** — the outcome you most want to understand.
In the sample it's **Churn**. For your own data it might be *Converted*, *Defaulted*, *Passed*,
*Diagnosis*, or anything else. Once set, the **With target** switch throughout the app compares
everything against it.

## Reviewing each column

The table lists every column with:

- its **detected dtype** (how it's stored), and
- a dropdown to set its **analysis type** — *numeric* or *categorical*.

The app pre-fills sensible guesses. Its rule of thumb: a number column with only a few distinct
values is probably a category, not a quantity. You override anything that looks off, then click
**Apply**.

### Common corrections

:::{card} A code stored as a number
"Missed Payments" holds 0–5. Those are *levels*, not a measured amount you'd average across the
whole population — often better as **categorical**.
:::

:::{card} A quantity that happens to be tidy
"Sum Assured" might only take a few round values (₹5,00,000; ₹10,00,000…). It's still a real
number — leave it **numeric** if you want to treat it as an amount, or make it categorical to
treat those values as tiers. Your call.
:::

```{admonition} Forcing a text column to numeric will blank it out
:class: warning
If you set a genuinely textual column (like "Time Since Issuance" = *"7+ months"*) to
**numeric**, the app can't turn that text into a number, so those cells become empty. Only mark
a column numeric if its values really are numbers.
```

## Applying and resetting

- **Apply** locks in your target and types and moves you toward analysis.
- **Reset to original** restores the types the app first detected, if you want to start over.

```{admonition} Recommended order
:class: tip
Set **types first**, then handle {doc}`missing-data`, then analyse. Changing a column's type
re-reads it from the originally loaded values, so do type fixes before imputing blanks.
```

**Next:** explore one variable at a time → {doc}`univariate`.
