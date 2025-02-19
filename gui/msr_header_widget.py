"""This module provides a toolkit for the GUI header definition."""

from pathlib import Path
from typing import List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMenu, QListWidget, QMessageBox,)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QAction
from src import Config
from gui import MSRModelImportPopup


class MSRHeaderWidget(QWidget):
    """Implements the header of the GUI as a QWidget."""

    def __init__(self) -> None:
        """Initializes the header widget."""
        super().__init__()

        self._popup_open: QWidget = None
        self._popup_import: QWidget = MSRModelImportPopup()

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
            self._open_models_popup)
        context_menu.addAction(open_action)

        import_action = QAction("Import", self)
        import_action.setShortcut(QKeySequence("Ctrl+I"))
        import_action.triggered.connect(
            self._popup_import.show)
        context_menu.addAction(import_action)

        context_menu.exec(self._models_button.mapToGlobal(
            self._models_button.rect().bottomLeft()))

    def _open_models_popup(self) -> None:
        """Opens the model selection popup menu."""

        self._popup_open = QWidget()  # garbage collected without self
        self._popup_open.setWindowTitle("Models")
        self._popup_open.resize(600, 400)

        layout = QVBoxLayout(self._popup_open)

        default_label = QLabel("Default Models:")
        default_list = QListWidget()

        custom_label = QLabel("Custom Models:")
        custom_list = QListWidget()

        lib_path = Path(__file__).parents[1] / "lib"

        self.load_models(default_list, lib_path / "models")
        default_list.itemClicked.connect(
            lambda item:
            self.update_loaded_model(item.text(), False, [custom_list]))

        self.load_models(custom_list, lib_path / "imported_models")
        custom_list.itemClicked.connect(
            lambda item:
            self.update_loaded_model(item.text(), True, [default_list]))

        close_button = QPushButton("Close")
        close_button.clicked.connect(self._popup_open.close)

        layout.addWidget(default_label)
        layout.addWidget(default_list)
        layout.addWidget(custom_label)
        layout.addWidget(custom_list)
        layout.addWidget(close_button)

        self._popup_open.show()

    def update_loaded_model(self, model_name: str, custom_model: bool,
                            other_widgets: List[QListWidget] = None, scale=0.02) -> None:
        """Updates the loaded model in the config.

        Args:
            model_name (str): The name of the model to load.
            custom_model (bool): Whether the model is a custom model.
            other_widgets (Optional[List[QListWidget]], optional): Other widgets to clear the selection of. Defaults to None.
            scale (float, optional): The scale of the model shown in the simulation. Defaults to 0.02.
        """
        # TODO: accept different file suffixes
        # TODO: make scaling factor configurable
        if other_widgets is not None:
            for widget in other_widgets:
                widget.clearSelection()

        Config.set_model(model_name, scale, custom_model)

    def load_models(self, list_widget: QListWidget, models_path: Path) -> None:
        """Loads the default models from the default folder into the list widget.

        Args:
            list_widget (QListWidget): The list widget to add the items to.
            models_path (Path): The path to the models folder.
        """
        if not models_path.exists():
            QMessageBox.warning(
                self, "Error", f"Models folder not found at: {models_path}")
            return

        model_names = list(
            {path.stem for path in models_path.iterdir()} - {".gitkeep"})
        # use set comprehension to remove duplicates
        for model_name in model_names:
            list_widget.addItem(model_name)
