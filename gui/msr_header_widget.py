"""
This module provides a header widget for the MSR GUI.

The header includes buttons and menus to manage model imports 
and the display of models. It integrates with other modules to handle 
custom and default models.

Classes:
    MSRHeaderWidget: Implements the header of the GUI as a QWidget.
"""

from pathlib import Path
from typing import List
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QMenu, QListWidget, QMessageBox,
                               QMainWindow, QSizePolicy)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QPixmap
from src import Config
from gui import MSRModelImportPopup


class MSRHeaderWidget(QWidget):
    """Implements the header of the GUI as a QWidget."""

    def __init__(self, main_window: QMainWindow) -> None:
        """Initializes the header widget. 
        Args:
            main_window (QMainWindow): The main window of the application.

        Attributes:
            main_window (QMainWindow): Reference to the main window.
            _popup_open (QWidget): Reference to the currently open popup, if any.
            _popup_import (QWidget): Instance of the import popup.
            _models_button (QPushButton): Button to open the models menu.
            logo_label (QLabel): Label to display the application logo.

        Notes: The `button_height` value is derived from `self._models_button.sizeHint().height() - 10`.
        The `-10` offset compensates for additional padding/margins that Qt includes in the 
        button's size hint calculation. This ensures the logo height aligns visually with the button.
        """
        super().__init__()

        self.main_window = main_window
        self._popup_open: QWidget = None
        self._popup_import: QWidget = MSRModelImportPopup()

        self.setFixedHeight(30)  # max 1cm height
        header_layout = QHBoxLayout(self)
        header_layout.setContentsMargins(5, 0, 5, 0)
        header_layout.setSpacing(5)  # min distance between buttons

        self._models_button = QPushButton("Models")
        self._models_button.clicked.connect(self._show_models_menu)

        button_size_hint = self._models_button.sizeHint()
        button_height = max(1, button_size_hint.height() -
                            10) if isinstance(button_size_hint, QSize) else 22

        self.logo_label = QLabel(self)
        pixmap = QPixmap(Path(__file__).parent / "logo" / "butterfly_logo.png")
        aspect_ratio = pixmap.width() / pixmap.height()
        desired_width = int(button_height * aspect_ratio)

        pixmap = pixmap.scaled(
            desired_width, button_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.logo_label.setPixmap(pixmap)
        self.logo_label.setFixedSize(desired_width, button_height)
        self.logo_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        header_layout.addWidget(self.logo_label, alignment=Qt.AlignVCenter)
        header_layout.addStretch()
        header_layout.addWidget(self._models_button, alignment=Qt.AlignVCenter)

    def _show_models_menu(self) -> None:
        """Creates and displays the models context menu."""

        # Create the menu bar
        context_menu = QMenu(self)
        context_menu.triggered.connect(context_menu.close)

        # Add action to the Library menu
        open_action = QAction("Open", self)
        open_action.triggered.connect(
            self._open_models_popup)
        context_menu.addAction(open_action)

        import_action = QAction("Import", self)
        import_action.triggered.connect(
            self._popup_import.show)
        context_menu.addAction(import_action)

        context_menu.exec(
            self._models_button.mapToGlobal(self._models_button.rect().bottomLeft()))

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
        """Updates the model loaded in the application configuration.

        Args:
            model_name (str): The name of the model to load.
            custom_model (bool): Whether the model is a custom model.
            other_widgets (Optional[List[QListWidget]], optional): Other widgets to clear 
            the selection of. Defaults to None.
            scale (float, optional): The scale of the model shown in the simulation. 
            Defaults to 0.02.
        """
        # TODO: accept different file suffixes
        # TODO: make scaling factor configurable
        if other_widgets is not None:
            for widget in other_widgets:
                widget.clearSelection()

        Config.set_model(model_name, scale, custom_model)
        self.main_window.update_model()

    def load_models(self, list_widget: QListWidget, models_path: Path) -> None:
        """Loads the models from the specified directory into the given list widget.

        Args:
            list_widget (QListWidget): The widget to display the list of models.
            models_path (Path): The path to the directory containing model files.
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
