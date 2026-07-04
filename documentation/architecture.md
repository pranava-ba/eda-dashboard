# Architecture

The guiding idea: **one engine, two front-ends.** All the real work lives in a small,
framework-free Python core, and both the desktop app and the browser demo drive that same
core through a pluggable bridge.

## Layout

```text
app/
  analytics.py   pure pandas/scipy: schema detection, summaries, stat tests, missing-data
  viz.py         chart-data builders (Plotly payloads — data only, no styling)
  core.py        EdaCore: holds state, orchestrates load → types → analyses → missing
  backend.py     thin Qt wrapper (QObject over QWebChannel)  — desktop only
  main.py        PyQt6 window + QWebEngineView + native dialogs + PDF/HTML export
frontend/
  index.html, styles.css, app.js, charts.js   the UI (shared by both builds)
  vendor/        plotly.min.js, qwebchannel.js
web/
  index.html, pyodide_bridge.js   the browser build's shell + Pyodide bridge
docs/            generated live demo (GitHub Pages serves this) — via build_web.py
documentation/   these docs (Sphinx / Read the Docs)
```

## The shared engine

`app/core.py` exposes an `EdaCore` class whose methods take plain arguments and return plain
dicts — no Qt, no browser, no globals. It delegates number-crunching to `analytics.py`
(statistics) and `viz.py` (chart payloads). Because it's dependency-light, the exact same file
runs unchanged on the desktop **and** inside the browser.

## The pluggable bridge

`frontend/app.js` talks to a `backend` object with a uniform contract:

```js
backend.someMethod(...args, resultJson => { /* resultJson is a JSON string */ });
backend.toast.connect((message, level) => { /* notifications */ });
```

How that `backend` is provided differs per build:

- **Desktop** — `app/backend.py` is a `QObject` registered on a `QWebChannel`. Qt injects the
  transport, and slots marshal `EdaCore` results to JSON. Native OS dialogs handle file-open
  and PDF/HTML save.
- **Web** — `web/pyodide_bridge.js` loads Pyodide, writes `analytics.py`/`viz.py`/`core.py`
  into Pyodide's virtual filesystem, and exposes a JS shim with the same method shape. Calls
  are dispatched to a Python function that runs `EdaCore` in WebAssembly.

`app.js` picks whichever bridge is present (`window.__edaConnect` for the web build, otherwise
the Qt `QWebChannel`), so the UI code is identical across both.

## Data flow (one request)

1. UI event in `app.js` → `backend.univariate('Age', true, 'Count', 'Boxplot', cb)`.
2. Bridge routes to `EdaCore.univariate(...)`.
3. `EdaCore` calls `analytics` (summary + test) and `viz` (chart payload), returns a dict.
4. Bridge serialises to JSON → `cb(json)`.
5. `charts.js` renders the chart payload with themed Plotly; `app.js` renders tables + the
   stat-test callout.
