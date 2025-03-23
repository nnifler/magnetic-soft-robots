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
import numpy as np
import Sofa
import Sofa.Simulation
from src import Config, sofa_instantiator


class TestConstraints(unittest.TestCase):

    def setUp(self):
        """Called before each test"""
        Config.set_test_env()
        Config.set_model("beam", 1)
        self.root = Sofa.Core.Node("root")

    def test_custom_constraints(self):
        ref_a = np.random.uniform(-10, 10, 3)
        ref_b = np.random.uniform(-10, 10, 3)
        Config.set_constraints(ref_a, ref_b)
        ref_box = np.concatenate((ref_a, ref_b))

        sofa_instantiator.createScene(self.root)
        elastic_object = self.root.getChild('object')

        roi = elastic_object.getObject('constraint_roi')
        for pair in zip(roi.box.value[0], ref_box):
            self.assertAlmostEqual(*pair)

    def test_default_constraints(self):
        names = ["beam", "butterfly", "gripper_3_arm",
                 "gripper_4_arm", "simple_butterfly"]
        refs = [
            [-0.0025, 0, 0, 0.0025, 0.025, 0.025],
            [-0.001449, -0.00869, -0.00289, 0.001449, 0.000724, 0.001449],
            [-0.025, -0.025, 0.005, 0.025, 0.025, 0.015],
            [-0.025, -0.025, 0.005, 0.025, 0.025, 0.015],
            [-0.001449, -0.00869, -0.00289, 0.001449, 0.000724, 0.001449]
        ]
        for i, name in enumerate(names):
            Config.set_model(name, 1)
            Config.set_default_constraints()
            sofa_instantiator.createScene(self.root)
            elastic_object = self.root.getChild('object')

            roi = elastic_object.getObject('constraint_roi')
            for pair in zip(roi.box.value[0], refs[i]):
                self.assertAlmostEqual(*pair)
            self.root = Sofa.Core.Node("root")

    def test_no_constraints(self):
        sofa_instantiator.createScene(self.root)
        elastic_object = self.root.getChild('object')

        self.assertIsNone(elastic_object.getChild('constraint_roi'))

    def tearDown(self):
        Config.reset()


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestConstraints,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
