"""
This module provides a header widget for the MSR GUI.

The header includes buttons and menus to manage model imports, shortcuts, 
and the display of models. It integrates with other modules to handle 
custom and default models.

Classes:
    MSRHeaderWidget: Implements the header of the GUI as a QWidget.
"""

from pathlib import Path
from typing import List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,     QLabel, QPushButton, QMenu, QListWidget, QMessageBox,)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QShortcut
from gui.shortcuts_utils import (setup_global_shortcuts,
                                 get_platform_specific_shortcuts, shortcuts_config)
from gui import MSRModelImportPopup
from src.config import Config
from src.mesh_loader import MeshLoader


class MSRHeaderWidget(QWidget):
    """Implements the header of the GUI as a QWidget."""

    def __init__(self) -> None:
        """Initializes the header widget."""
        super().__init__()

        self.popup_open: QWidget = None
        self.popup_import: QWidget = MSRModelImportPopup()

        self.setFixedHeight(30)  # max 1cm height

        header_layout = QHBoxLayout(self)
        header_layout.setContentsMargins(5, 0, 5, 0)
        header_layout.setSpacing(5)  # min distance between buttons

        msr_label = QLabel("MSR")
        msr_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(msr_label, alignment=Qt.AlignLeft)

        self._models_button = QPushButton("Models")
        self._models_button.clicked.connect(self.show_models_menu)
        header_layout.addStretch()
        header_layout.addWidget(self._models_button)

        setup_global_shortcuts(self)

    def show_models_menu(self) -> None:
        """Creates and displays the models context menu."""

        context_menu = QMenu(self)
        context_menu.triggered.connect(context_menu.close)

        for action_name, config in shortcuts_config.items():
            shortcut_key = get_platform_specific_shortcuts(config["key"])
            method_name = config["method"]

            print(f"Checking for method '{method_name}'")

            if hasattr(self, method_name):
                action = QAction(action_name.replace(
                    '_', ' ').capitalize(), self)
                action.setShortcut(shortcut_key)
                action.triggered.connect(getattr(self, method_name))
                context_menu.addAction(action)

                shortcut = QShortcut(shortcut_key, self)
                shortcut.setContext(Qt.WindowShortcut)
                shortcut.activated.connect(getattr(self, method_name))

                print(
                    f"Setting up shortcut '{shortcut_key.toString()}' for method '{method_name}'")

            else:
                print(
                    f"Warning: Widget has no method '{method_name}' for shortcut '{shortcut_key}'")

        context_menu.exec(self._models_button.mapToGlobal(
            self._models_button.rect().bottomLeft()))

    def open_models_popup(self, menu: QMenu) -> None:
        """Opens the models popup menu.

        Args:
            menu (QMenu): The menu to close when opening the popup.
        """
        if menu:
            menu.close()

        self.popup_open = QWidget()  # garbage collected without self
        self.popup_open.setWindowTitle("Models")
        self.popup_open.resize(600, 400)

        layout = QVBoxLayout(self.popup_open)

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

        import_button = QPushButton("Close")
        import_button.clicked.connect(self.popup_open.close)
        # TODO Implement import_custom_model or use super? (GUI refactoring issue)
        # import_button.clicked.connect(self.import_custom_model)

        layout.addWidget(default_label)
        layout.addWidget(default_list)
        layout.addWidget(custom_label)
        layout.addWidget(custom_list)
        layout.addWidget(import_button)

        self.popup_open.show()

    def show_popup_import(self) -> None:
        """Opens the import models popup window."""
        self.popup_import.show()

    def update_loaded_model(self, model_name: str, custom_model: bool,
                            other_widgets: List[QListWidget] = None, scale: float = 0.02) -> None:
        """Updates the model loaded in the application configuration.

        Args:
            model_name (str): The name of the model to load.
            custom_model (bool): Whether the model is a custom model.
            other_widgets (Optional[List[QListWidget]], optional): Other widgets to 
            clear the selection of. Defaults to None.
            scale (float, optional): The scale of the model 
            shown in the simulation. Defaults to 0.02.
        """
        # TODO: make scaling factor configurable
        if other_widgets is not None:
            for widget in other_widgets:
                widget.clearSelection()

        # Config.set_model(model_name, scale)
        # My idea how custom models could be implemented
        Config.set_model(model_name, scale, custom_model)

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

        model_names = []
        for path in models_path.iterdir():
            if path.is_file():
                try:
                    name = path.stem
                    mode = None
                    if "_surface" in name:
                        mode = MeshLoader.Mode.SURFACE
                    elif "_volumetric" in name:
                        mode = MeshLoader.Mode.VOLUMETRIC
                    else:
                        continue

                    MeshLoader.validate_mesh_file(path, mode)
                    model_names.append(name)
                except ValueError:
                    continue

        for model_name in sorted(set(model_names)):
            list_widget.addItem(model_name)
