"""This module contains the widgets for the post simulation analysis."""

import re
from enum import Enum
from typing import List

from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QCheckBox, QGridLayout, QTextEdit, QLabel, QLineEdit, QRadioButton
)
from PySide6.QtCore import Qt


class MSRDeformationAnalysisWidget(QGroupBox):
    """Widget for the deformation analysis of the simulation results."""

    class SelectionMode(Enum):
        """Enum class for the different ways to select points."""
        INDICES = 0
        COORDINATES = 1
        ALL = 2

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
            "Enter coordinates as [x1, y1, z1],\n[x2, y2, z2],\n...")
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

        self.result = [QLineEdit(), QLineEdit(), QLineEdit()]
        for i, line_edit in enumerate(self.result):
            line_edit.setReadOnly(True)
            self._output.addWidget(line_edit, 1, i)

        self.result_indices = None

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
        for i, result in enumerate(results):
            self.result[i].setText(str(result))

        if self.result_indices is None:
            self.result_indices = [QLabel(), QLabel(), QLabel()]
            for i, label in enumerate(self.result_indices):
                label.setAlignment(Qt.AlignCenter)
                self._output.addWidget(label, 2, i)
        for i, index in enumerate(indices):
            self.result_indices[i].setText(f"Index: {index}")

    def display_input_error(self, message: str) -> None:
        error_message = QLabel(message)
        error_message.setAlignment(Qt.AlignCenter)
        error_message.setStyleSheet("color: crimson")
        self._output.addWidget(error_message, 3, 0, 1, 3)

    def get_mode(self) -> SelectionMode:
        """Returns the mode of the point selection.

        Returns:
            SelectionMode: The mode of the point selection
        """
        if self.point_radio_buttons[0].isChecked():
            return self.SelectionMode.ALL
        if self.point_radio_buttons[1].isChecked():
            return self.SelectionMode.COORDINATES
        return self.SelectionMode.INDICES
