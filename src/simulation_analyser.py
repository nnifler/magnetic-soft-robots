"""This module contains all classes needed for the analysis of the simulation."""

from typing import List, Tuple
import numpy as np

import Sofa

from src import AnalysisParameters


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
        This function uses the state of the model when the analyser was initialized.

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

    def calculate_deformation(self, points: List[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates the maximum and minimum deformation of the model
        compared to the state of the model when the Analyser was initialized.
        Only the given points are considered when calculating the maximum and minimum.
        This method uses the state from when last update_deformation was called.

        Args:
            points (List[int], optional): The points to calculate the deformation for. 
             If points is None, considers all points of the model. Defaults to None.

        Raises:
            ValueError: If a given point is not part of the model.
            ValueError: If points is an empty list.

        Returns:
            Tuple[np.ndarray, np.ndarray]: The maximum and minimum deformation 
            and the corresponding indices. The arrays have the following shape:
            ```
            [[max_x, max_y, max_z],
             [min_x, min_y, min_z]]
            ```
            ```
            [[max_index_x, max_index_y, max_index_z],
             [min_index_x, min_index_y, min_index_z]]
            ```
        """
        max_deformations = self.maximum_deformation_array
        min_deformations = self.minimum_deformation_array
        if points is not None:
            if points == []:
                raise ValueError("List of points must not be empty.")
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

    def calculate_maximum_deformation(self, points: List[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates the maximum deformation of the model
        compared to the state of the model when the Analyser was initialized.
        Only the given points are considered when calculating the maximum.
        This method uses the state from when last update_deformation was called.

        Args:
            points (List[int], optional): The points to calculate the deformation for. 
             If points is None, considers all points of the model. Defaults to None.

        Raises:
            ValueError: If a given point is not part of the model.

        Returns:
            Tuple[np.ndarray, np.ndarray]: The maximum deformation 
            and the corresponding indices. The arrays have the following shape:
            ```
            [max_x, max_y, max_z]
            ```
            ```
            [max_index_x, max_index_y, max_index_z]
            ```
        """
        return self.calculate_deformation(points)[0][0], self.calculate_deformation(points)[1][0]

    def calculate_minimum_deformation(self, points: List[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates the minimum deformation of the model
        compared to the state of the model when the Analyser was initialized.
        Only the given points are considered when calculating the minimum.
        This method uses the state from when last update_deformation was called.

        Args:
            points (List[int], optional): The points to calculate the deformation for. 
             If points is None, considers all points of the model. Defaults to None.

        Raises:
            ValueError: If a given point is not part of the model.

        Returns:
            Tuple[np.ndarray, np.ndarray]: The minimum deformation 
            and the corresponding indices. The arrays have the following shape:
            ```
            [min_x, min_y, min_z]
            ```
            ```
            [min_index_x, min_index_y, min_index_z]
            ```
        """
        return self.calculate_deformation(points)[0][1], self.calculate_deformation(points)[1][1]


class SimulationAnalysisController(Sofa.Core.Controller):
    """This class is used to perform analysis during the simulation"""

    def __init__(self, root: Sofa.Core.Node, analysis_parameters: AnalysisParameters) -> None:
        """Initializes the SimulationAnalysisController 
        with the given root node and analysis parameters.

        Args:
            root (Sofa.Core.Node): The root node of the simulation.
            analysis_parameters (AnalysisParameters): The analysis parameters.
        """
        super().__init__(root, name="AnalysisController")
        self.root = root
        self.analyser = SimulationAnalyser(root)

        # Max deformation
        self.max_deformation_analysis = analysis_parameters.max_deformation_analysis
        self.max_deformation_input = analysis_parameters.max_deformation_input
        self.max_deformation_widget = analysis_parameters.max_deformation_widget
        if self.max_deformation_widget is not None:
            self.max_deformation_mode = self.max_deformation_widget.get_mode()
            # Convert input to indices if necessary
            if self.max_deformation_mode == self.max_deformation_widget.SelectionMode.COORDINATES:
                self.max_deformation_input = list(
                    map(self.analyser.calculate_nearest_node, self.max_deformation_input))
        else:
            # Not tested right now, should be tested as soon as
            # the controller has to handle multiple analysis types
            self.max_deformation_mode = None

    # Inbuilt function, therfore not in snake case
    def onAnimateBeginEvent(self, _) -> None:
        """Method that is automatically called at the beginning of the Sofa animation step.
        """
        # Perform max deformation analysis
        if self.max_deformation_analysis:
            self.analyser.update_deformation()
            try:
                deformation, deformation_indices = None, None
                if self.max_deformation_mode == self.max_deformation_widget.SelectionMode.ALL:
                    deformation, deformation_indices = self.analyser.calculate_deformation()
                else:
                    # This might raise a ValueError
                    # if e.g. a point in the input is not part of the model
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
