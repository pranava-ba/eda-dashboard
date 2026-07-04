"""
main.py — PyQt6 shell for the EDA Dashboard.

A single QMainWindow hosting a QWebEngineView that loads the local HTML/JS SPA.
A QWebChannel bridges the Python `Backend` object to JavaScript. Native OS
dialogs are used for opening data files and saving PDF/HTML reports.

Run (dev):   python -m app.main
Run (entry): python run_qt.py
"""
from __future__ import annotations

import os
import sys

# Allow `python app/main.py` as well as `python -m app.main`
if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel

from app.backend import Backend

APP_NAME = "EDA Dashboard"
APP_VERSION = "3.0"


def resource_base() -> str:
    """Directory that contains the `frontend/` folder (handles PyInstaller)."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(1360, 900)
        self.setMinimumSize(1024, 680)

        icon_path = os.path.join(resource_base(), "frontend", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # WebEngine view
        self.view = QWebEngineView(self)
        self.setCentralWidget(self.view)

        settings = self.view.settings()
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)

        # Bridge
        self.backend = Backend(window=self)
        self.channel = QWebChannel()
        self.channel.registerObject("backend", self.backend)
        self.view.page().setWebChannel(self.channel)
        self.backend.requestExport.connect(self.on_export)
        # connect PDF-finished once (avoids stacking connections per export)
        self._pdf_path = ""
        self.view.page().pdfPrintingFinished.connect(
            lambda _p, ok: self._notify_saved(self._pdf_path, ok))

        # Load SPA
        index = os.path.join(resource_base(), "frontend", "index.html")
        self.view.load(QUrl.fromLocalFile(index))

    # ── report export ───────────────────────────────────────────────────────
    def on_export(self, fmt: str):
        if fmt == "pdf":
            path, _ = QFileDialog.getSaveFileName(
                self, "Save report as PDF", "eda_report.pdf", "PDF (*.pdf)")
            if not path:
                return
            self._pdf_path = path
            self.view.page().printToPdf(path)
        elif fmt == "html":
            path, _ = QFileDialog.getSaveFileName(
                self, "Save report as HTML", "eda_report.html", "HTML (*.html)")
            if not path:
                return
            self.view.page().toHtml(lambda html: self._save_html(path, html))

    def _save_html(self, path: str, html: str):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            self._notify_saved(path, True)
        except Exception as e:
            QMessageBox.warning(self, APP_NAME, f"Could not save HTML:\n{e}")

    def _notify_saved(self, path: str, ok: bool):
        if ok:
            self.backend.toast.emit(f"Report saved to {os.path.basename(path)}.",
                                    "success")
        else:
            self.backend.toast.emit("Export failed.", "error")


def main():
    QApplication.setApplicationName(APP_NAME)
    QApplication.setOrganizationName("BI Analytics")
    # Chromium flag: allow file:// scripts to work smoothly offline
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--allow-file-access-from-files")

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
