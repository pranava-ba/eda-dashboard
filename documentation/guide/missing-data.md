# Missing Data

Real-world files are rarely complete — someone skipped a field, a sensor dropped a reading, a
column doesn't apply to everyone. A **missing** (blank) value is a cell with no data. The
**Missing** tab helps you find and deal with them.

## Why it matters

Missing values quietly distort analysis: an average computed from half the rows can mislead, and
some charts drop incomplete rows without telling you. So it's worth *seeing* the gaps and
*deciding* what to do, rather than letting the app guess silently.

## The overview

The tab shows:

- **Missing cells** — the total number of blanks across the table.
- **Rows affected** — how many records have at least one blank.
- A **per-column breakdown** with a bar showing each column's missing percentage, so you can see
  whether the gaps are concentrated in one or two columns or spread everywhere.

```{admonition} The sample has none
:class: note
The bundled insurance dataset is complete, so this tab will simply say so. Load your own file
(or one with gaps) to see the tools below in action.
```

## Strategies

Pick a strategy, choose whether it applies to **all columns** or a specific one, and click
**Apply**. Your options:

Drop rows with missing
: Remove any record that has a blank in the chosen column(s). *Simple and safe, but you lose
whole rows* — fine when only a few are affected.

Drop columns with missing
: Remove entire columns that contain blanks. *Use when a column is mostly empty* and not worth
keeping.

Fill numeric with **mean**
: Replace blanks in a number column with that column's average. Keeps every row, but nudges the
data toward the middle.

Fill numeric with **median**
: Replace blanks with the middle value. *Usually safer than the mean* for skewed data (like
income), because a few extreme values won't distort the fill.

Fill with **most frequent** (mode)
: Replace blanks with the commonest value. The natural choice for **categorical** columns.

Fill numeric with **zero**
: Replace blanks with 0 — only when a blank genuinely means "none".

```{admonition} Filling in values is a judgement call
:class: warning
Replacing blanks (called *imputation*) lets you keep rows, but you're inventing data. Prefer
**median** for skewed numbers and **mode** for categories, and be cautious if a column is mostly
empty — sometimes dropping it is more honest than filling it.
```

## Resetting

Changed your mind? **Reset data** restores the dataset exactly as it was first loaded, so you
can try a different approach. Set your {doc}`variable-types` before imputing, since changing a
column's type re-reads its original values.

**Next:** save your findings → {doc}`exporting`.
