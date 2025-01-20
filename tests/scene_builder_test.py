import unittest
import numpy as np

import Sofa

from src.SceneBuilder import SceneBuilder
from src.config import Config
from random import choices
import string

class TestSceneBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Config.set_plugin_list(['Sofa.Component.Collision.Detection.Algorithm',
            'Sofa.Component.Collision.Detection.Intersection',
            'Sofa.Component.Collision.Geometry',
            'Sofa.Component.Collision.Response.Contact',
            'Sofa.Component.Constraint.Projective',
            'Sofa.Component.IO.Mesh',
            'Sofa.Component.LinearSolver.Iterative',
            'Sofa.Component.Mapping.Linear',
            'Sofa.Component.Mass',
            'Sofa.Component.ODESolver.Backward',
            'Sofa.Component.SolidMechanics.FEM.Elastic',
            'Sofa.Component.StateContainer',
            'Sofa.Component.Topology.Container.Dynamic',
            'Sofa.Component.Visual',
            'Sofa.GL.Component.Rendering3D',
            'Sofa.Component.AnimationLoop',
            'Sofa.Component.LinearSolver.Direct',
            'Sofa.Component.Constraint.Lagrangian.Correction',
            'Sofa.Component.Topology.Mapping',
            'Sofa.Component.MechanicalLoad'
        ])

    def test_gravity(self):
        ref_gravity = np.random.uniform(0,100,3)
        old_ug = Config.get_use_gravity()
        Config.set_external_forces(
            True,
            Config.get_gravity_vec(),
            Config.get_magnetic_force(),
            Config.get_magnetic_dir(),
            Config.get_initial_dipole_moment()
        )

        root = Sofa.Core.Node("root")
        SceneBuilder(root, gravity_vec=ref_gravity)
        
        for actual, ref in zip(root.gravity.value, ref_gravity):
            self.assertAlmostEqual(actual, ref)

        Config.set_external_forces(
            old_ug,
            Config.get_gravity_vec(),
            Config.get_magnetic_force(),
            Config.get_magnetic_dir(),
            Config.get_initial_dipole_moment()
        )
    
    def test_gravity_exceptional(self):
        root = Sofa.Core.Node("root")

        invalid_vector1 = np.random.uniform(0,100,2)
        invalid_vector2 = np.random.uniform(0,100,(3,1))
        with self.assertRaises(ValueError):
            SceneBuilder(root, gravity_vec=invalid_vector1)
        with self.assertRaises(ValueError):
            SceneBuilder(root, gravity_vec=invalid_vector2)

    def test_no_gravity(self):
        gravity = np.random.uniform(0,100,3)
        old_ug = Config.get_use_gravity()
        Config.set_external_forces(
            False,
            Config.get_gravity_vec(),
            Config.get_magnetic_force(),
            Config.get_magnetic_dir(),
            Config.get_initial_dipole_moment()
        )

        root = Sofa.Core.Node("root")
        SceneBuilder(root, gravity_vec=gravity)
        
        for actual, ref in zip(root.gravity.value, [0,0,0]):
            self.assertAlmostEqual(actual, ref)

        Config.set_external_forces(
            old_ug,
            Config.get_gravity_vec(),
            Config.get_magnetic_force(),
            Config.get_magnetic_dir(),
            Config.get_initial_dipole_moment()
        )

    def test_dt(self):
        ref_dt = np.random.uniform(0,100)

        root = Sofa.Core.Node("root")
        SceneBuilder(root, dt=ref_dt)
        
        self.assertAlmostEqual(root.dt.value, ref_dt)

    def test_dt_exceptional(self):
        root = Sofa.Core.Node("root")

        invalid_dt = np.random.uniform(-100,0)
        with self.assertRaises(ValueError):
            SceneBuilder(root, dt=invalid_dt)
        with self.assertRaises(ValueError):
            SceneBuilder(root, dt=0)

    def test_plugins(self):
        root = Sofa.Core.Node("root")
        SceneBuilder(root)

        for plugin in Config.get_plugin_list():
            self.assertIn(plugin, root.getObject('RequiredPlugin').pluginName.value)

    def test_child(self):
        root = Sofa.Core.Node("root")
        uut = SceneBuilder(root)

        name = ''.join(choices(string.ascii_uppercase + string.digits, k=6))
        uut.create_child(name)

        child = root.getChild(name)
        self.assertIsNotNone(child)

    @classmethod
    def tearDownClass(cls):
        Config.set_plugin_list([""])

def suite() -> unittest.TestSuite: 
    suite = unittest.TestSuite()

    ## Insert new tests here
    tests = [
        TestSceneBuilder,
    ]

    ## Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    ## Add tests to test suite
    suite.addTests(loaded_tests)
    return suite