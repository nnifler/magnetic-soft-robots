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

"""
This module provides a header widget for the MSR GUI.

The header includes buttons and menus to manage model imports 
and the display of models. It integrates with other modules to handle 
custom and default models.

Classes:
    MSRHeaderWidget: Implements the header of the GUI as a QWidget.
"""

from pathlib import Path
from PySide6.QtWidgets import (QWidget, QHBoxLayout,
                               QLabel, QPushButton, QMenu, QMainWindow, QSizePolicy)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QPixmap
from gui import MSROpenModelsPopup, MSRModelImportPopup


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

        self._main_window = main_window
        self._popup_open: QWidget = MSROpenModelsPopup(self._main_window)
        self._popup_import: QWidget = MSRModelImportPopup(self._popup_open)

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
            self._popup_open.show)
        context_menu.addAction(open_action)

        import_action = QAction("Import", self)
        import_action.triggered.connect(
            self._popup_import.show)
        context_menu.addAction(import_action)

        context_menu.exec(self._models_button.mapToGlobal(
            self._models_button.rect().bottomLeft()))
