

import re
from enum import Enum

from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QCheckBox, QGridLayout, QTextEdit, QLabel, QLineEdit
)
from PySide6.QtCore import Qt


class MSRDeformationAnalysisWidget(QGroupBox):

    class SelectionMode(Enum):
        """Enum class for the different ways to select points."""
        INDICES = 0
        COORDINATES = 1
        ALL = 2

    def __init__(self) -> None:
        super().__init__("Maximum Deformation Analysis")

        layout = QVBoxLayout(self)

        # Add checkbox to enable the deformation analysis
        self.enable_checkbox = QCheckBox("Enable Deformation Analysis")
        layout.addWidget(self.enable_checkbox)

        # Add Widgets for the selection of the points
        point_selector = QGroupBox("Point Selection")
        point_selector_layout = QGridLayout()

        # Add checkboxes for the way the points are selected
        self.point_checkboxes = [
            QCheckBox("Indices"),
            QCheckBox("Coordinates"),
            QCheckBox("All Points")
        ]
        point_selector_layout.addWidget(self.point_checkboxes[0], 0, 0)
        point_selector_layout.addWidget(self.point_checkboxes[1], 0, 1)
        point_selector_layout.addWidget(self.point_checkboxes[2], 0, 2)

        self.point_checkboxes[2].setChecked(True)
        for i, checkbox in enumerate(self.point_checkboxes):
            checkbox.stateChanged.connect(
                lambda state, index=i: self._unselect_other_point_checkboxes(
                    state, index)
            )
            checkbox.setEnabled(False)

        # Add text fields for the indices and coordinates
        self.point_inputs = [QTextEdit(), QTextEdit()]
        self.point_inputs[0].setPlaceholderText(
            "Enter indices separated by comma")
        self.point_inputs[0].setReadOnly(True)
        point_selector_layout.addWidget(self.point_inputs[0], 1, 0)
        self.indices_regex = re.compile(r"^\s*\d+\s*(,\s*\d+\s*)*$")

        self.point_inputs[1].setPlaceholderText(
            "Enter coordinates as [x1, y1, z1],\n[x2, y2, z2],\n...")
        self.point_inputs[1].setReadOnly(True)
        point_selector_layout.addWidget(self.point_inputs[1], 1, 1)
        self.coord_regex = re.compile(
            r"\A\s*\[\s*(-?\d+(\.\d+)?\s*,\s*){2}-?\d+(\.\d+)?\s*\]\s*" +
            r"(,\s*\n\s*\[\s*(-?\d+(\.\d+)?\s*,\s*){2}-?\d+(\.\d+)?\s*\]\s*)*\Z",
            re.M
        )

        point_selector.setLayout(point_selector_layout)
        layout.addWidget(point_selector)

        # Add widgets for the output
        result_box = QGroupBox("Result")

        output = QGridLayout()

        dimension_labels = [
            QLabel("X Axis"),
            QLabel("Y Axis"),
            QLabel("Z Axis")
        ]
        for i, label in enumerate(dimension_labels):
            label.setAlignment(Qt.AlignCenter)
            output.addWidget(label, 0, i)

        self.result = [QLineEdit(), QLineEdit(), QLineEdit()]
        for i, line in enumerate(self.result):
            line.setReadOnly(True)
            output.addWidget(line, 1, i)

        result_box.setLayout(output)
        layout.addWidget(result_box)

        # Enable point selection when deformation analysis is enabled
        self.enable_checkbox.stateChanged.connect(self._enable_point_selection)

    def _unselect_other_point_checkboxes(self, state: bool, index: int) -> None:
        if not state:
            return
        for i, checkbox in enumerate(self.point_checkboxes):
            if i != index:
                checkbox.setChecked(False)
        for i, input_field in enumerate(self.point_inputs):
            if i == index:
                input_field.setReadOnly(False)
            else:
                input_field.setReadOnly(True)

    def _enable_point_selection(self, state: bool) -> None:
        for i, checkbox in enumerate(self.point_checkboxes):
            checkbox.setEnabled(state)
            if state and checkbox.isChecked() and i in [0, 1]:
                self.point_inputs[i].setReadOnly(False)
            elif not state and i in [0, 1]:
                self.point_inputs[i].setReadOnly(True)

    def enabled(self) -> bool:
        return self.enable_checkbox.isChecked()
