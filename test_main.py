import unittest
from tests import *

suite = unittest.TestSuite()
test_suites = []

# Add new test suites here
suite.addTests([
    density_test_suite(),
    tesla_test_suite(),
    youngs_modulus_test_suite(),
    config_test_suite(),
    magnetic_controller_test_suite(),
    material_loader_test_suite(),
    mesh_loader_test_suite(),
    scene_builder_test_suite(),
    beam_test_suite(),
    gripper_3_arm_test_suite(),
    gripper_4_arm_test_suite(),
])

runner = unittest.TextTestRunner()
runner.run(suite)
