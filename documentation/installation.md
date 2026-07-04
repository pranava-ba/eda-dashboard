# Installation

There are three ways to use the EDA Dashboard, depending on whether you want zero-install,
a packaged desktop app, or to run from source.

## Live web demo (no install)

Open **<https://pranava-ba.github.io/eda-dashboard/>** in any modern browser.

The entire app runs client-side via [Pyodide](https://pyodide.org) — Python, pandas and
scipy are compiled to WebAssembly and executed in the page. The first visit downloads
~20 MB of runtime and packages (cached by the browser afterwards); nothing is uploaded to a
server, and your data never leaves your machine.

## Windows — standalone executable

The desktop app is packaged with [PyInstaller](https://pyinstaller.org) into a one-folder
build (no Python required on the target machine).

```bash
pip install -r requirements_qt.txt
python build_qt.py
```

This produces `dist/EDA_Dashboard/EDA_Dashboard.exe`. Distribute the whole
`dist/EDA_Dashboard/` folder, or build an installer by compiling `installer_eda_qt.iss` with
[Inno Setup](https://jrsoftware.org/isdl.php).

```{note}
The build is **one-folder**, not one-file, on purpose: a one-file bundle re-extracts the
embedded Chromium (QtWebEngine) on every launch, which is slow and fragile. The folder build
starts instantly.
```

## Run from source

Requires **Python 3.10+**.

```bash
git clone https://github.com/pranava-ba/eda-dashboard.git
cd eda-dashboard
pip install -r requirements_qt.txt
python run_qt.py
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `PyQt6`, `PyQt6-WebEngine` | native window + embedded web UI |
| `pandas`, `numpy` | data handling |
| `scipy` | statistical tests |
| `openpyxl` | Excel reading |
| `pyinstaller` | building the `.exe` (optional) |
