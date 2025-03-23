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

"""This module contains the class that hold all parameters important for the analysis."""
from multiprocessing.connection import Connection
from enum import Enum
from typing import List, Optional
import numpy as np


class AnalysisParameters:
    """Class that holds all parameters important for the analysis"""

    class SelectionMode(Enum):
        """Enum class for the different ways to select points."""
        INDICES = 0
        COORDINATES = 1
        ALL = 2

    def __init__(self, callpoint: Connection):
        """Initializes the class with every analysis disabled.

        Args:
            callpoint (Connection): A pipe for communicating with the QWidget.
            Should always be set on initialization, as it will be required independent of analysis type.
        """
        if callpoint is None:
            raise ValueError(
                "callpoint must not be None. Necessary for process communication")

        self.max_deformation_analysis = False
        self.max_deformation_input = None
        self.max_deformation_mode = None

        self._stress_analysis = False

        self.callpoint = callpoint

    def __repr__(self) -> str:
        """Returns a string representation of the class.

        Returns:
            str: The string representation of the class.
        """
        return f"""AnalysisParameters (
    Max Deformation Analysis:
        Enabled: {self.max_deformation_analysis}
        Input: {self.max_deformation_input}
        Mode: {self.max_deformation_mode}

    Stress Analysis:
        Enabled: {self._stress_analysis}
)"""

    def enable_max_deformation_analysis(
            self,
            mode: SelectionMode,
            input_list: Optional[List[int | np.ndarray]]
    ) -> None:
        """Enables the maximum deformation analysis 
        and sets the points to analyse and the widget to display the results in.

        Args:
            mode (SelectionMode): Mode how the points are selected for analysis.
            input_list (Optional[List[int  |  np.ndarray]]): The list of points to analyse.
                If the selection mode is ALL, this parameter can be None.

        Raises:
            ValueError: If no input list is provided and the selection mode is not ALL.
        """
        if input_list is None and not \
                mode == self.SelectionMode.ALL:
            raise ValueError(
                "No input list provided for max deformation analysis.")

        self.max_deformation_analysis = True
        self.max_deformation_mode = mode
        self.max_deformation_input = input_list

    def disable_max_deformation_analysis(self) -> None:
        """Disables the maximum deformation analysis and resets the corresponding parameters.
        """
        self.max_deformation_analysis = False
        self.max_deformation_input = None
        self.max_deformation_mode = None

    def enable_stress_analysis(self) -> None:
        """Enables the stress analysis in the parameters. 
        stress_analysis will return True until disabled.
        The user is responsible for enabling stress analysis in the Config file as well.
        """
        self._stress_analysis = True

    def disable_stress_analysis(self) -> None:
        """Disables the stress Analysis.
        stress_analysis will return False.
        """
        self._stress_analysis = False

    @property
    def stress_analysis(self) -> bool:
        """Whether the Stress Analysis is enabled.

        Returns:
            bool: True iff enable_stress_analysis has been called before, 
            without calls to disable_stress_analysis inbetween. 
        """
        return self._stress_analysis
