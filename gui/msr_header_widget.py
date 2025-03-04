"""This module provides a toolkit for the GUI header definition."""

from PySide6.QtWidgets import (QWidget, QHBoxLayout,
                               QLabel, QPushButton, QMenu, QMainWindow,)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QAction
from gui import MSROpenModelsPopup, MSRModelImportPopup


class MSRHeaderWidget(QWidget):
    """Implements the header of the GUI as a QWidget."""

    def __init__(self, main_window: QMainWindow) -> None:
        """Initializes the header widget."""
        super().__init__()

        self._main_window = main_window
        self._popup_open: QWidget = MSROpenModelsPopup(self._main_window)
        self._popup_import: QWidget = MSRModelImportPopup(self._popup_open)

        self.setFixedHeight(30)  # max 1cm height
        header_layout = QHBoxLayout(self)
        header_layout.setContentsMargins(5, 0, 5, 0)
        header_layout.setSpacing(5)  # min distance between buttons

        msr_label = QLabel("MSR")
        msr_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(msr_label, alignment=Qt.AlignLeft)

        self._models_button = QPushButton("Models")
        self._models_button.clicked.connect(self._show_models_menu)
        header_layout.addStretch()
        header_layout.addWidget(self._models_button)

    def _show_models_menu(self) -> None:
        """Creates the models context menu."""

        # Create the menu bar
        context_menu = QMenu(self)
        context_menu.triggered.connect(context_menu.close)

        # Add action to the Library menu
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(
            self._popup_open.show)
        context_menu.addAction(open_action)

        import_action = QAction("Import", self)
        import_action.setShortcut(QKeySequence("Ctrl+I"))
        import_action.triggered.connect(
            self._popup_import.show)
        context_menu.addAction(import_action)

        context_menu.exec(self._models_button.mapToGlobal(
            self._models_button.rect().bottomLeft()))
