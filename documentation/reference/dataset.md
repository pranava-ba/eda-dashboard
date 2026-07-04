# The Sample Dataset

The app ships with an example dataset, *"Excel datafile for exercise 2.xlsx"* — **1,000
insurance customers** described by **19 columns**. This page is a full **data dictionary**: what
every column means, its type, and the values it can take. Use it as a reference while you follow
the {doc}`../tutorial` or explore on your own.

```{admonition} You don't need insurance knowledge
:class: tip
Everything here is explained in plain terms. And none of it is specific to *your* data — load
your own file and these same ideas apply, just with your columns.
```

## At a glance

- **Rows:** 1,000 (one per customer)
- **Columns:** 19 (plus a *Date of Birth* column the app drops automatically)
- **Target:** `Churn` — did the customer leave? **48.6%** of them did.
- **Missing values:** none (a clean teaching dataset)

The columns fall into four **KPI groups** — the app uses these to organise the variable pickers.

## Demography — who the customer is

| Column | Type | Values / range | Meaning |
|--------|------|----------------|---------|
| **Age at Issuance** | numeric | 18 – 66 (median 43) | Age in years when the policy was taken out |
| **Gender** | categorical | Female, Male, Trans, Do not wish to disclose | Self-reported gender |
| **Marital Status** | categorical | Married, Unmarried | — |
| **Financial Dependents** | numeric* | 0 – 5 | People financially reliant on the customer |
| **Occupation** | categorical | Employed, Gig Work, Retired | Employment type |
| **Major Life Events** | numeric* | 0 – 4 | Recent big life events (marriage, childbirth, job change, …) |
| **Location** | categorical | Urban, Rural | Where the customer lives |

## Financial — the customer's money

| Column | Type | Values / range | Meaning |
|--------|------|----------------|---------|
| **Income (INR p.a.)** | numeric | ₹1.2L – ₹26L (median ₹2.6L) | Annual income in Indian rupees |
| **Sum Assured (INR)** | numeric* | ₹5L, ₹10L, ₹20L, ₹50L, ₹1Cr | Payout the policy guarantees (5 tiers) |
| **Premium (INR p.a.)** | numeric | ₹2,594 – ₹1.99L (median ₹15,882) | Annual cost of the policy |
| **Bank Balance (INR)** | numeric | ₹10,653 – ₹15.3L (median ₹99,450) | Balance at application time |
| **Credit Score** | numeric | 433 – 900 (median 683) | Creditworthiness score |

## Policy Characteristics — the policy itself

| Column | Type | Values / range | Meaning |
|--------|------|----------------|---------|
| **Policy Type** | categorical | Term Life, Whole Life, Supplemental Health Insurance | Kind of policy |
| **Time Since Issuance** | categorical | 0–3 months, 4–6 months, 7+ months | How long they've held the policy |
| **Payment Frequency** | categorical | Monthly, Quarterly, Half Yearly, Annual | How often premiums are paid |
| **Payment Method** | categorical | Auto-Debit, Manual Payment | How premiums are paid |
| **Missed Payments** | numeric* | 0 – 5 | Count of missed premium payments |
| **Purchase Channel** | categorical | Agent Distribution, Direct, Embedded Apps | How the policy was bought |

## Target

| Column | Type | Values | Meaning |
|--------|------|--------|---------|
| **Churn** | categorical | 0 = stayed, 1 = left | Did the customer leave? The outcome to explain. |

```{admonition} About the * "numeric*" columns
:class: note
Columns marked with an asterisk (Financial Dependents, Major Life Events, Sum Assured, Missed
Payments) store **numbers** but have only a **handful of distinct values**. The app defaults them
to **categorical** because treating "3 missed payments" as a group is usually more meaningful than
averaging it. You can switch any of them to numeric on the {doc}`../guide/variable-types` screen —
see the guidance there for when each choice makes sense.
```

## What the data does (and doesn't) show

This is a **teaching dataset**, deliberately close to balanced (48.6% churn) with mostly weak
relationships — which makes it perfect for learning to tell a **real signal** from **random
noise**. When you work through the {doc}`../tutorial`, you'll find that:

- **Sum Assured and Premium move together strongly** (correlation ≈ 0.90) — bigger policies cost
  more. A textbook strong relationship.
- **Bank Balance is heavily right-skewed** — most balances are modest, a few are huge.
- **No single variable strongly predicts churn** here — and recognising *that*, rather than
  over-reading a coincidence, is one of the most valuable skills EDA teaches.
