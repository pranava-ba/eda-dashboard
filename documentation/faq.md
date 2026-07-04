# FAQ & Troubleshooting

## Using your own data

**What files can I load?**
: Excel (`.xlsx`, `.xls`) and CSV/TSV. Each row should be one record and the first row should be
  column headers.

**Does my data get uploaded anywhere?**
: No. The desktop app reads files on your machine; the web demo reads them inside your own browser
  tab. Nothing is sent to a server.

**My dataset isn't about insurance. Will it still work?**
: Yes. The insurance schema is just a convenient default. Load any table, then pick your **target**
  and set **types** on the {doc}`guide/variable-types` screen. Everything else works identically.

**Do I have to choose a target?**
: For univariate charts and plain comparisons, no. But **With target** mode — the most useful
  feature — needs one. Pick the column representing the outcome you care about.

## Interpreting results

**A chart clearly shows a difference, but the test says "not significant". Who's right?**
: The test. The eye finds patterns in noise, especially in small groups. A visible difference that
  isn't significant means the data doesn't have enough evidence to rule out chance. See the
  {doc}`guide/statistical-tests` pitfall on Missed Payments.

**The test is significant but the effect looks tiny. Does it matter?**
: Significant means *real*, not *large*. Check the effect size (correlation **r**, or **Cramér's
  V**, or how far a group sits from the baseline). A real-but-tiny effect usually isn't worth
  acting on.

**What's a "good" correlation?**
: As a rule of thumb for |r|: under 0.1 negligible, 0.1–0.3 weak, 0.3–0.5 moderate, 0.5–0.7 strong,
  above 0.7 very strong. Context matters — in some fields 0.3 is a big deal.

**Why did a column turn into all blanks after I changed its type?**
: You set a text column (like *"7+ months"*) to **numeric**, and the app couldn't convert the text
  to numbers. Change it back to categorical, or use **Reset to original** on the Types tab.

## The app

**A pie chart became a bar chart (or vice versa). Why?**
: The app picks the chart by how many categories there are — pie for 2, donut for 3–4, bar for 5+.
  More categories are clearer as bars.

**Charts look empty or a group is missing.**
: Usually a very small or all-missing group after filtering/type changes. Check the variable on the
  {doc}`guide/loading-data` overview and the {doc}`guide/missing-data` tab.

**How do I save a result?**
: Use **⬇ PDF** or **⬇ HTML** in the top bar to export the current view. See
  {doc}`guide/exporting`.

**Can I change the theme?**
: Yes — the 🌙 / ☀️ button toggles light/dark. The light theme prints better.

## Installation

**The desktop download is one big folder — can I keep just the .exe?**
: No. `EDA_Dashboard.exe` needs the files unzipped beside it. Keep the whole folder together (make
  a shortcut to the `.exe` if you like). See {doc}`installation`.

**The live demo is slow to start.**
: The first visit downloads ~20 MB of Python runtime (Pyodide) and caches it. Later visits are fast.
  A modern browser and a working internet connection are needed for that first load.

**Still stuck?**
: Open an issue on the project's GitHub repository with your file's column layout (not the data
  itself) and what you expected to see.
