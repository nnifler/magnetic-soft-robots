"""This module contains the SimulationAnalyser class, 
which is used to analyse the simulation results."""

from typing import List
import numpy as np

import Sofa

from gui.msr_analysis_widgets import MSRDeformationAnalysisWidget


class SimulationAnalyser:
    """This class is used to analyse the simulation results."""

    def __init__(self, root: Sofa.Core.Node) -> None:
        """Initializes the SimulationAnalyser with the given root node.

        Args:
            root (Sofa.Core.Node): The root node of the simulation to analyse.
        """
        self.root = root
        self.elastic_object = self.root.getChild('object')
        self.mech_obj = self.elastic_object.getObject('dofs')

        # Copy is needed because the array would otherwise change during simulation
        self.initial_positions = self.mech_obj.position.value.copy()

        self.maximum_deformation_array = np.ones((
            len(self.initial_positions), 3)) * -np.inf
        self.minimum_deformation_array = np.ones((
            len(self.initial_positions), 3)) * np.inf

    def calculate_nearest_node(self, point: np.ndarray) -> int:
        """Calculates the nearest node in the model to the given point.
        This function uses the state of the model when the Analyser was initialized.

        Args:
            point (np.ndarray): The point to calculate the nearest node for.

        Raises:
            ValueError: If the point does not have the shape [x,y,z].

        Returns:
            int: The index of the nearest node.
        """
        if point.shape != (3,):
            raise ValueError("Point must have the shape [x,y,z].")
        distances = np.linalg.norm(self.initial_positions - point, axis=1)
        return int(np.argmin(distances))

    def update_deformation(self) -> None:
        """Updates the maximum and minimum deformation of the model
        with the current state of the model.
        """
        current_positions = self.mech_obj.position.value
        self.maximum_deformation_array = np.maximum(
            self.maximum_deformation_array, current_positions - self.initial_positions)
        self.minimum_deformation_array = np.minimum(
            self.minimum_deformation_array, current_positions - self.initial_positions)

    def calculate_deformation(self, points: List[int] = None) -> np.ndarray:
        # TODO: Update Docstring
        """Calculates the maximum and minimum deformation of the model
        compared to the state of the model when the Analyser was initialized.
        Only the given points are considered when calculating the maximum and minimum.
        This method uses the state from when last update_deformation was called.

        Args:
            points (List[int]): The points to calculate the deformation for.

        Raises:
            ValueError: If a given point is not part of the model.

        Returns:
            np.ndarray: The maximum and minimum deformation. The array has the following shape:
            ```
            [[max_x, max_y, max_z],
             [min_x, min_y, min_z]]
            ```
        """
        max_deformations = self.maximum_deformation_array
        min_deformations = self.minimum_deformation_array
        if points is not None:
            for point in points:
                if point >= len(self.initial_positions):
                    raise ValueError(
                        f"Point {point} is not part of the model.")

            max_deformations = self.maximum_deformation_array[points]
            min_deformations = self.minimum_deformation_array[points]

        maxima = max_deformations.max(axis=0)
        minima = min_deformations.min(axis=0)
        maxima_index = max_deformations.argmax(axis=0)
        minima_index = min_deformations.argmin(axis=0)
        if points is not None:
            maxima_index = np.array(points)[maxima_index]
            minima_index = np.array(points)[minima_index]

        return np.stack((maxima, minima)), np.stack((maxima_index, minima_index))

    def calculate_maximum_deformation(self, points: List[int] = None) -> np.ndarray:
        """Calculates the maximum deformation of the model
        compared to the state of the model when the Analyser was initialized.
        Only the given points are considered when calculating the maximum.
        This method uses the state from when last update_deformation was called.

        Args:
            points (List[int]): The points to calculate the deformation for.

        Raises:
            ValueError: If a given point is not part of the model.

        Returns:
            np.ndarray: The maximum deformation. The array has the following shape:
            ```
            [max_x, max_y, max_z]
            ```
        """
        return self.calculate_deformation(points)[0][0], self.calculate_deformation(points)[1][0]

    def calculate_minimum_deformation(self, points: List[int] = None) -> np.ndarray:
        """Calculates the minimum deformation of the model
        compared to the state of the model when the Analyser was initialized.
        Only the given points are considered when calculating the minimum.
        This method uses the state from when last update_deformation was called.

        Args:
            points (List[int]): The points to calculate the deformation for.

        Raises:
            ValueError: If a given point is not part of the model.

        Returns:
            np.ndarray: The minimum deformation. The array has the following shape:
            ```
            [min_x, min_y, min_z]
            ```
        """
        return self.calculate_deformation(points)[0][1], self.calculate_deformation(points)[1][1]


class SimulationAnalysisController(Sofa.Core.Controller):
    def __init__(self, root: Sofa.Core.Node, analysis_parameters: dict) -> None:
        super().__init__(root)
        self.root = root
        self.analyser = SimulationAnalyser(root)

        # Max deformation
        self.max_deformation_analysis = analysis_parameters.get(
            "max_deformation_analysis", False)
        self.max_deformation_input = analysis_parameters.get(
            "max_deformation_input", [])
        self.max_deformation_widget: MSRDeformationAnalysisWidget = analysis_parameters.get(
            "max_deformation_widget", None)
        self.max_deformation_mode = self.max_deformation_widget.get_mode(
        ) if self.max_deformation_widget is not None else None
        if self.max_deformation_mode == MSRDeformationAnalysisWidget.SelectionMode.COORDINATES:
            self.max_deformation_input = list(
                map(self.analyser.calculate_nearest_node, self.max_deformation_input))

    def onAnimateBeginEvent(self, _):
        if self.max_deformation_analysis:
            self.analyser.update_deformation()
            try:
                deformation, deformation_indices = None, None
                if self.max_deformation_mode == MSRDeformationAnalysisWidget.SelectionMode.ALL:
                    deformation, deformation_indices = self.analyser.calculate_deformation()
                else:
                    deformation, deformation_indices = self.analyser.calculate_deformation(
                        self.max_deformation_input)
                maximum_indices = np.abs(deformation).argmax(axis=0)
                self.max_deformation_widget.update_results([
                    round(deformation[maximum_indices[0], 0], 6),
                    round(deformation[maximum_indices[1], 1], 6),
                    round(deformation[maximum_indices[2], 2], 6),
                ], [
                    deformation_indices[maximum_indices[0], 0],
                    deformation_indices[maximum_indices[1], 1],
                    deformation_indices[maximum_indices[2], 2],
                ])
            except ValueError as vale:
                self.max_deformation_widget.display_input_error(str(vale))
