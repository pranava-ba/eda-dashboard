# Building & Packaging

## Desktop executable

```bash
python build_qt.py
```

This runs PyInstaller against `eda_qt.spec` and produces a one-folder app at
`dist/EDA_Dashboard/`. The spec bundles the `frontend/` assets, the `sample_data/`, and the
QtWebEngine runtime.

To make a Windows installer, open `installer_eda_qt.iss` in
[Inno Setup](https://jrsoftware.org/isdl.php) and compile — it packages the whole
`dist/EDA_Dashboard/` folder and creates Start-menu/Desktop shortcuts.

```{tip}
While debugging a fresh build, set `console=False` → `console=True` in `eda_qt.spec` to see
Python tracebacks in a terminal window.
```

## Web demo (GitHub Pages)

The browser demo is generated into `docs/` and served by GitHub Pages.

```bash
python build_web.py                    # assembles docs/
python -m http.server -d docs 8000     # preview at http://localhost:8000
```

`build_web.py` copies the shared UI, the vendored Plotly, the pure-Python engine (into
`docs/py/`), and a CSV copy of the sample dataset, then adds a `.nojekyll` marker.

```{important}
The demo must be served over http(s). Opening `docs/index.html` directly from disk won't
work, because browsers block `fetch()` on `file://` URLs. GitHub Pages serves over https, so
it's fine there.
```

### Publishing on GitHub Pages

1. Push the repository to GitHub.
2. **Settings → Pages → Source: "Deploy from a branch"**, branch `main`, folder `/docs`, Save.
3. After ~1 minute the demo is live at `https://<user>.github.io/<repo>/`.
4. Re-run `python build_web.py` and commit `docs/` whenever the app changes.

## This documentation

These docs are built with [Sphinx](https://www.sphinx-doc.org) + [MyST](https://myst-parser.readthedocs.io)
and hosted on [Read the Docs](https://readthedocs.org). Build them locally with:

```bash
pip install -r documentation/requirements.txt
sphinx-build -b html documentation documentation/_build/html
```

Open `documentation/_build/html/index.html`. On Read the Docs, the build is driven by
`.readthedocs.yaml` at the repository root.
