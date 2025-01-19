import unittest
from math import isclose

import Sofa

import Sofa.Simulation
from sofa_instantiator import createScene

def isInPositionArray(value, array):
    for element in array:
        if all([isclose(p1, p2, rel_tol=1e-5) for p1, p2 in zip(element, value)]):
            return True
    return False

class TestBeam(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # TODO: Make sure that beam object is used (only really doable as soon as LINK is in main)
        cls.root = Sofa.Core.Node("root")
        createScene(cls.root)
        Sofa.Simulation.init(cls.root)

        cls.elastic_object = cls.root.getChild('object')
        cls.visu = cls.elastic_object.getChild('VisualModel')
        cls.ogl = cls.visu.getObject('model')
        cls.mech_obj = cls.elastic_object.getObject('dofs')
        cls.topo = cls.elastic_object.getObject('topo')

    def setUp(self):
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
