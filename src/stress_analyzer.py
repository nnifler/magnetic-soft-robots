import Sofa
import numpy as np

from src import AnalysisParameters, ElasticObject


class StressAnalyzer(Sofa.Core.Controller):
    def __init__(self, elastic_object: ElasticObject, parameters: AnalysisParameters) -> None:
        super().__init__()

        self._elastic_object = elastic_object
        self._params = parameters
        self.max_stress = -np.inf
        self.min_stress = np.inf

    # override -> no snake case
    def onAnimateBeginEvent(self, _) -> None:
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
