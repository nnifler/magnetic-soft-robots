import unittest
import tests.units.YoungsModulusTest
import tests.units.DensityTest
import tests.MagneticControllerTest
import tests.mesh_loader_test
suite = unittest.TestSuite()
test_suites = []

# Add new test suites here
suite.addTests([
    tests.units.YoungsModulusTest.suite(),
    tests.units.DensityTest.suite(),
    tests.MagneticControllerTest.suite(),
    tests.mesh_loader_test.suite(),
])

runner = unittest.TextTestRunner()
runner.run(suite)
