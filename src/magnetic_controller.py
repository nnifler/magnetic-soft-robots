"""This module contains the MagneticController class that is responsible for calculating and 
changing the magnetic forces acting on the nodes of the elastic object during the simulation.
"""

import math
from typing import Tuple
from scipy.spatial.transform import Rotation
import numpy as np

import Sofa

from . import ElasticObject, MaterialLoader, Config


MU0 = (4 * np.pi) / np.pow(10, 7)  # Permeability (H/m)


class MagneticController(Sofa.Core.Controller):
    """This class is responsible for calculating and changing the magnetic forces 
    acting on the nodes of the elastic object during the simulation."""

    @staticmethod
    def _projection_from(axis: str, vec: np.ndarray) -> np.ndarray:
        """Projects the 3d vector to a 2d vector by ignoring the given axis.

        Args:
            axis (str): The axis that is ignored.
            vec (np.ndarray): The 3d vector that is projected.

        Raises:
            ValueError: If the axis is not a string or is not 'x', 'y' or 'z'.

        Returns:
            np.ndarray: The projected 2d vector.
        """
        proj = {
            'x': lambda x: x[1:],
            'y': lambda x: [x[0], -x[2]],
            'z': lambda x: x[:2]
        }
        if not isinstance(axis, str) or axis not in 'xyz':
            raise ValueError(
                f"Invalid axis!!! Got {axis}, should be string x, y, or z.")

        return proj[axis](vec)

    @staticmethod
    def _normal(cur_positions: np.ndarray,
                tetrahedron: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Calculates the normal of the surface defined by the 
        first three points of the given tetrahedron.

        Args:
            cur_positions (np.ndarray): Array that maps the point inidices 
            to the current positions in the simulation.
            tetrahedron (np.ndarray): Array that contains all point indices of the tetrahedron.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray]: The normal of the surface, 
            the first vector of the tetrahedron and the second vector of the tetrahedron.
        """
        vec1 = cur_positions[tetrahedron[1]] - cur_positions[tetrahedron[0]]
        vec2 = cur_positions[tetrahedron[2]] - cur_positions[tetrahedron[0]]
        cross = np.cross(vec1, vec2)
        return (cross / np.linalg.norm(cross)), vec1, vec2

    @staticmethod
    def calculate_angle(vec1: np.ndarray, vec2: np.ndarray, axis: str) -> float:
        """Calculates the angle between two 3d vectors along the given axis.

        Args:
            vec1 (np.ndarray): The first 3d vector.
            vec2 (np.ndarray): The second 3d vector.
            axis (str): The axis the angle is calculated for.

        Returns:
            float: The angle between the two vectors.
        """
        projected_vector1 = MagneticController._projection_from(axis, vec1)
        projected_vector2 = MagneticController._projection_from(axis, vec2)

        angle = math.atan2(
            np.dot(projected_vector1, np.array(
                [projected_vector2[1], -1*projected_vector2[0]])),
            np.dot(projected_vector1, projected_vector2)
        )
        return angle if not math.isnan(angle) else 0

    @staticmethod
    def calculate_rotation(source: np.ndarray, destination: np.ndarray) -> Rotation:
        """Calculates the rotation between two 3d vectors. 
        Applying the result to the source will result in the destination.

        Args:
            source (np.ndarray): The first 3d vector.
            destination (np.ndarray): The second 3d vector.

        Returns:
            Rotation: The rotation that is needed to rotate the source to the destination.
        """
        if np.isclose(source, destination).all():
            return Rotation.from_euler('x', 0)
        if np.isclose(source, -1 * destination).all():
            source = Rotation.from_euler(
                'xyz', [0.000000001*np.pi]*3).apply(source)

        normalized_source = (source / np.linalg.norm(source)).reshape(3)
        normalized_destination = (
            destination / np.linalg.norm(destination)).reshape(3)
        normal = np.cross(normalized_source, normalized_destination)
        dot_product = np.dot(normalized_source, normalized_destination)
        normal_length = np.linalg.norm(normal)
        kmat = np.array([[0, -normal[2], normal[1]], [normal[2],
                        0, -normal[0]], [-normal[1], normal[0], 0]])
        rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * \
            ((1 - dot_product) / (normal_length ** 2))

        return Rotation.from_matrix(rotation_matrix)

    def __init__(self, elastic_object: ElasticObject, material_loader: MaterialLoader) -> None:
        """Initializes the Magnetic Controller.

        Args:
            elastic_object (ElasticObject): The elastic_object that is modeled.
            material_loader (MaterialLoader): The material_loader that is used to update the material values.
        """
        # Call init of Base class (required)
        super().__init__()

        # Process parameters
        self._elastic_object = elastic_object
        self._material_loader = material_loader

        # Get list of the nodes of all tetrahedra
        self._tetrahedra = np.array(elastic_object.mesh.tetrahedra.value)
        self._rotations = []
        self._volume = 0
        # Get list of the positions of all nodes
        cur_positions = np.array(elastic_object.mesh.position.value)

        self._num_nodes = len(cur_positions)

        for tetrahedron in self._tetrahedra:
            # Calculate the normal of the tetrahedrons face formed by the first 3 nodes
            normal, vec1, vec2 = self._normal(cur_positions, tetrahedron)

            # Initial direction of the magnetic dipole moment
            initial = Config.get_initial_dipole_moment()

            r = self.calculate_rotation(normal, initial)
            self._rotations.append(r)

            vec3 = cur_positions[tetrahedron[3]] - \
                cur_positions[tetrahedron[0]]
            self._volume += abs(np.dot(vec1, np.cross(vec2, vec3))) / 6

    def onAnimateBeginEvent(self, _):
        """Function that is automatically called at the beginning of the Sofa animation step.
        """

        # first of all, update material values
        self._material_loader.update_elastic_object()
        # TODO: for LINK, also update magnetic field etc; similar class maybe?

        # Get the current positions of all nodes
        cur_positions = np.array(self._elastic_object.mech_obj.position.value)
        force_defined_at = [False] * self._num_nodes

        for index, tetrahedron in enumerate(self._tetrahedra):
            # Calculate the normal of the tetrahedrons face formed by the first 3 nodes
            normal = self._normal(cur_positions, tetrahedron)[0]

            # Calculate the orientation of the magnetic dipole moment
            orientation = self._rotations[index].apply(normal)

            for node in tetrahedron:
                if not force_defined_at[node]:
                    # TO DO: check if volume per node is relevant here
                    dipole_moment = Config.get_remanence().T * self._volume / MU0

                    m = dipole_moment * orientation
                    torque = np.cross(m, Config.get_b_field())
                    self._elastic_object.vertex_forces[node].forces = [torque]

                    force_defined_at[node] = True
