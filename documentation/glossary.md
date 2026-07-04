# Glossary

Every term the app and these docs use, in one place.

**ANOVA (one-way)**
: A {doc}`statistical test <guide/statistical-tests>` for whether a numeric variable's average
differs across **three or more** groups.

**Categorical variable**
: A column of **labels or groups** (gender, city, policy type) rather than measured numbers. See
{doc}`concepts`.

**Chi-square test**
: A {doc}`test <guide/statistical-tests>` of whether two categorical variables are **related or
independent**.

**Churn**
: Customers **leaving** a business (cancelling, not renewing). In the sample, `1` = left, `0` =
stayed. See {doc}`concepts`.

**Correlation (r, ρ)**
: How strongly two numeric variables **move together**, from −1 to +1. See
{doc}`guide/multivariate`.

**Cramér's V**
: The **strength** of a relationship between two categories, 0 (none) to 1 (total) — companion to
the chi-square p-value.

**Distribution**
: The **shape** of a numeric variable — where values cluster and how spread out they are. Drawn
as a histogram.

**EDA (Exploratory Data Analysis)**
: The practice of exploring a dataset — describing columns, checking quality, finding
relationships — before modelling. It's what this whole app is for.

**Histogram**
: A bar chart of a numeric variable's distribution: values are binned along the bottom; bar
height is how many fall in each bin.

**Imputation**
: **Filling in** missing values (e.g. with the median or mode) instead of dropping them. See
{doc}`guide/missing-data`.

**Mean / Median**
: Two "typical values". The **mean** is the average; the **median** is the middle value when
sorted (sturdier against extremes).

**Missing value**
: A **blank** cell — no data recorded. See {doc}`guide/missing-data`.

**Numeric variable**
: A column of **numbers you can do maths on** (age, income). See {doc}`concepts`.

**p-value**
: The probability a pattern this strong could appear **by chance alone**. Below 0.05 →
statistically significant. See {doc}`guide/statistical-tests`.

**Proportion**
: A share of the total, shown as a percentage — the alternative to a raw **count** in category
charts.

**Quantity of Interest (QoI)**
: Another name for the **target**.

**Skewness**
: How **lopsided** a distribution is. Positive skew = a long tail of large values (e.g. income).

**Standard deviation (Std Dev)**
: A measure of **spread** — how far values typically sit from the mean.

**Statistically significant**
: A result unlikely to be due to chance (p < 0.05). Says the effect is probably **real** — *not*
that it's large or important. See {doc}`guide/statistical-tests`.

**Target**
: The **outcome column** you want to understand (Churn in the sample). Turning on **With target**
compares everything against it. See {doc}`concepts`.

**Boxplot**
: A compact picture of a distribution — a box for the middle 50%, a line for the median, whiskers
for the typical range, dots for outliers. See {doc}`guide/univariate`.

**Variable**
: A **column** of the dataset. See {doc}`concepts`.
