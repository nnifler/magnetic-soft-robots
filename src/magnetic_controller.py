import Sofa

from src.elastic_body import ElasticObject
from src.material_loader import MaterialLoader
import src.config as config

import numpy as np
from scipy.spatial.transform import Rotation
from typing import Tuple
import math


MU0 = (4 * np.pi) / np.pow(10, 7) # Permeability (H/m)

class MagneticController(Sofa.Core.Controller):

    @staticmethod
    def _projection_from(axis: str, vec: np.ndarray) -> np.ndarray:
        """
        Projects the 3d vector to a 2d vector by ignoring the given axis.

        Arguments:
        - axis: The axis that is ignored
        - vec: The 3d vector that is projected
        """
        proj = {
            'x': lambda x: x[1:], 
            'y': lambda x: [x[0], -x[2]],
            'z': lambda x: x[:2]
        }
        if type(axis) != str or axis not in 'xyz':
            raise ValueError(f"Invalid axis!!! Got {axis}, should be string x, y, or z.")
        
        return proj[axis](vec)

    @staticmethod
    def _normal(cur_positions: np.ndarray, tetrahedron: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculates the normal of the surface defined by the first three points of the given tetrahedron.

        Arguments:
        - cur_positions: Array that maps the point inidices to the current positions in the simulation
        - tetrahedron: Array contains all point indices of the tetrahedron
        """
        vec1 = cur_positions[tetrahedron[1]] - cur_positions[tetrahedron[0]]
        vec2 = cur_positions[tetrahedron[2]] - cur_positions[tetrahedron[0]]
        cross = np.cross(vec1, vec2)
        return (cross / np.linalg.norm(cross)), vec1, vec2

    @staticmethod
    def calculate_angle(vec1: np.ndarray, vec2: np.ndarray, axis: str) -> float:
        """
        Calculates the angle between two 3d vectors along the given axis.

        Arguments:
        - vec1: The first 3d vector
        - vec2: The second 3d vector
        - axis: The axis the angle is calculated for
        """
        projected_vector1 = MagneticController._projection_from(axis, vec1)
        projected_vector2 = MagneticController._projection_from(axis, vec2)

        angle = math.atan2(
            np.dot(projected_vector1, np.array([projected_vector2[1], -1*projected_vector2[0]])),
            np.dot(projected_vector1, projected_vector2)
        )
        return angle if not math.isnan(angle) else 0

    @staticmethod
    def calculate_rotation(source: np.ndarray, destination: np.ndarray) -> Rotation:
        """
        Calculates the rotation between two 3d vectors. Applying the result to the source will result in the destination. 

        Arguments:
        - source: The first 3d vector
        - destination: The second 3d vector
        """
        if np.isclose(source, destination).all(): return Rotation.from_euler('x', 0)
        if np.isclose(source, -1 * destination).all(): 
            source = Rotation.from_euler('xyz', [0.000000001*np.pi]*3).apply(source)

        normalized_source = (source / np.linalg.norm(source)).reshape(3)
        normalized_destination = (destination / np.linalg.norm(destination)).reshape(3)
        normal = np.cross(normalized_source, normalized_destination)
        dot_product = np.dot(normalized_source, normalized_destination)
        normal_length = np.linalg.norm(normal)
        kmat = np.array([[0, -normal[2], normal[1]], [normal[2], 0, -normal[0]], [-normal[1], normal[0], 0]])
        rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - dot_product) / (normal_length ** 2))

        return Rotation.from_matrix(rotation_matrix)


    def __init__(self, elastic_object: ElasticObject, material_loader: MaterialLoader):
        """
        Initializes the Magnetic Controller
        
        Arguments:
        - elastic_object -- the elastic_object that is modeled
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
            initial = config.INIT

            r = self.calculate_rotation(normal, initial)
            self._rotations.append(r)

            vec3 = cur_positions[tetrahedron[3]] - cur_positions[tetrahedron[0]]
            self._volume += abs(np.dot(vec1, np.cross(vec2, vec3))) / 6

        self._volume_per_node = self._volume / self._num_nodes


    def onAnimateBeginEvent(self, _):
        """
        Function that is automatically called every Sofa animation step
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
                    dipole_moment = config.REMANENCE.T * self._volume_per_node / MU0

                    m = dipole_moment * orientation
                    torque = np.cross(m, config.B_FIELD)
                    self._elastic_object.vertex_forces[node].forces = [[torque[0], torque[1], torque[2]]]

                    force_defined_at[node] = True
