import unittest
import tests.units.YoungsModulusTest
import tests.units.DensityTest
import tests.units.TeslaTest
import tests.MagneticControllerTest
import tests.mesh_loader_test
import tests.material_loader_test
import tests.configTest
import tests.meshes.BeamTest

suite = unittest.TestSuite()
test_suites = []

# Add new test suites here
suite.addTests([
    tests.units.YoungsModulusTest.suite(),
    tests.units.DensityTest.suite(),
    tests.units.TeslaTest.suite(),
    tests.MagneticControllerTest.suite(),
    tests.mesh_loader_test.suite(),
    tests.material_loader_test.suite(),
    tests.configTest.suite(),
    tests.meshes.BeamTest.suite(),
])

runner = unittest.TextTestRunner()
runner.run(suite)
