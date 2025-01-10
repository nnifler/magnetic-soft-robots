import Sofa

from src.elastic_body import ElasticObject
from src.material_loader import MaterialLoader
import src.config as config

import numpy as np
from scipy.spatial.transform import Rotation
from typing import Callable
import math


MU0 = (4 * np.pi) / np.pow(10, 7) # Permeability (H/m)

class MagneticController(Sofa.Core.Controller):

    @staticmethod
    def _projection_from(axis: str, vec: np.ndarray): 
        proj = {
            'x': lambda x: x[1:], 
            'y': lambda x: [x[0], -x[2]],
            'z': lambda x: x[:2]
        }
        if type(axis) != str or axis not in 'xyz':
            raise ValueError(f"Invalid axis!!! Got {axis}, should be string x, y, or z.")
        
        return proj[axis](vec)

    @staticmethod
    def _normal(cur_positions: np.ndarray, tetrahedron: np.ndarray):
        vec1 = cur_positions[tetrahedron[1]] - cur_positions[tetrahedron[0]]
        vec2 = cur_positions[tetrahedron[2]] - cur_positions[tetrahedron[0]]
        cross = np.cross(vec1, vec2)
        return (cross / np.linalg.norm(cross)), vec1, vec2

    @staticmethod
    def calculate_angle(v1: np.ndarray, v2: np.ndarray, axis: str) -> float:
        """Calculate the angle between v1 and v2 projected from the direction excluded in the subscript"""
        p1, p2 = MagneticController._projection_from(axis, v1), MagneticController._projection_from(axis, v2)
        def rot(v):
            return np.array([v[1], -1*v[0]])

        angle = math.atan2(
            np.dot(p1, rot(p2)),
            np.dot(p1, p2)
        )
        return angle if not math.isnan(angle) else 0

    @staticmethod
    def calculate_rotation(normal: np.ndarray, initial_dipole_orientation: np.ndarray):

        if np.isclose(normal, initial_dipole_orientation).all(): return Rotation.from_euler('x', 0)
        if np.isclose(normal, -1 * initial_dipole_orientation).all(): 
            normal = Rotation.from_euler('x', 0.000000001*np.pi).apply(normal)

        a = (normal / np.linalg.norm(normal)).reshape(3)
        b = (initial_dipole_orientation / np.linalg.norm(initial_dipole_orientation)).reshape(3)
        v = np.cross(a, b)
        c = np.dot(a, b)
        s = np.linalg.norm(v)
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
        return Rotation.from_matrix(rotation_matrix)


    def __init__(self, elastic_object: ElasticObject, material_loader: MaterialLoader):
        """
        Initializes the Magnetic Controller
        
        Arguments:
        elastic_object -- the elastic_object that is modeled
        """
        # Call init of Base class (required)
        Sofa.Core.Controller.__init__(self)

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

            for vertex in tetrahedron:
                if not force_defined_at[vertex]:
                    dipole_moment = self._elastic_object.remanence * self._volume_per_node / MU0
                    #print(force * orientation)
                    #print(self._elastic_object.vertex_forces[0].forces
                    m = dipole_moment * orientation
                    # print(config.B_FIELD.shape, m.shape)
                    torque = np.cross(m, config.B_FIELD)
                    # print(type(m), m)
                    self._elastic_object.vertex_forces[vertex].forces = [torque]

                    force_defined_at[vertex] = True
