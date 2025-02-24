"""Implementation of the Stress Analyzer, a class responsible for the von Mises stress analysis. It updates the associated GUI component as well."""
from typing import Any

import Sofa
import numpy as np

from src import AnalysisParameters, ElasticObject


class StressAnalyzer(Sofa.Core.Controller):
    """Analyzer responsible for the von Mises stress analysis. 
    Updates max_stress and min_stress on each step.
    """

    def __init__(self, elastic_object: ElasticObject, parameters: AnalysisParameters) -> None:
        super().__init__()

        if elastic_object is None or parameters is None:
            raise ValueError("provided argument is None")

        self._elastic_object = elastic_object
        self._params = parameters

        self.max_stress = -np.inf
        self.min_stress = np.inf

    # override -> no snake case
    def onAnimateBeginEvent(self, _: Any) -> None:
        """Overrides the onAnimateBeginEvent method executed before each animation step.

        Args:
            _ (Any): the (unused) event
        """
        if not self._params.stress_analysis:
            return

        stress_values = self._elastic_object.FEM_force_field.vonMisesPerNode.value
        stress_values = np.array(stress_values)

        cur_max = stress_values.max()
        cur_min = stress_values.min()

        if cur_max > self.max_stress:
            self.max_stress = cur_max
            # update gui
            # max stress alert check
        if cur_min < self.min_stress:
            self.min_stress = cur_min
            # update gui

        return
