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

"""This module contains the widgets for the post simulation analysis."""

import re
from typing import List

from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QCheckBox, QGridLayout, QTextEdit, QLabel, QLineEdit, QRadioButton, QHBoxLayout
)
from PySide6.QtCore import Qt

from src import AnalysisParameters


class MSRDeformationAnalysisWidget(QGroupBox):
    """Widget for the deformation analysis of the simulation results."""

    def __init__(self) -> None:
        """Initializes the widget for the deformation analysis.
        """
        super().__init__("Maximum Deformation Analysis")

        layout = QVBoxLayout(self)

        # Add checkbox to enable the deformation analysis
        self.enable_checkbox = QCheckBox("Enable Deformation Analysis")
        layout.addWidget(self.enable_checkbox)

        # Add Widgets for the selection of the points
        point_selector = QGroupBox("Point Selection")
        point_selector_layout = QGridLayout()

        # Add checkboxes for the way the points are selected
        self.point_radio_buttons = [
            QRadioButton("All Points"),
            QRadioButton("Coordinates"),
            QRadioButton("Indices"),
        ]
        point_selector_layout.addWidget(self.point_radio_buttons[0], 0, 0)
        point_selector_layout.addWidget(self.point_radio_buttons[1], 1, 0)
        point_selector_layout.addWidget(self.point_radio_buttons[2], 1, 1)

        self.point_radio_buttons[0].setChecked(True)
        for i, checkbox in enumerate(self.point_radio_buttons):
            checkbox.toggled.connect(
                lambda state, index=i: self._enable_text_field(
                    state, index)
            )
            checkbox.setEnabled(False)

        # Add text fields for the indices and coordinates
        self.point_inputs = [QTextEdit(), QTextEdit()]
        self.point_inputs[1].setPlaceholderText(
            "Enter indices separated by comma")
        self.point_inputs[1].setReadOnly(True)
        point_selector_layout.addWidget(self.point_inputs[0], 2, 0)
        self.indices_regex = re.compile(r"^\s*\d+\s*(,\s*\d+\s*)*$")

        self.point_inputs[0].setPlaceholderText(
            "Enter coordinates as\n[x1, y1, z1],\n[x2, y2, z2],\n...")
        self.point_inputs[0].setReadOnly(True)
        point_selector_layout.addWidget(self.point_inputs[1], 2, 1)
        self.coord_regex = re.compile(
            r"\A\s*\[\s*(-?\d+(\.\d+)?\s*,\s*){2}-?\d+(\.\d+)?\s*\]\s*" +
            r"(,\s*\n\s*\[\s*(-?\d+(\.\d+)?\s*,\s*){2}-?\d+(\.\d+)?\s*\]\s*)*\Z",
            re.M
        )

        point_selector.setLayout(point_selector_layout)
        layout.addWidget(point_selector)

        # Add widgets for the output
        result_box = QGroupBox("Result")

        self._output = QGridLayout()

        dimension_labels = [
            QLabel("X Axis"),
            QLabel("Y Axis"),
            QLabel("Z Axis")
        ]
        for i, label in enumerate(dimension_labels):
            label.setAlignment(Qt.AlignCenter)
            self._output.addWidget(label, 0, i)

        self.result_outputs = [QLineEdit(), QLineEdit(), QLineEdit()]
        for i, line_edit in enumerate(self.result_outputs):
            line_edit.setReadOnly(True)
            self._output.addWidget(line_edit, 1, i)

        self.result_indices = [QLabel(), QLabel(), QLabel()]
        self.result_indices_box = QHBoxLayout()
        for label in self.result_indices:
            label.setAlignment(Qt.AlignCenter)
            self.result_indices_box.addWidget(label)
            label.setText("Index: tbd")
        self._output.addLayout(self.result_indices_box, 2, 0, 1, 3)

        result_box.setLayout(self._output)
        layout.addWidget(result_box)

        # Enable point selection when deformation analysis is enabled
        self.enable_checkbox.stateChanged.connect(self._enable_point_selection)

    def _enable_text_field(self, state: bool, index: int) -> None:
        """Enables or disables the corresponding text field 
        based on the state of the radio button.

        Args:
            state (bool): The state of the radio button
            index (int): Index of the checkbox in the point_radio_buttons list
        """
        if index == 0:  # Index 0 -> All Points radio button (no text field)
            return
        if not state:
            self.point_inputs[index-1].setReadOnly(True)
        elif state:
            self.point_inputs[index-1].setReadOnly(False)

    def _enable_point_selection(self, state: bool) -> None:
        """Enables or disables the point selection based on the state of the checkbox.

        Args:
            state (bool): The state of the enable checkbox
        """
        for i, checkbox in enumerate(self.point_radio_buttons):
            checkbox.setEnabled(state)
            if i == 0:  # Index 0 -> All Points radio button (no text field)
                continue
            if state and checkbox.isChecked():
                self.point_inputs[i-1].setReadOnly(False)
            elif not state:
                self.point_inputs[i-1].setReadOnly(True)

    def is_enabled(self) -> bool:
        """Returns if the deformation analysis is enabled.

        Returns:
            bool: True if the deformation analysis is enabled, False otherwise
        """
        return self.enable_checkbox.isChecked()

    def update_results(self, results: List[float], indices: List[int]) -> None:
        """Updates the content of the results area with the given list of analysis results
        and the corresponding indices.

        Args:
            results (List[float]): The list of deformation analysis results
            indices (List[int]): The list of indices
        """
        for output, result in zip(self.result_outputs, results):
            output.setText(str(result))

        for output, index in zip(self.result_indices, indices):
            output.setStyleSheet("")
            output.setText(f"Index: {index}")

    def display_input_error(self, message: str) -> None:
        """Displays the given message as an error in the results section.

        Args:
            message (str): The message to display
        """
        for i, ind in enumerate(self.result_indices):
            if i == 1:
                ind.setText(message)
                ind.setStyleSheet("color: crimson")
            else:
                ind.setText("")

    def get_mode(self) -> AnalysisParameters.SelectionMode:
        """Returns the mode of the point selection.

        Returns:
            SelectionMode: The mode of the point selection
        """
        if self.point_radio_buttons[0].isChecked():
            return AnalysisParameters.SelectionMode.ALL
        if self.point_radio_buttons[1].isChecked():
            return AnalysisParameters.SelectionMode.COORDINATES
        return AnalysisParameters.SelectionMode.INDICES

    def reset(self) -> None:
        """Resets the labels and the saved min/max values used for input validation.
        Useful e.g. for running another simulation.
        """
        for i, result in enumerate(self.result_outputs):
            result.setText("")
            self.result_indices[i].setText("Index: tbd")
            self.result_indices[i].setStyleSheet("")
