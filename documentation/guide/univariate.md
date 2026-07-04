# Univariate Analysis

*"Univariate"* means **one variable at a time**. This is where every analysis should begin: before
you compare anything, understand each column on its own. This tab gives you a summary table and a
chart matched to the variable's type, and — with the target on — a first comparison plus a
statistical test.

Pick a **KPI group** to narrow the list, then a **Variable**.

---

## Numeric variables

For a number column you get a statistics table and a histogram.

### Reading the statistics table

Every row, in plain words:

| Statistic | Meaning | Why you care |
|-----------|---------|--------------|
| **Count** | how many values | your effective sample size |
| **Missing** | how many blanks | high = handle it on {doc}`missing-data` |
| **Min / Max** | smallest / largest | spot impossible values (a negative age?) |
| **Q1 / Median / Q3** | 25th / 50th / 75th percentiles | the median is the "typical" value |
| **Mean** | arithmetic average | compare to the median (see below) |
| **Std Dev** | typical distance from the mean | small = consistent, large = varied |
| **Skewness** | lopsidedness | 0 ≈ symmetric; + = long right tail |
| **Kurtosis** | tail heaviness | high = frequent extreme values |

### Worked example: a skewed variable

Load the sample and open **Financial → Bank Balance**:

- Median **₹99,450**, but Mean **₹140,099** — the mean is **41% higher** than the median.
- Skewness **3.85**, Max **₹1.53 million**.

The histogram shows a tall stack of modest balances on the left and a long thin tail stretching
right. That gap between mean and median is the signature of **right skew**: a few very rich
customers pull the average up, even though a *typical* customer has far less.

```{admonition} Mean vs median — the 10-second diagnostic
:class: tip
**Mean ≫ median** → right-skewed (long tail of large values: income, balances, prices).
**Mean ≈ median** → roughly symmetric (e.g. Credit Score here, mean ≈ median ≈ 683).
**Mean ≪ median** → left-skewed (long tail of small values).
For skewed data, the **median** is the more honest "typical value".
```

### The histogram and the normal curve

The **histogram** slices the value range into bins along the x-axis; each bar's height is how many
values land in that bin. Tall bars = common values; a long low tail = rare extremes.

The orange **normal curve** overlaid on top is a bell curve with the *same* mean and spread. It's a
yardstick: if the bars hug the curve, the data is bell-shaped; if they bunch to one side of it, the
data is skewed. It is **not** a claim that your data *is* normal — just a reference shape.

---

## Categorical variables

For a label column you get a counts table (each category with its count and %) and a chart chosen
automatically by how many categories there are:

| Categories | Chart | Why |
|------------|-------|-----|
| 2 | **pie** | two slices are easy to compare |
| 3–4 | **donut** | still readable as parts of a whole |
| 5+ | **bar** | bars compare many groups better than a crowded pie |

![A categorical variable as a donut chart](../images/i3.png)

The top-bar **Measure** control flips these between **Count** (how many) and **Proportion** (what
share). Use **Proportion** when the total is less interesting than the mix.

```{admonition} Watch for tiny categories
:class: note
A category with very few rows (e.g. *Gender = Trans* or *Do not wish to disclose*, a handful of
customers each) will produce unstable percentages and unreliable comparisons later. Note which
categories are thin — it explains a lot of "weird" results downstream.
```

---

## Turning on "With target"

Flip the **Target** control to **With target** and each view splits by the outcome so you can
*compare groups*. This is where you start hunting for drivers.

### Numeric variable, split by target

Choose a chart style:

**Boxplot** — a compact five-number summary per group. The **box** is the middle 50% (Q1–Q3), the
**line** inside is the median, the **whiskers** reach the normal range, and **dots** beyond them
are outliers. Two boxes side by side answer at a glance: *is one group generally higher? more
spread out?* If the boxes overlap heavily and their medians line up, the groups are similar.

**Overlapping histogram** — both groups' full distributions on shared axes, so you can see exactly
where they coincide and where they part.

![Income boxplots for stayed vs left, with a t-test](../images/i2.png)

Below the chart, a **test card** (here a Welch's t-test) tells you whether the visible difference
is real or chance — always read it. See {doc}`statistical-tests`.

### Categorical variable, split by target

You get a **grouped bar chart** — each category broken into the target's groups — plus a chi-square
test. The question it answers: *does the churn rate differ across these categories?* With a 48.6%
baseline, look for any category sitting well above or below that line **and** a significant test.

---

## How to actually use this tab

1. Skim **every** variable once to learn its shape and spot data-quality issues.
2. Turn on **With target** and look for groups that separate.
3. Trust the **test card**, not just your eyes — small groups create fake-looking trends.
4. Note the promising variables, then study them together on {doc}`multivariate`.

A full walkthrough of this in action is in the {doc}`../tutorial`.
