"""This module provides a toolkit for the GUI header definition."""

from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QMenu, QListWidget, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QAction
from src import Config
# from src.mesh_loader import Mode as MeshMode, endings as mesh_endings # used for commented code


class MSRHeaderWidget(QWidget):
    """Implements the header of the GUI as a QWidget.
    """

    def __init__(self) -> None:
        """Initializes the header widget.
        """
        super().__init__()

        self.setFixedHeight(30)  # Maximal 1 cm Höhe
        header_layout = QHBoxLayout(self)
        header_layout.setContentsMargins(5, 0, 5, 0)
        header_layout.setSpacing(5)  # Minimaler Abstand zwischen Buttons

        msr_label = QLabel("MSR")
        msr_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(msr_label, alignment=Qt.AlignLeft)

        self.library_button = QPushButton("Library")
        self.library_button.clicked.connect(self.show_library_menu)
        header_layout.addStretch()
        header_layout.addWidget(self.library_button)

    def show_library_menu(self) -> None:
        """Creates the library menu.
        """

        # Create the menu bar
        context_menu = QMenu(self)

        # Add action to the Library menu
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(
            lambda _: self.open_library(context_menu))
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

        context_menu.exec(self.library_button.mapToGlobal(
            self.library_button.rect().bottomLeft()))

    def open_library(self, menu: QMenu) -> None:
        """Opens the library popup menu.

        Args:
            menu (QMenu): The menu to close when opening the popup.
        """
        menu.close()

        self._popup = QWidget()  # garbage collcted without self
        self._popup.setWindowTitle("Library")
        self._popup.resize(600, 400)

        layout = QVBoxLayout(self._popup)

        default_label = QLabel("Default Library:")
        default_list = QListWidget()
        self.load_default_models(default_list)
        default_list.currentTextChanged.connect(
            self.update_loaded_model)

        custom_label = QLabel("Custom Library:")
        custom_list = QListWidget()

        import_button = QPushButton("Import")
        # TODO Implement import_custom_model or use super? (GUI refactoring issue)
        # import_button.clicked.connect(self.import_custom_model)

        layout.addWidget(default_label)
        layout.addWidget(default_list)
        layout.addWidget(custom_label)
        layout.addWidget(custom_list)
        layout.addWidget(import_button)

        self._popup.show()

    def update_loaded_model(self, model_name: str) -> None:
        """Updates the loaded mesh in the config.

        Args:
            currentText (str): The currently selected file name in the widget.
        """
        # TODO: make scaling factor configurable
        Config.set_model(model_name, .02)  # use .02 for now

    def load_default_models(self, list_widget: QListWidget) -> None:
        """Loads the default models from the default folder into the list widget.

        Args:
            list_widget (QListWidget): The list widget to add the items to.
        """

        models_path = Path(__file__).parent.parent / "lib/models"

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
