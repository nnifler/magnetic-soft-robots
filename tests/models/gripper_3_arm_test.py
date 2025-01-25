import unittest
import Sofa
import Sofa.Simulation
from src import Config, sofa_instantiator


class TestGripper3Arm(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Called once before all the tests in the class"""
        Config.set_test_env()
        Config.set_model('gripper_3_arm', 1)

        cls.root = Sofa.Core.Node("root")
        sofa_instantiator.createScene(cls.root)
        Sofa.Simulation.init(cls.root)

        cls.elastic_object = cls.root.getChild('object')
        cls.visu = cls.elastic_object.getChild('VisualModel')
        cls.ogl = cls.visu.getObject('model')
        cls.mech_obj = cls.elastic_object.getObject('dofs')
        cls.topo = cls.elastic_object.getObject('topo')

    def setUp(self):
        """Called before each test"""
        Sofa.Simulation.reset(self.root)

    def test_volume_mesh(self):
        # Extracted from beam.msh (first line under $Nodes)
        ref_amount_nodes = 1441
        # Extracted from beam.msh (line beginning with 3 in $Elements)
        ref_amount_tetras = 4203

        self.assertEqual(len(self.mech_obj.position.value), ref_amount_nodes)
        self.assertEqual(len(self.topo.tetrahedra.value), ref_amount_tetras)

    def test_surface_mesh(self):
        # Extracted from beam.msh (first line under $Nodes)
        ref_amount_nodes = 1441
        # Extracted from beam.msh (first line under $Elements)
        ref_amount_faces = 2612

        self.assertEqual(len(self.ogl.position.value), ref_amount_nodes)
        self.assertEqual(len(self.ogl.triangles.value), ref_amount_faces)

    def test_volume_mesh_simulation(self):
        # Extracted from beam.msh (first line under $Nodes)
        ref_amount_nodes = 1441
        # Extracted from beam.msh (line beginning with 3 in $Elements)
        ref_amount_tetras = 4203

        for _ in range(10):
            Sofa.Simulation.animate(self.root, self.root.dt.value)
            self.assertEqual(
                len(self.mech_obj.position.value), ref_amount_nodes)
            self.assertEqual(len(self.topo.tetrahedra.value),
                             ref_amount_tetras)

    def test_surface_mesh_simulation(self):
        # Extracted from beam.msh (first line under $Nodes)
        ref_amount_nodes = 1441
        # Extracted from beam.msh (first line under $Elements)
        ref_amount_faces = 2612

        for _ in range(10):
            Sofa.Simulation.animate(self.root, self.root.dt.value)
            self.assertEqual(len(self.ogl.position.value), ref_amount_nodes)
            self.assertEqual(len(self.ogl.triangles.value), ref_amount_faces)

    def test_volume_to_surface_link(self):
        for i, pos in enumerate(self.ogl.position.value):
            self.assertAlmostEqual(
                pos[0], self.mech_obj.position.value[i][0],
                msg=f"Position {i} ({pos}) in surface mesh is not the same as position {i} in volume mesh ({self.mech_obj.position.value[i]})"
            )
            self.assertAlmostEqual(
                pos[1], self.mech_obj.position.value[i][1],
                msg=f"Position {i} ({pos}) in surface mesh is not the same as position {i} in volume mesh ({self.mech_obj.position.value[i]})"
            )
            self.assertAlmostEqual(
                pos[2], self.mech_obj.position.value[i][2],
                msg=f"Position {i} ({pos}) in surface mesh is not the same as position {i} in volume mesh ({self.mech_obj.position.value[i]})"
            )

    def test_volume_to_surface_link_simulation(self):
        for _ in range(10):
            Sofa.Simulation.animate(self.root, self.root.dt.value)
            for i, pos in enumerate(self.ogl.position.value):
                self.assertAlmostEqual(
                    pos[0], self.mech_obj.position.value[i][0],
                    msg=f"Position {i} ({pos}) in surface mesh is not the same as position {i} in volume mesh ({self.mech_obj.position.value[i]})"
                )
                self.assertAlmostEqual(
                    pos[1], self.mech_obj.position.value[i][1],
                    msg=f"Position {i} ({pos}) in surface mesh is not the same as position {i} in volume mesh ({self.mech_obj.position.value[i]})"
                )
                self.assertAlmostEqual(
                    pos[2], self.mech_obj.position.value[i][2],
                    msg=f"Position {i} ({pos}) in surface mesh is not the same as position {i} in volume mesh ({self.mech_obj.position.value[i]})"
                )

    @classmethod
    def tearDownClass(self) -> None:
        """Called once after all tests in the class"""
        Config.reset()


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestGripper3Arm,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
