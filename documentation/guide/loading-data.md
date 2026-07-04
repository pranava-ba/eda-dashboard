# Loading Data

The **Load** tab is where every session starts. You bring in a file, and the app gives you a
first-glance summary of what's inside.

## Bringing in a file

You have three choices:

- **Browse files** — open an Excel (`.xlsx`, `.xls`) or CSV/TSV file from your computer.
- **Use sample data** — load the bundled 1,000-customer insurance dataset to explore or learn.
- *(Drag it in)* — on the desktop app you can also drop a file onto the window.

Each row of your file should be one *record* (a customer, a transaction, a patient…) and each
column one *property* of it. A header row of column names is expected.

![The Load tab after loading the sample dataset](../images/i1.png)

## The overview cards

Once a file loads you'll see four summary cards:

Rows
: How many records were loaded (1,000 in the sample).

Columns
: How many properties each record has.

Numeric
: How many columns the app read as numbers.

Missing cells
: How many blank/empty values exist across the whole table. **0** is ideal; a high number is a
flag to visit {doc}`missing-data`.

## The column overview table

Below the cards, a table describes every column so you can sanity-check the import at a glance:

| Field | What it tells you |
|-------|-------------------|
| **Column** | the column's name |
| **dtype** | the raw storage type (int, float, str, …) |
| **Detected type** | how the app will treat it — **numeric** or **categorical** |
| **Non-null** | how many rows have a value here |
| **Missing** | how many are blank |
| **Unique** | how many distinct values appear |
| **Sample** | an example value from the first row |

The **Unique** count is a handy clue: a numeric-looking column with only a handful of unique
values (like "missed payments" = 0–5) is usually really a category. You'll confirm all of this
on the next screen.

## Automatic schema recognition

If your file matches the known **insurance-churn** layout, the app recognises it, drops the
irrelevant `Date of Birth` column, and sets the target to **Churn** — you'll see a green
notification saying so.

For **any other dataset**, the app still loads everything; it simply asks you to choose the
target yourself on the {doc}`variable-types` screen. So you are never locked into the insurance
example.

```{admonition} Your data stays with you
:class: note
Files are read locally — in the desktop app on your machine, and in the web demo inside your own
browser tab. Nothing is uploaded to any server.
```

**Next:** confirm how each column should be treated → {doc}`variable-types`.
