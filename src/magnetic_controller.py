import Sofa

from src.elastic_body import ElasticObject
from src.SceneBuilder import SceneBuilder
import src.config as config

import numpy as np
from scipy.spatial.transform import Rotation
from typing import Callable
import math


MU0 = (4 * np.pi) / np.pow(10, 7)

class MagneticController(Sofa.Core.Controller):

    def _normal(self, cur_positions: np.ndarray, tetrahedron: np.ndarray):
        vec1 = cur_positions[tetrahedron[1]] - cur_positions[tetrahedron[0]]
        vec2 = cur_positions[tetrahedron[2]] - cur_positions[tetrahedron[0]]
        cross = np.cross(vec1, vec2)
        return (cross / np.linalg.norm(cross)), vec1, vec2


    def _calculate_angle(self, v1: np.ndarray, v2: np.ndarray, subscript: Callable[[np.ndarray], np.ndarray]) -> float:
        """Calculate the angle between v1 and v2 projected from the direction excluded in the subscript"""
        p1, p2 = subscript(v1), subscript(v2)
        def rot(v):
            return np.array([v[1], -1*v[0]])

        angle = math.atan2(
            np.dot(p1, rot(p2)),
            np.dot(p1, p2)
        )
        return angle if not math.isnan(angle) else 0


    def _calculate_rotation(self, normal: np.ndarray, initial_dipole_orientation: np.ndarray):
        # Calculate the angle between the normal and the initial direction in x direction
        angle_x = self._calculate_angle(normal, initial_dipole_orientation, lambda x: x[1:])
        rot_x = Rotation.from_euler('x', angle_x, degrees=False)

        # Calculate the angle between the in x direction rotated normal and the initial direction in z direction
        normal_rot = rot_x.apply(normal)

        angle_y = self._calculate_angle(normal_rot, initial_dipole_orientation, lambda x: x[::2])
        rot_y = Rotation.from_euler('y', angle_y, degrees=False)
        normal_rot = rot_y.apply(normal_rot)

        angle_z = self._calculate_angle(normal_rot, initial_dipole_orientation, lambda x: x[:2])
        return Rotation.from_euler('xyz', [angle_x, angle_y, angle_z], degrees=False)


    def __init__(self, elastic_object: ElasticObject):
        """
        Initializes the Magnetic Controller
        
        Arguments:
        elastic_object -- the elastic_object that is modeled
        """
        # Call init of Base class (required)
        Sofa.Core.Controller.__init__(self)

        # Process parameters
        self._elastic_object = elastic_object

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

            r = self._calculate_rotation(normal, initial)
            self._rotations.append(r)
            print(r.as_euler('xyz'), "r")

            vec3 = cur_positions[tetrahedron[3]] - cur_positions[tetrahedron[0]]
            self._volume += abs(np.dot(vec1, np.cross(vec2, vec3))) / 6

        self._volume_per_node = self._volume / self._num_nodes

        print(self._volume)


    def onAnimateBeginEvent(self, event):
        """
        Function that is automatically called every Sofa animation step
        """
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
                    dipole_moment = config.REMANENCE * self._volume_per_node / MU0
                    #print(force * orientation)
                    #print(self._elastic_object.vertex_forces[0].forces
                    m = dipole_moment * orientation
                    # print(config.B_FIELD.shape, m.shape)
                    torque = np.cross(m, config.B_FIELD)
                    # print(type(m), m)
                    self._elastic_object.vertex_forces[node].forces = f"{torque[0]} {torque[1]} {torque[2]}"

                    force_defined_at[node] = True
