from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QCheckBox, QLabel, QWidget, QHBoxLayout
)
from PySide6.QtGui import QLinearGradient, QPainter

from src.units import YoungsModulus


class MSRHeatmapBar(QLabel):
    def paintEvent(self, arg__1) -> None:
        super().paintEvent(arg__1)

        painter = QPainter(self)
        gradient = QLinearGradient(
            self.width()/2, self.height(), self.width()/2, 0)

        colors = ["blue", "green", "yellow", "red"]
        for i, c in enumerate(colors):
            # c = 255*c
            gradient.setColorAt(
                i/(len(colors)-1),
                c,
            )

        painter.fillRect(self.rect(), gradient)


class MSRHeatmap(QWidget):
    def __init__(self, parent=...):
        super().__init__(parent)

        self._heatmap = MSRHeatmapBar(self)
        self._heatmap.setFixedWidth(40)
        self._heatmap.setFixedHeight(170)

        self._min_label = QLabel("min: tbd", self)
        self._max_label = QLabel("max: tbd", self)

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self._max_label)
        self._layout.addWidget(self._heatmap)
        self._layout.addWidget(self._min_label)

    def set_min(self, val: float) -> None:
        self._min_label.setText(
            f"min: {round(YoungsModulus.from_Pa(val).Pa, 2)} Pa")

    def set_max(self, val: float) -> None:
        self._max_label.setText(
            f"max: {round(YoungsModulus.from_Pa(val).MPa, 2)} MPa")


class MSRStressAnalysisWidget(QGroupBox):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._stress_checkbox = QCheckBox("Stress Visualization", self)
        self._heatmap = MSRHeatmap(self)

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self._stress_checkbox)
        self._layout.addWidget(self._heatmap)

    @property
    def show_stress(self) -> bool:
        """Should stress be visualized?

        Returns:
            bool: True iff stress should be visualized?
        """
        return self._stress_checkbox.isChecked()

    def set_min(self, val: float) -> None:
        self._heatmap.set_min(val)

    def set_max(self, val: float) -> None:
        self._heatmap.set_max(val)
