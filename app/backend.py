"""
backend.py — thin Qt wrapper around EdaCore, exposed to JS over QWebChannel.

All real logic lives in app/core.py (EdaCore). This class only:
  • marshals dicts → JSON strings for the bridge,
  • forwards EdaCore's `last_toast` to a Qt signal,
  • handles the two OS-native bits (file-open dialog, PDF/HTML export).
"""
from __future__ import annotations

import json
import os

from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal

from . import analytics as A
from .core import EdaCore


class Backend(QObject):
    toast = pyqtSignal(str, str)          # (message, level)
    requestExport = pyqtSignal(str)       # ask main window to save PDF/HTML

    def __init__(self, window=None):
        super().__init__()
        self.window = window
        self.core = EdaCore()

    # ── helpers ────────────────────────────────────────────────────────────
    def _emit(self, result: dict) -> str:
        """Drain any toast the core queued, then JSON-encode the result."""
        if self.core.last_toast:
            self.toast.emit(*self.core.last_toast)
            self.core.last_toast = None
        return json.dumps(A.clean(result))

    # ── loading ────────────────────────────────────────────────────────────
    @pyqtSlot(result=str)
    def browse_and_load(self) -> str:
        from PyQt6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(
            self.window, "Open dataset", "",
            "Data files (*.xlsx *.xls *.csv *.tsv);;All files (*.*)")
        if not path:
            return json.dumps({"ok": False, "cancelled": True})
        return self._emit(self.core.load_file(path))

    @pyqtSlot(str, result=str)
    def load_path(self, path: str) -> str:
        if not path or not os.path.exists(path):
            return json.dumps({"ok": False, "error": "File not found"})
        return self._emit(self.core.load_file(path))

    @pyqtSlot(result=str)
    def sample_data_path(self) -> str:
        here = os.path.dirname(os.path.abspath(__file__))
        for base in (here, os.path.dirname(here)):
            cand = os.path.join(base, "sample_data",
                                "Excel datafile for exercise 2.xlsx")
            if os.path.exists(cand):
                return json.dumps({"ok": True, "path": cand})
        return json.dumps({"ok": False})

    # ── state / types ──────────────────────────────────────────────────────
    @pyqtSlot(result=str)
    def get_state(self) -> str:
        return self._emit(self.core.get_state())

    @pyqtSlot(str, result=str)
    def set_qoi(self, col: str) -> str:
        return self._emit(self.core.set_qoi(col))

    @pyqtSlot(str, result=str)
    def apply_types(self, mapping_json: str) -> str:
        return self._emit(self.core.apply_types(json.loads(mapping_json)))

    @pyqtSlot(result=str)
    def reset_data(self) -> str:
        return self._emit(self.core.reset())

    @pyqtSlot(str, result=str)
    def group_columns(self, group: str) -> str:
        return self._emit(self.core.group_columns(group))

    # ── analyses ───────────────────────────────────────────────────────────
    @pyqtSlot(str, bool, str, str, result=str)
    def univariate(self, var: str, with_qoi: bool, measure: str, plot_mode: str) -> str:
        return self._emit(self.core.univariate(var, with_qoi, measure, plot_mode))

    @pyqtSlot(str, result=str)
    def multivariate(self, args_json: str) -> str:
        return self._emit(self.core.multivariate(json.loads(args_json)))

    @pyqtSlot(result=str)
    def missing_overview(self) -> str:
        return self._emit(self.core.missing_overview())

    @pyqtSlot(str, str, result=str)
    def apply_missing(self, strategy: str, cols_json: str) -> str:
        cols = json.loads(cols_json) if cols_json else None
        return self._emit(self.core.apply_missing(strategy, cols))

    # ── export ─────────────────────────────────────────────────────────────
    @pyqtSlot(str)
    def export_report(self, fmt: str) -> None:
        self.requestExport.emit(fmt)
