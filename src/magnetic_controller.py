import Sofa
from src.elastic_body import ElasticObject
import numpy as np
from scipy.spatial.transform import Rotation
import src.config as config


MU0 = (4 * np.pi) / np.pow(10, 7)

class MagneticController(Sofa.Core.Controller):
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
        for tetrahedron in self._tetrahedra:
            # Calculate the normal of the tetrahedrons face formed by the first 3 nodes
            vec1 = cur_positions[tetrahedron[1]] - cur_positions[tetrahedron[0]]
            vec2 = cur_positions[tetrahedron[2]] - cur_positions[tetrahedron[0]]
            cross = np.cross(vec1, vec2)
            normal = cross / np.linalg.norm(cross)

            # Initial direction of the magnetic dipole moment
            initial = np.array([0,-1,0])

            # TODO: Fix exception when normal = (x,0,0) or normal = (0,0,x)
            # TODO: Fix error that the angles are in the wrong direction (when they should be negative)
            # Calculate the angle between the normal and the initial direction in x direction 
            angle_x = np.arccos(np.dot(normal[1:], initial[1:]) / (np.linalg.norm(normal[1:]) * np.linalg.norm(initial[1:])))
            rot_x = Rotation.from_euler('x', angle_x, degrees=False)

            # Calculate the angle between the in x direction rotated normal and the initial direction in z direction
            normal_rot = rot_x.apply(normal)
            angle_z = np.arccos(np.dot(normal_rot[:2], initial[:2]) / (np.linalg.norm(normal_rot[:2]) * np.linalg.norm(initial[:2])))

            # Create a Rotation object and append it to the _rotations list
            rot = Rotation.from_euler('xyz', [angle_x, 0, angle_z], degrees=False)
            self._rotations.append(rot)
            
            vec3 = cur_positions[tetrahedron[3]] - cur_positions[tetrahedron[0]]
            self._volume += abs(np.dot(vec1, np.cross(vec2, vec3))) / 6

        self._volume_per_node = self._volume / len(cur_positions)


    def onAnimateBeginEvent(self, event):
        """
        Function that is automatically called every Sofa animation step
        """
        # Get the current positions of all nodes
        cur_positions = np.array(self._elastic_object.mech_obj.position.value)
        already_assigned = []
        for id, tetrahedron in enumerate(self._tetrahedra):
            # Calculate the normal of the tetrahedrons face formed by the first 3 nodes
            vec1 = cur_positions[tetrahedron[1]] - cur_positions[tetrahedron[0]]
            vec2 = cur_positions[tetrahedron[2]] - cur_positions[tetrahedron[0]]
            cross = np.cross(vec1, vec2)
            normal = cross / np.linalg.norm(cross)

            # Calculate the orientation of the magnetic dipole moment
            orientation = self._rotations[id].apply(normal)
            
            for node in tetrahedron:
                if node not in already_assigned:
                    force = config.REMANENCE * self._volume_per_node / MU0
                    print(force * orientation)
                    m = force * orientation
                    self._elastic_object.vertex_forces[0].forces = f"{m[0]} {m[1]} {m[2]}"
                    
