"""
build_web.py — assemble the GitHub-Pages live demo into  docs/.

The demo reuses the desktop app's UI (frontend/) and the SAME pure-Python
engine (app/analytics.py, viz.py, core.py), run in the browser via Pyodide.
This script just copies the right pieces into docs/ and converts the sample
dataset to CSV (so the browser doesn't need openpyxl just to show the demo).

    python build_web.py     →  docs/  (commit this; enable Pages on /docs)
"""
import os
import shutil

import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")


def copy(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print("  +", os.path.relpath(dst, ROOT))


def main():
    # ignore_errors: on Windows a dir can be transiently locked (AV / open CWD);
    # copies below overwrite in place, so a partial clean is fine.
    if os.path.exists(DOCS):
        shutil.rmtree(DOCS, ignore_errors=True)
    os.makedirs(DOCS, exist_ok=True)
    print("Building docs/ …")

    # Web shell + bridge
    copy(os.path.join(ROOT, "web", "index.html"), os.path.join(DOCS, "index.html"))
    copy(os.path.join(ROOT, "web", "pyodide_bridge.js"), os.path.join(DOCS, "pyodide_bridge.js"))

    # Shared UI (identical to desktop)
    for f in ("app.js", "charts.js", "styles.css"):
        copy(os.path.join(ROOT, "frontend", f), os.path.join(DOCS, f))
    copy(os.path.join(ROOT, "frontend", "vendor", "plotly.min.js"),
         os.path.join(DOCS, "vendor", "plotly.min.js"))

    # Pure-Python engine (loaded into Pyodide's virtual FS as package `eda`)
    for f in ("analytics.py", "viz.py", "core.py"):
        copy(os.path.join(ROOT, "app", f), os.path.join(DOCS, "py", f))

    # Sample data → CSV (smaller, no openpyxl needed to run the demo)
    xlsx = os.path.join(ROOT, "sample_data", "Excel datafile for exercise 2.xlsx")
    out_csv = os.path.join(DOCS, "sample_data", "churn_sample.csv")
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    df = pd.read_excel(xlsx)
    if "Date of Birth" in df.columns:      # dropped by the app anyway
        df = df.drop(columns=["Date of Birth"])
    df.to_csv(out_csv, index=False)
    print("  +", os.path.relpath(out_csv, ROOT), f"({df.shape[0]}×{df.shape[1]})")

    # GitHub Pages: don't run Jekyll (it hides py/ and other files)
    open(os.path.join(DOCS, ".nojekyll"), "w").close()
    print("  + docs/.nojekyll")

    print("\nDone. Test locally with:\n"
          "  python -m http.server -d docs 8000   ->  http://localhost:8000")


if __name__ == "__main__":
    main()
