"""This module bundles functionality needed for the GUI implementation of the stress analysis.
"""

from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QCheckBox, QLabel, QWidget, QHBoxLayout
)
from PySide6.QtGui import QLinearGradient, QPainter, QPaintEvent

from src.units import YoungsModulus


class MSRHeatmapBar(QLabel):
    """Subclass of QLabel displaying the stress color gradient.
    """

    def paintEvent(self, arg__1: QPaintEvent) -> None:
        """custom reimplementation of the paintEvent of QLabel. Responsible for drawing the gradient.

        Args:
            arg__1 (QPaintEvent): the event
        """
        super().paintEvent(arg__1)
        self.setFixedWidth(40)
        self.setFixedHeight(170)

        painter = QPainter(self)
        gradient = QLinearGradient(
            self.width()/2, self.height(), self.width()/2, 0)

        colors = ["blue", "cyan", "yellow", "red"]
        for i, c in enumerate(colors):
            # c = 255*c
            gradient.setColorAt(
                i/(len(colors)-1),
                c,
            )

        painter.fillRect(self.rect(), gradient)


class MSRHeatmap(QWidget):
    """A QWidget that displays a heatmap and labels for minimum / maximum measured stress.
    """

    def __init__(self, parent: QWidget = ...):
        """Initializes the heatmap display includimg labels for minimum and maximum stress.

        Args:
            parent (QWidget, optional): Parent widget. Defaults to ....
        """
        super().__init__(parent)

        self._heatmap = MSRHeatmapBar(self)

        self._min_label = QLabel("min: tbd", self)
        self._max_label = QLabel("max: tbd", self)

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self._max_label)
        self._layout.addWidget(self._heatmap)
        self._layout.addWidget(self._min_label)

    def set_min(self, val: float) -> None:
        """Updates the minimum measured value for the heatmap legend.

        Args:
            val (float): The new value in Pa.
        """
        self._min_label.setText(
            f"min: {round(YoungsModulus.from_Pa(val).Pa, 2)} Pa")

    def set_max(self, val: float) -> None:
        """Updates the maximum measured value for the heatmap legend.

        Args:
            val (float): The new value in Pa.
        """
        self._max_label.setText(
            f"max: {round(YoungsModulus.from_Pa(val).MPa, 2)} MPa")


class MSRStressAnalysisWidget(QGroupBox):
    """Widget to setup stress analysis. Inherits from QGroupBox.
    """

    def __init__(self, parent: QWidget = None) -> None:
        """Initializes the MSRStressAnalyzationWidget.

        Args:
            parent (QWidget, optional): the parent widget. Defaults to None.
        """
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
        """Updates the minimum measured value for the heatmap legend.

        Args:
            val (float): The new value in Pa.
        """
        self._heatmap.set_min(val)

    def set_max(self, val: float) -> None:
        """Updates the maximum measured value for the heatmap legend.

        Args:
            val (float): The new value in Pa.
        """
        self._heatmap.set_max(val)
