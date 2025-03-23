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
from random import choices
import string
import numpy as np

import Sofa

from src import SceneBuilder, Config


class TestSceneBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Config.set_test_env()

    def test_gravity(self):
        ref_gravity = np.random.uniform(0, 100, 3)
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

        invalid_vector1 = np.random.uniform(0, 100, 2)
        invalid_vector2 = np.random.uniform(0, 100, (3, 1))
        with self.assertRaises(ValueError):
            SceneBuilder(root, gravity_vec=invalid_vector1)
        with self.assertRaises(ValueError):
            SceneBuilder(root, gravity_vec=invalid_vector2)

    def test_no_gravity(self):
        gravity = np.random.uniform(0, 100, 3)
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

        for actual, ref in zip(root.gravity.value, [0, 0, 0]):
            self.assertAlmostEqual(actual, ref)

        Config.set_external_forces(
            old_ug,
            Config.get_gravity_vec(),
            Config.get_magnetic_force(),
            Config.get_magnetic_dir(),
            Config.get_initial_dipole_moment()
        )

    def test_dt(self):
        ref_dt = np.random.uniform(0, 100)

        root = Sofa.Core.Node("root")
        SceneBuilder(root, dt=ref_dt)

        self.assertAlmostEqual(root.dt.value, ref_dt)

    def test_dt_exceptional(self):
        root = Sofa.Core.Node("root")

        invalid_dt = np.random.uniform(-100, 0)
        with self.assertRaises(ValueError):
            SceneBuilder(root, dt=invalid_dt)
        with self.assertRaises(ValueError):
            SceneBuilder(root, dt=0)

    def test_plugins(self):
        root = Sofa.Core.Node("root")
        SceneBuilder(root)

        for plugin in Config.get_plugin_list():
            self.assertIn(plugin, root.getObject(
                'RequiredPlugin').pluginName.value)

    def test_child(self):
        root = Sofa.Core.Node("root")
        uut = SceneBuilder(root)

        name = ''.join(choices(string.ascii_uppercase + string.digits, k=6))
        uut.create_child(name)

        child = root.getChild(name)
        self.assertIsNotNone(child)

    @classmethod
    def tearDownClass(cls):
        Config.reset()


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestSceneBuilder,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
