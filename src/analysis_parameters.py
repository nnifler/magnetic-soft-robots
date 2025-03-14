"""This module contains the class that hold all parameters important for the analysis."""

from typing import List, Optional
import numpy as np
from PySide6.QtWidgets import QWidget


class AnalysisParameters:
    """Class that holds all parameters important for the analysis"""

    def __init__(self):
        """Initializes the class with every analysis disabled.
        """
        self.max_deformation_analysis = False
        self.max_deformation_input = None
        self.max_deformation_widget = None

        self._stress_analysis = False
        self._stress_widget = None

    def __repr__(self) -> str:
        """Returns a string representation of the class.

        Returns:
            str: The string representation of the class.
        """
        return f"""AnalysisParameters (
    Max Deformation Analysis:
        Enabled: {self.max_deformation_analysis}
        Input: {self.max_deformation_input}
        Widget: {self.max_deformation_widget}

    Stress Analysis:
        Enabled: {self._stress_analysis}
        Widget: {self._stress_widget}
)"""

    def enable_max_deformation_analysis(
            self,
            widget: QWidget,
            input_list: Optional[List[int | np.ndarray]]
    ) -> None:
        """Enables the maximum deformation analysis 
        and sets the points to analyse and the widget to display the results in.

        Args:
            widget (MSRDeformationAnalysisWidget): The widget to display the results in.
            input_list (Optional[List[int  |  np.ndarray]]): The list of points to analyse.
                If the selection mode of the widget is ALL, this parameter can be None.

        Raises:
            ValueError: If no input list is provided and the selection mode of the widget is not ALL.
        """
        if input_list is None and not \
                widget.get_mode() == widget.SelectionMode.ALL:
            raise ValueError(
                "No input list provided for max deformation analysis.")

        self.max_deformation_analysis = True
        self.max_deformation_widget = widget
        self.max_deformation_input = input_list

    def disable_max_deformation_analysis(self) -> None:
        """Disables the maximum deformation analysis and resets the corresponding parameters.
        """
        self.max_deformation_analysis = False
        self.max_deformation_input = None
        self.max_deformation_widget = None

    def enable_stress_analysis(self, widget: QWidget) -> None:
        if widget is None:
            raise ValueError("Widget cannot be None")
        if not hasattr(widget, "set_min") or not callable(widget.set_min) \
                or not hasattr(widget, "set_max") or not callable(widget.set_max):
            raise ValueError("widget has not the necessary methods")

        self._stress_analysis = True
        self._stress_widget = widget

    def disable_stress_analysis(self) -> None:
        self._stress_analysis = False
        self._stress_widget = None

    @property
    def stress_analysis(self) -> bool:
        return self._stress_analysis

    @property
    def stress_widget(self) -> QWidget:
        if not self.stress_analysis:
            raise ValueError(
                "access to stress_widget where stress_analysis is deactivated")
        return self._stress_widget
