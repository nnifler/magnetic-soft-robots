"""This module provides a toolkit for the GUI header definition."""

from pathlib import Path
from typing import List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QMenu, QListWidget, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QAction
from src import Config
# from src.mesh_loader import Mode as MeshMode, endings as mesh_endings # used for commented code


class MSRHeaderWidget(QWidget):
    """Implements the header of the GUI as a QWidget."""

    def __init__(self) -> None:
        """Initializes the header widget."""
        super().__init__()

        self.setFixedHeight(30)  # Maximal 1 cm Höhe
        header_layout = QHBoxLayout(self)
        header_layout.setContentsMargins(5, 0, 5, 0)
        header_layout.setSpacing(5)  # Minimaler Abstand zwischen Buttons

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

        # Add action to the Library menu
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(
            lambda _: self._open_models_popup(context_menu))
        context_menu.addAction(open_action)

        import_action = QAction("Import", self)
        import_action.setShortcut(QKeySequence("Ctrl+I"))
        import_action.triggered.connect(
            lambda _: self.import_library(context_menu))
        context_menu.addAction(import_action)

        export_action = QAction("Export", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(
            lambda _: self.export_library(context_menu))
        context_menu.addAction(export_action)

        context_menu.exec(self._models_button.mapToGlobal(
            self._models_button.rect().bottomLeft()))

    def _open_models_popup(self, menu: QMenu) -> None:
        """Opens the models popup menu.

        Args:
            menu (QMenu): The menu to close when opening the popup.
        """
        menu.close()

        self._popup = QWidget()  # garbage collected without self
        self._popup.setWindowTitle("Models")
        self._popup.resize(600, 400)

        layout = QVBoxLayout(self._popup)

        default_label = QLabel("Default Models:")
        default_list = QListWidget()

        custom_label = QLabel("Custom Models:")
        custom_list = QListWidget()

        lib_path = Path(__file__).parents[1] / "lib"

        self.load_models(default_list, lib_path / "models")
        default_list.currentTextChanged.connect(
            lambda model_name:
            self.update_loaded_model(model_name, False, [custom_list]))

        # TODO: change to custom model path
        self.load_models(custom_list, lib_path / "models")
        custom_list.currentTextChanged.connect(
            lambda model_name:
            self.update_loaded_model(model_name, True, [default_list]))

        import_button = QPushButton("Close")
        import_button.clicked.connect(self._popup.close)
        # TODO Implement import_custom_model or use super? (GUI refactoring issue)
        # import_button.clicked.connect(self.import_custom_model)

        layout.addWidget(default_label)
        layout.addWidget(default_list)
        layout.addWidget(custom_label)
        layout.addWidget(custom_list)
        layout.addWidget(import_button)

        self._popup.show()

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

        Config.set_model(model_name, scale)
        # Config.set_model(model_name, scaling, custom_model)  # My idea how custom models could be implemented

    def load_models(self, list_widget: QListWidget, models_path: Path) -> None:
        """Loads the default models from the default folder into the list widget.

        Args:
            list_widget (QListWidget): The list widget to add the items to.
            models_path (Path): The path to the models folder.
        """
        if not models_path.exists:
            QMessageBox.warning(
                self, "Error", f"Models folder not found at: {models_path}")
            return

        # previous implementation: problem with both surface and volumetric mesh endings
        # self._default_list_filenames = []
        # for filepath in models_path.iterdir():
        #     if filepath.suffix not in mesh_endings[MeshMode.SURFACE.value]:
        #         return
        #     self._default_list.addItem(filepath.stem)
        #     self._default_list_filenames.append(filepath.stem)

        model_names = list({path.stem for path in models_path.iterdir()})
        # use set comprehension to remove duplicates
        for model_name in model_names:
            list_widget.addItem(model_name)
