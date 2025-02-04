"""This module contains the SimulationAnalyser class, 
which is used to analyse the simulation results."""

from typing import List
import numpy as np

import Sofa


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
        return np.argmin(distances)

    def calculate_deformation(self, points: List[int]) -> np.ndarray:
        """Calculates the maximum and minimum deformation of the model
        compared to the state of the model when the Analyser was initialized.
        Only the given points are considered when calculating the maximum and minimum.

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
        for point in points:
            if point >= len(self.initial_positions):
                raise ValueError(f"Point {point} is not part of the model.")

        current_positions = self.mech_obj.position.value
        deformations = np.stack(list(map(
            lambda point: current_positions[point] - self.initial_positions[point], points)))

        maxima = deformations.max(axis=0)
        minima = deformations.min(axis=0)

        return np.stack((maxima, minima))

    def calculate_maximum_deformation(self, points: List[int]) -> np.ndarray:
        """Calculates the maximum deformation of the model
        compared to the state of the model when the Analyser was initialized.
        Only the given points are considered when calculating the maximum.

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
        return self.calculate_deformation(points)[0]

    def calculate_minimum_deformation(self, points: List[int]) -> np.ndarray:
        """Calculates the minimum deformation of the model
        compared to the state of the model when the Analyser was initialized.
        Only the given points are considered when calculating the minimum.

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
        return self.calculate_deformation(points)[1]
