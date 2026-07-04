# Quick Start

This is a five-minute tour that takes you from an empty screen to a real finding. We'll use the
built-in sample, so you can follow along even without your own data.

## The layout

The app is a row of **tabs** you move through left to right, plus two **global controls** in the
top bar that affect every tab:

- **Measure** — show category charts as raw **Count**s or as **Proportion**s (%).
- **Target** — **With target** splits everything by the outcome column; **Without target** looks
  at variables on their own. (See the target concept in {doc}`concepts`.)

## Step 1 — Load the sample

Open the **Load** tab and click **Use sample data**. The app reads a 1,000-row insurance
dataset, recognises it, and sets the target to **Churn** automatically. You'll see summary
cards (rows, columns, missing values) and a table describing every column.

→ Details: {doc}`guide/loading-data`

## Step 2 — Check the variable types

Open the **Types** tab. Each column is marked **numeric** or **categorical**. The guesses are
usually right; if anything looks wrong, change it and click **Apply**. This is also where you'd
pick a different target for your own data.

→ Details: {doc}`guide/variable-types`

## Step 3 — Look at one variable

Open the **Univariate** tab, choose the group **Financial** and the variable
**Income (INR p.a.)**. You'll get a statistics table and a histogram showing the shape of
incomes.

Now flip the top-bar **Target** control to **With target**. The chart becomes two boxplots —
income for customers who *stayed* vs those who *left* — and a **Welch's t-test** card appears
telling you whether the difference is statistically real.

![Univariate income, split by the target, with a t-test](images/i2.png)

→ Details: {doc}`guide/univariate`

## Step 4 — Compare several variables

Open the **Multivariate** tab, set the count to **3 vars**, and pick e.g. *Income*, *Credit
Score*, and *Gender*. Click **Analyze**. The app automatically produces every relevant
comparison — a scatter plot, a correlation heatmap, boxplots by gender — each with its own
statistical test.

![Multivariate scatter, summary and correlation](images/i4.png)

→ Details: {doc}`guide/multivariate`

## Step 5 — Read the verdict

Every chart that compares groups is paired with a **test card**: the name of the test, the key
numbers, and a sentence like *"No statistically significant association (p = 0.874)."* That
sentence is the takeaway — {doc}`guide/statistical-tests` explains exactly how to read it.

## Where to go next

- Handle blanks in real-world data → {doc}`guide/missing-data`
- Save a report to share → {doc}`guide/exporting`
- Unsure about a word? → {doc}`glossary`
