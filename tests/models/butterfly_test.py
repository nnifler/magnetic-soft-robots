# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ #
#                        MSR, Magnetic Soft Robotics Simulation                        #
#   Copyright (C) 2025 Julius Hahnewald, Heiko Hellkamp, Finn Schubert, Carla Wehner   #
#                                                                                      #
# This program is free software; you can redistribute it and/or                        #
# modify it under the terms of the GNU Lesser General Public                           #
# License as published by the Free Software Foundation; either                         #
# version 2.1 of the License, or (at your option) any later version.                   #
#                                                                                      #
# This program is distributed in the hope that it will be useful,                      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU                    #
# Lesser General Public License for more details.                                      #
#                                                                                      #
# You should have received a copy of the GNU Lesser General Public                     #
# License along with this program; if not, write to the Free Software                  #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301            #
# USA                                                                                  #
# ------------------------------------------------------------------------------------ #
# Contact information: finn.s.schubert@gmail.com                                       #
# ____________________________________________________________________________________ #

import unittest
import Sofa
import Sofa.Simulation
from src import Config, sofa_instantiator


class TestButterfly(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Called once before all the tests in the class"""
        Config.set_test_env()
        Config.set_model('butterfly', 1)

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
        ref_amount_nodes = 423
        # Extracted from beam.msh (line beginning with 3 in $Elements)
        ref_amount_tetras = 1094

        self.assertEqual(len(self.mech_obj.position.value), ref_amount_nodes)
        self.assertEqual(len(self.topo.tetrahedra.value), ref_amount_tetras)

    def test_surface_mesh(self):
        # Extracted from beam.msh (first line under $Nodes)
        ref_amount_nodes = 423
        # Extracted from beam.msh (first line under $Elements)
        ref_amount_faces = 826

        self.assertEqual(len(self.ogl.position.value), ref_amount_nodes)
        self.assertEqual(len(self.ogl.triangles.value), ref_amount_faces)

    def test_volume_mesh_simulation(self):
        # Extracted from beam.msh (first line under $Nodes)
        ref_amount_nodes = 423
        # Extracted from beam.msh (line beginning with 3 in $Elements)
        ref_amount_tetras = 1094

        for _ in range(10):
            Sofa.Simulation.animate(self.root, self.root.dt.value)
            self.assertEqual(
                len(self.mech_obj.position.value), ref_amount_nodes)
            self.assertEqual(len(self.topo.tetrahedra.value),
                             ref_amount_tetras)

    def test_surface_mesh_simulation(self):
        # Extracted from beam.msh (first line under $Nodes)
        ref_amount_nodes = 423
        # Extracted from beam.msh (first line under $Elements)
        ref_amount_faces = 826

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

    # This test does not pass right now, because BarycentricMapping is too inaccurate.
    # I dont want to change the mapping in this branch, because it would affect the the number of nodes in the ogl model.
    # Then the tests in the gripper branch would fail when both gripper and butterfly are merged.
    # Once both branches are merged, I will change the mapping to IdentityMapping and fix the tests.

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
        TestButterfly,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
