
import re
from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QCheckBox, QGridLayout, QTextEdit
)


class MSRDeformationAnalysisWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Maximum Deformation Analysis")

        layout = QVBoxLayout(self)

        # Add checkbox to enable the deformation analysis
        enable_checkbox = QCheckBox("Enable Deformation Analysis")
        layout.addWidget(enable_checkbox)

        # Add Widgets for the selection of the points
        point_selector = QGridLayout()

        # Add checkboxes for the way the points are selected
        self.point_checkboxes = [
            QCheckBox("Indices"),
            QCheckBox("Coordinates"),
            QCheckBox("All Points")
        ]
        point_selector.addWidget(self.point_checkboxes[0], 0, 0)
        point_selector.addWidget(self.point_checkboxes[1], 0, 1)
        point_selector.addWidget(self.point_checkboxes[2], 0, 2)

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
        self.point_inputs[0].setEnabled(False)
        point_selector.addWidget(self.point_inputs[0], 1, 0)
        self.indices_regex = re.compile(r"^\s*\d+\s*(,\s*\d+\s*)*$")

        self.point_inputs[1].setPlaceholderText(
            "Enter coordinates as [x1, y1, z1],\n[x2, y2, z2],\n...")
        self.point_inputs[1].setEnabled(False)
        point_selector.addWidget(self.point_inputs[1], 1, 1)
        self.coord_regex = re.compile(
            r"/\A\s*\[\s*(-?\d+(\.\d+)?\s*,\s*){2}-?\d+(\.\d+)?\s*\]\s*(,\s*\n\s*\[\s*(-?\d+(\.\d+)?\s*,\s*){2}-?\d+(\.\d+)?\s*\]\s*)*\Z",
            re.M
        )

        layout.addLayout(point_selector)

        # Enable point selection when deformation analysis is enabled
        enable_checkbox.stateChanged.connect(self._enable_point_selection)

    def _unselect_other_point_checkboxes(self, state: bool, index: int) -> None:
        if not state:
            return
        for i, checkbox in enumerate(self.point_checkboxes):
            if i != index:
                checkbox.setChecked(False)
        for i, input_field in enumerate(self.point_inputs):
            if i == index:
                input_field.setEnabled(True)
            else:
                input_field.setEnabled(False)

    def _enable_point_selection(self, state: bool) -> None:
        for i, checkbox in enumerate(self.point_checkboxes):
            checkbox.setEnabled(state)
            if state and checkbox.isChecked() and i in [0, 1]:
                self.point_inputs[i].setEnabled(True)
            elif not state and i in [0, 1]:
                self.point_inputs[i].setEnabled(False)
