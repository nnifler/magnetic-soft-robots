import unittest
import tests.units.YoungsModulusTest
import tests.units.DensityTest
import tests.MagneticControllerTest

suite = unittest.TestSuite()
test_suites = []

# Add new test suites here
suite.addTests([
    tests.units.YoungsModulusTest.suite(),
    tests.units.DensityTest.suite(),
    tests.MagneticControllerTest.suite(),
])

runner = unittest.TextTestRunner()
runner.run(suite)
