import unittest
import tests.units.YoungsModulusTest
import tests.units.DensityTest

suite = unittest.TestSuite()
test_suites = []

# Add new test suites here
suite.addTests([
    tests.units.YoungsModulusTest.suite(),
    tests.units.DensityTest.suite()
])

runner = unittest.TextTestRunner()
runner.run(suite)
