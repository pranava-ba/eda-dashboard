"""
build_qt.py — build the EDA Dashboard v3 executable with PyInstaller.

    python build_qt.py

Produces a one-folder app in  dist/EDA_Dashboard/  with EDA_Dashboard.exe inside.
Zip that folder to distribute, or compile installer_eda_qt.iss with Inno Setup.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def run(cmd, desc):
    print(f"\n{'=' * 60}\n  {desc}\n{'=' * 60}")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode != 0:
        print(f"[X] {desc} failed.")
        sys.exit(1)
    print(f"[OK] {desc}")


def main():
    print("EDA Dashboard v3 — build")

    try:
        import PyInstaller  # noqa: F401
        import PyQt6.QtWebEngineWidgets  # noqa: F401
    except ImportError:
        run(f'"{sys.executable}" -m pip install -r requirements_qt.txt',
            "Installing requirements")

    run(f'"{sys.executable}" -m PyInstaller eda_qt.spec --noconfirm --clean',
        "Building executable")

    exe = os.path.join(ROOT, "dist", "EDA_Dashboard", "EDA_Dashboard.exe")
    if os.path.exists(exe):
        print(f"\nBUILD SUCCESSFUL\n  {exe}")
        print("\nNext: zip the dist/EDA_Dashboard/ folder and attach it to a GitHub Release.")
    else:
        print("\n[X] Executable not found — check the log above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
