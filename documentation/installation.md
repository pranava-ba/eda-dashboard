# Getting the App

There are three ways to use the EDA Dashboard. If you just want to try it, the **live demo**
needs nothing at all.

## Option 1 — Live web demo (nothing to install)

Open **<https://pranava-ba.github.io/eda-dashboard/>** in any modern browser (Chrome, Edge,
Firefox, Safari).

The entire app runs *inside the page* using [Pyodide](https://pyodide.org), which is Python
compiled to run in a browser. The first visit downloads about 20 MB of runtime (cached
afterwards, so later visits are quick). Everything happens on your computer — **your data is
never uploaded anywhere**.

```{admonition} Best for
:class: tip
Trying the app, exploring the bundled sample, or analysing a file quickly on any machine —
including one where you can't install software.
```

## Option 2 — Windows desktop app (recommended for regular use)

1. Go to the [**Releases**](https://github.com/pranava-ba/eda-dashboard/releases/latest) page.
2. Download **`EDA_Dashboard.zip`**.
3. Unzip it anywhere (e.g. your Desktop).
4. Open the unzipped folder and double-click **`EDA_Dashboard.exe`**.

No Python, no installer, no admin rights required. The app opens in its own window.

```{admonition} Keep the folder together
:class: warning
`EDA_Dashboard.exe` relies on the other files unzipped beside it. Move or create a shortcut to
the **whole folder**, not the `.exe` on its own.
```

Where your work lives: the app reads the files you open and writes only the reports you choose
to export. Nothing is installed system-wide.

## Option 3 — Run from source (for developers)

Requires **Python 3.10 or newer**.

```bash
git clone https://github.com/pranava-ba/eda-dashboard.git
cd eda-dashboard
pip install -r requirements_qt.txt
python run_qt.py
```

This launches the same desktop app from the source code.

---

However you run it, the interface and workflow are identical. Continue to {doc}`quickstart`.
