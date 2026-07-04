# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for EDA Dashboard v3 (PyQt6 + WebEngine).

One-FOLDER build (recommended for QtWebEngine — one-file re-extracts Chromium
on every launch and is slow/fragile). Produces dist/EDA_Dashboard/EDA_Dashboard.exe

Build:  pyinstaller eda_qt.spec --noconfirm
"""
from PyInstaller.utils.hooks import collect_all

datas = [
    ('frontend', 'frontend'),        # HTML/JS/CSS + vendored plotly & qwebchannel
    ('sample_data', 'sample_data'),  # bundled example dataset
]
binaries = []
hiddenimports = [
    'scipy.special._cdflib',
    'scipy._lib.array_api_compat.numpy.fft',
]

# Pull in PyQt6 (incl. WebEngine binaries/resources), pandas, scipy, openpyxl.
for pkg in ('PyQt6', 'scipy', 'pandas', 'numpy', 'openpyxl'):
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

a = Analysis(
    ['run_qt.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'streamlit', 'altair', 'matplotlib', 'seaborn',
              'IPython', 'notebook', 'PyQt5'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name='EDA_Dashboard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,                       # UPX + Qt DLLs often corrupts WebEngine
    console=False,                   # windowed GUI app (no terminal)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='frontend/icon.ico' if __import__('os').path.exists('frontend/icon.ico') else None,
)

coll = COLLECT(
    exe, a.binaries, a.datas,
    strip=False, upx=False, upx_exclude=[],
    name='EDA_Dashboard',
)
