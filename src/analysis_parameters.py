"""This module contains the class that hold all parameters important for the analysis."""

from typing import List, Optional
import numpy as np


class AnalysisParameters:
    """Class that holds all parameters important for the analysis"""

    def __init__(self):
        """Initializes the class with every analysis disabled.
        """
        self.max_deformation_analysis = False
        self.max_deformation_input = None
        self.max_deformation_widget = None
        self.stress_analysis = False
        self.stress_widget = None

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
        Enabled: {self.stress_analysis}
        Widget: {self.stress_widget}
)"""

    # The parameter widget has no type hint,
    # as classes from gui cannot be imported in src (circular import).
    # The file also cannot be moved to gui, as it is used in src.
    # If anyone has a better solution for this, feel free to change it.
    def set_max_deformation_parameters(
            self,
            widget,
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
        self.max_deformation_analysis = True
        self.max_deformation_widget = widget

        if input_list is None and not \
                self.max_deformation_widget.get_mode() == widget.SelectionMode.ALL:
            raise ValueError(
                "No input list provided for max deformation analysis.")
        self.max_deformation_input = input_list

    def disable_max_deformation_analysis(self) -> None:
        """Disables the maximum deformation analysis and resets the corresponding parameters.
        """
        self.max_deformation_analysis = False
        self.max_deformation_input = None
        self.max_deformation_widget = None
