import unittest
import numpy as np

import Sofa
import Sofa.Simulation

from src.sofa_instantiator import createScene
from src.config import Config
from src.units.YoungsModulus import YoungsModulus
from src.units.Density import Density
from src.units.Tesla import Tesla

class TestBeam(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Called once before all the tests in the class"""
        Config.set_test_env()
        Config.set_model('beam', 1)
        
        cls.root = Sofa.Core.Node("root")
        createScene(cls.root)
        Sofa.Simulation.init(cls.root)

        cls.elastic_object = cls.root.getChild('object')
        cls.visu = cls.elastic_object.getChild('VisualModel')
        cls.ogl = cls.visu.getObject('model')
        cls.mech_obj = cls.elastic_object.getObject('dofs')
        cls.topo = cls.elastic_object.getObject('topo')

    def setUp(self):
        """Called before each test"""
        Sofa.Simulation.reset(self.root)

    def testVolumeMesh(self):
        ref_amount_nodes = 306 # Extracted from beam.msh (first line under $Nodes)
        ref_amount_tetras = 807 # Extracted from beam.msh (line beginning with 3 in $Elements)

        self.assertEqual(len(self.mech_obj.position.value), ref_amount_nodes)
        self.assertEqual(len(self.topo.tetrahedra.value), ref_amount_tetras)

    def testSurfaceMesh(self):
        ref_amount_nodes = 290 # Extracted from beam.msh (second line under $Nodes)
        ref_amount_faces = 576 # Extracted from beam.msh (first line under $Elements)

        self.assertEqual(len(self.ogl.position.value), ref_amount_nodes)
        self.assertEqual(len(self.ogl.triangles.value), ref_amount_faces)

    def testVolumeMeshSimulation(self):
        ref_amount_nodes = 306 # Extracted from beam.msh (first line under $Nodes)
        ref_amount_tetras = 807 # Extracted from beam.msh (line beginning with 3 in $Elements)

        for _ in range(10):
            Sofa.Simulation.animate(self.root, self.root.dt.value)
            self.assertEqual(len(self.mech_obj.position.value), ref_amount_nodes)
            self.assertEqual(len(self.topo.tetrahedra.value), ref_amount_tetras)

    def testSurfaceMeshSimulation(self):
        ref_amount_nodes = 290 # Extracted from beam.msh (second line under $Nodes)
        ref_amount_faces = 576 # Extracted from beam.msh (first line under $Elements)

        for _ in range(10):
            Sofa.Simulation.animate(self.root, self.root.dt.value)
            self.assertEqual(len(self.ogl.position.value), ref_amount_nodes)
            self.assertEqual(len(self.ogl.triangles.value), ref_amount_faces)

    def testVolumeToSurfaceLink(self):
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

    def testVolumeToSurfaceLinkSimulation(self):
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
    suite = unittest.TestSuite()

    ## Insert new tests here
    tests = [
        TestBeam,
    ]

    ## Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    ## Add tests to test suite
    suite.addTests(loaded_tests)
    return suite
