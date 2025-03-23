# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ #
#                        MSR, Magnetic Soft Robotics Simulation                        #
#   Copyright (C) 2025 Julius Hahnewald, Heiko Hellkamp, Finn Schubert, Carla Wehner   #
#                                                                                      #
# This program is free software; you can redistribute it and/or                        #
# modify it under the terms of the GNU Lesser General Public                           #
# License as published by the Free Software Foundation; either                         #
# version 2.1 of the License, or (at your option) any later version.                   #
#                                                                                      #
# This program is distributed in the hope that it will be useful,                      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU                    #
# Lesser General Public License for more details.                                      #
#                                                                                      #
# You should have received a copy of the GNU Lesser General Public                     #
# License along with this program; if not, write to the Free Software                  #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301            #
# USA                                                                                  #
# ------------------------------------------------------------------------------------ #
# Contact information: finn.s.schubert@gmail.com                                       #
# ____________________________________________________________________________________ #

"""This module bundels functionality around the selection of models. 
It includes a widget with two list selections, for choosing between builtin and custom models.
Upon selecting a model, the selection process might either be discarded by closing the window, 
or loading the selected model into the simulation by the press of a button.

Classes:
    Implements a popup window for model selection as a QWidget.
"""

from pathlib import Path
from typing import List, Optional
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QMainWindow,
                               QLabel, QPushButton, QListWidget, QMessageBox,)
from PySide6.QtGui import QFont
from src import Config


class MSROpenModelsPopup(QWidget):
    """A class implementing the popup for model selection.
    Inherits from QWidget.
    Provides functionality for loading, selecting and opening models into the simulation.
    """

    def __init__(self, main_window: QMainWindow):
        """Initializes the popup for model selection. 

        Attributes:
            default_list (QListWidget): The widget listing the predefined models
            custom_list (QListWidget): The widget listing all user-imported models

        Args:
            main_window (QMainWindow): The main GUI window.
        """

        super().__init__()
        self.setWindowTitle("Models")
        self.resize(600, 400)

        self._main_window = main_window
        self._layout = QVBoxLayout(self)
        self.default_list = QListWidget()
        self.custom_list = QListWidget()

        self._selected_model_name = None
        self._selected_is_custom = None
        self._selected_scale = None

        default_label = QLabel("Default Models:")
        custom_label = QLabel("Custom Models:")

        selection_text_label = QLabel("Current Selection:")
        self._selection_label = QLabel("")

        fat_text = QFont()
        fat_text.setBold(True)
        for label in [default_label, custom_label, selection_text_label]:
            label.setFont(fat_text)

        lib_path = Path(__file__).parents[1] / "lib"

        self.load_models(self.default_list, lib_path / "models")
        self.default_list.itemActivated.connect(
            lambda item:
            self.update_loaded_model(item.text(), False, [self.custom_list]))
        self.default_list.itemSelectionChanged.connect(
            self.custom_list.clearSelection)

        self.load_models(self.custom_list, lib_path / "imported_models")
        self.custom_list.itemActivated.connect(
            lambda item:
            self.update_loaded_model(item.text(), True, [self.default_list]))
        self.custom_list.itemSelectionChanged.connect(
            self.default_list.clearSelection)

        open_button = QPushButton("Open Model")
        open_button.clicked.connect(self.open_model)

        self._layout.addWidget(default_label)
        self._layout.addWidget(self.default_list)
        self._layout.addWidget(custom_label)
        self._layout.addWidget(self.custom_list)
        self._layout.addWidget(selection_text_label)
        self._layout.addWidget(self._selection_label)
        self._layout.addWidget(open_button)

    def update_loaded_model(self, model_name: str, custom_model: bool,
                            other_widgets: List[QListWidget] = None, scale: Optional[float] = None) -> None:
        """Updates the loaded model in the config.

        Args:
            model_name (str): The name of the model to load.
            custom_model (bool): Whether the model is a custom model.
            other_widgets (Optional[List[QListWidget]], optional): Other widgets to clear the selection of. Defaults to None.
            scale (Optional[float], optional): The scale of the model shown in the simulation. 
                If set to None, uses the default scales (This means a predefined scale for the example models
                and a scale of `0.01` for any custom model). Defaults to None.

        Raises:
            ValueError: If scale is less than or equal to 0.
        """
        if other_widgets is not None:
            for widget in other_widgets:
                widget.clearSelection()

        self._selected_model_name = model_name
        self._selected_is_custom = custom_model
        self._selected_scale = scale

        self._selection_label.setText(f">> {model_name}")

    def open_model(self):
        """Loads the selected model into the configuration file and displays information on the model in the main window.
        Displays a warning if no model is selected.
        Displays a message after everything succeeds.
        """
        if self._selected_is_custom is None or self._selected_model_name is None:
            QMessageBox.warning(
                self,
                "Model Selection Error",
                "Please select a model. If you find none appealing, feel free to import your own.",
            )
            return

        Config.set_model(self._selected_model_name,
                         self._selected_scale, self._selected_is_custom)
        self._main_window.update_model()

        QMessageBox.information(
            self,
            "Success!",
            "The selected model will be used in the next simulation run.",
        )
        self.close()

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
