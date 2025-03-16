"""Implementation of the Stress Analyzer, a class responsible for the von Mises stress analysis. It updates the associated GUI component as well."""
from typing import Any


import Sofa
import numpy as np

from src import AnalysisParameters, ElasticObject


class StressAnalyzer(Sofa.Core.Controller):
    """Analyzer responsible for the von Mises stress analysis. 
    Updates max_stress and min_stress on each step.
    Is a subclass of Sofa.Core.Controller.
    """

    def __init__(self, elastic_object: ElasticObject, parameters: AnalysisParameters) -> None:
        """Builds the Stress Analyzer.

        Args:
            elastic_object (ElasticObject): The ElasticObject which needs to be analyzed.
            parameters (AnalysisParameters): The parameters of the stress analysis.

        Raises:
            ValueError: If elastic_object or parameters are None.
        """
        super().__init__()

        if elastic_object is None or parameters is None:
            raise ValueError("provided argument is None")

        self._elastic_object = elastic_object

        self._analyze = parameters.stress_analysis
        self._widget = None
        if self._analyze:
            self._widget = parameters.stress_widget

        self.max_stress = -np.inf
        self.min_stress = np.inf

        self._callpoint = parameters.callpoint

    # override -> no snake case
    def onAnimateBeginEvent(self, _: Any) -> None:
        """Overrides the onAnimateBeginEvent method executed before each animation step.

        Args:
            _ (Any): the (unused) event
        """
        if not self._analyze:
            return

        stress_values = self._elastic_object.FEM_force_field.vonMisesPerNode.value
        stress_values = np.array(stress_values)

        cur_max = stress_values.max()
        cur_min = stress_values.min()

        if cur_max > self.max_stress:
            self.max_stress = cur_max
            self._callpoint.send((
                "stress_max",
                [self.max_stress],
            ))
            # max stress alert check
        if cur_min < self.min_stress:
            self.min_stress = cur_min
            self._callpoint.send((
                "stress_min",
                [self.max_stress],
            ))

        return
