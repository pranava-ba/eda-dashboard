# Core Concepts (start here)

This page assumes **no background** in statistics or data science. By the end you'll understand
every term the app uses. Feel free to skim and come back to it.

## What is a dataset?

A **dataset** is just a table — like a spreadsheet. It has:

- **Rows** — one per *thing* you measured. In our example, each row is one insurance customer.
- **Columns** — one per *property* of that thing (age, income, whether they left, …).

| | Age | Gender | Income | Churn |
|--|-----|--------|--------|-------|
| **Customer 1** | 56 | Female | 251,706 | 1 (left) |
| **Customer 2** | 46 | Female | 253,567 | 1 (left) |
| **Customer 3** | 32 | Male | 278,335 | 0 (stayed) |

The sample file has **1,000 rows** (customers) and **19 columns** (properties).

```{admonition} Definition — variable
:class: note
A **variable** is simply a column. "Age" is a variable, "Gender" is a variable. Each row has one
value for each variable. (It's called a *variable* because its value *varies* from row to row.)
```

## Two kinds of variable

The single most important distinction in this app:

:::{card} 🔢 Numeric variables
Values are **numbers you can do maths on** — average them, rank them, measure spread.
*Examples:* age (56, 46, 32…), income, credit score, bank balance.
:::

:::{card} 🏷️ Categorical variables
Values are **labels or groups**, not quantities. Averaging them makes no sense.
*Examples:* gender (Male/Female), city, policy type, or churn (stayed/left).
:::

Why it matters: you summarise and chart the two kinds completely differently. You take the
*average* of a numeric variable, but you *count* the categories of a categorical one. The app
asks you to confirm each column's kind on the **Variable Types** screen
(see {doc}`guide/variable-types`).

```{admonition} Watch out — numbers that are really categories
:class: warning
Some columns *look* numeric but are really labels. A column that stores churn as `0` and `1` is
**categorical** — the `1` doesn't mean "one more" of anything; it's a stand-in for "left".
Likewise a "number of missed payments" of 0–5 is a small set of groups. The app makes sensible
guesses, but you can override them.
```

## What is "churn"? (the example dataset)

**Churn** is a business word for **customers leaving**. If you run a subscription or insurance
business, a customer who cancels or doesn't renew has "churned". Companies care about churn
because keeping an existing customer is far cheaper than finding a new one.

In our sample dataset the **Churn** column is:

- `0` → the customer **stayed**
- `1` → the customer **left** (churned)

The whole point of analysing this data is to ask: *what's different about the people who left?*
Do they have lower balances? More missed payments? A particular policy type? That's exactly the
kind of question this app is built to explore. **You don't need to care about insurance** — swap
in your own data and "churn" becomes whatever outcome you're studying.

## The "target" (Quantity of Interest)

Most analyses have one column you care about most — the **outcome** you're trying to understand
or predict. This app calls it the **target** or **Quantity of Interest (QoI)**. In the sample,
the target is **Churn**.

Marking a target unlocks the app's most useful feature: **"With target" mode**, which splits
every chart and statistic by the target so you can compare the two groups side by side — e.g.
the income distribution of *stayers* vs *leavers*, drawn on the same axes.

```{admonition} Definition — target / QoI
:class: note
The **target** is the column representing the outcome you want to explain. Turn on **With target**
anywhere in the app to compare the rest of the data across the target's groups.
```

## What is "EDA"?

**EDA** stands for **Exploratory Data Analysis** — the first thing analysts do with a new
dataset. Before building any prediction model, you *explore*: look at each column, check for
errors and gaps, and hunt for relationships. It's detective work, and it's what this whole app
is for. Three questions drive it:

1. **What does each column look like on its own?** → {doc}`guide/univariate`
2. **How do columns relate to each other (and to the target)?** → {doc}`guide/multivariate`
3. **Are the patterns I see real, or just chance?** → {doc}`guide/statistical-tests`

## A few statistical ideas, in plain words

You'll meet these throughout the app. Here's the intuition; the guide pages show them in action.

Distribution
: The **shape** of a numeric column — where values pile up and how spread out they are. "Most
customers are 30–55, with a long tail of older ones" describes a distribution. A **histogram**
draws it (see {doc}`guide/univariate`).

Average (mean) & median
: Two ways to say "a typical value". The **mean** is the arithmetic average; the **median** is
the middle value when sorted. The median is sturdier when a few extreme values would otherwise
drag the mean around.

Spread (standard deviation)
: How much values differ from the typical one. Small spread = everyone's similar; large spread =
very mixed.

Correlation
: Whether two numeric columns **move together**. If higher income tends to come with a higher
credit score, they're *positively correlated*. Measured from **−1** (perfect opposite) through
**0** (no link) to **+1** (perfect together). See {doc}`guide/multivariate`.

Statistical significance & the p-value
: When you spot a difference between groups, you must ask: *could this just be luck?* A
**statistical test** answers that with a **p-value** — the probability of seeing a difference
this big **if there were really no difference at all**. A **small p-value (below 0.05)** means
"luck alone is an unlikely explanation", so we call the result **statistically significant**.
The app runs the right test for you and writes the conclusion in a sentence — see
{doc}`guide/statistical-tests`.

```{admonition} The one rule to remember about p-values
:class: important
A small p-value says a pattern is probably **real** (not random noise). It does **not** say the
pattern is **large** or **important** — a tiny, useless difference can be "significant" if you
have enough data. Always look at the chart *and* the p-value together.
```

Ready? Head to {doc}`installation` to get the app, or jump straight to {doc}`quickstart`.
