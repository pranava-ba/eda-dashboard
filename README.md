# 📊 EDA Dashboard

An exploratory-data-analysis tool for tabular datasets (built around an insurance
churn example, but works with any Excel/CSV). It ships **two ways from one codebase**:

- **🖥️ Desktop app** — a native PyQt6 window (packaged to a standalone Windows `.exe`).
- **🌐 Live web demo** — the same UI running entirely in the browser via
  [Pyodide](https://pyodide.org) (Python compiled to WebAssembly). No server, no install.

> **🌐 Live demo:** https://pranava-ba.github.io/eda-dashboard/
> *(goes live once GitHub Pages is enabled — Settings → Pages → `main` / `/docs`)*

## Features

- **Churn-first, flexible** — auto-detects the insurance-churn schema; or load any
  dataset and pick your own target + variable types.
- **Load** Excel (`.xlsx/.xls`) and CSV/TSV, with a dataset overview.
- **Variable Types** — confirm/override numeric vs categorical; choose the target (QoI).
- **Univariate** — summaries + interactive Plotly charts (histogram + normal curve,
  boxplots, pie/donut/bar), optionally split by the target.
- **Multivariate** — 2–4 variables, auto-rendering every relevant pairing: scatter +
  regression, correlation heatmap, grouped boxplots, cross-tab bars.
- **Statistical tests** — Pearson/Spearman, Welch's t-test / one-way ANOVA, chi-square
  (+ Cramér's V), each with a plain-language significance callout.
- **Missing data** — overview + drop/impute (mean, median, mode, zero).
- **Report export** — one-click PDF or HTML of the current view.
- **Light / dark theme**, responsive layout, toast notifications.

## How it's built

```
app/
  analytics.py   pure pandas/scipy logic (schema detect, summaries, stat tests, missing)
  viz.py         chart-data builders (Plotly payloads)
  core.py        EdaCore — the framework-free engine (holds state, orchestrates everything)
  backend.py     thin Qt wrapper (QObject over QWebChannel) — desktop only
  main.py        PyQt6 window + WebEngine + native dialogs + PDF/HTML export
frontend/
  index.html, styles.css, app.js, charts.js   the UI (shared by both builds)
  vendor/        plotly.min.js, qwebchannel.js
web/
  index.html, pyodide_bridge.js   the browser build's shell + Pyodide bridge
sample_data/     example dataset + metadata
docs/            GENERATED live demo (GitHub Pages serves this) — via build_web.py
```

**The trick:** all real logic lives in `app/core.py` + `analytics.py` + `viz.py`, which
are completely framework-free. The desktop app wraps them in a Qt `QObject`; the web demo
runs the *exact same files* inside Pyodide. `frontend/app.js` talks to a `backend` object
with a pluggable bridge — Qt's `QWebChannel` on the desktop, a Pyodide shim in the browser.

## Run the desktop app (from source)

```bash
pip install -r requirements_qt.txt
python run_qt.py
```

## Build the desktop `.exe`

```bash
python build_qt.py     # → dist/EDA_Dashboard/EDA_Dashboard.exe  (one-folder)
```

Distribute the whole `dist/EDA_Dashboard/` folder, or compile `installer_eda_qt.iss` in
[Inno Setup](https://jrsoftware.org/isdl.php) for a setup wizard.
(One-folder, not one-file: QtWebEngine re-extracts Chromium on every one-file launch.)

## Build & host the live web demo

```bash
python build_web.py                       # assembles docs/
python -m http.server -d docs 8000        # test at http://localhost:8000
```

> The demo must be served over http(s) — opening `docs/index.html` directly won't work
> (browsers block `fetch` on `file://`). GitHub Pages serves it over https, so it's fine there.

### Publish on GitHub Pages

1. Create a repo on GitHub and push this project (see below).
2. On GitHub: **Settings → Pages → Build and deployment → Source: “Deploy from a branch”**,
   Branch **`main`**, Folder **`/docs`**, then **Save**.
3. Wait ~1 minute; your demo is at `https://<username>.github.io/<repo>/`.
4. Re-run `python build_web.py` and commit `docs/` whenever you change the app.

## Requirements

- Desktop: Python 3.10+, `PyQt6`, `PyQt6-WebEngine`, `pandas`, `scipy`, `openpyxl`
  (see `requirements_qt.txt`).
- Web demo: just a browser (Pyodide + packages load from CDN on first visit, then cache).

## License

See [LICENSE.txt](LICENSE.txt).
