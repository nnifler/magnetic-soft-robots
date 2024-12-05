import unittest
import tests.units.YoungsModulusTest

suite = unittest.TestSuite()
test_suites = []

# Add new test suites here
suite.addTests([
    tests.units.YoungsModulusTest.suite()
])

runner = unittest.TextTestRunner()
runner.run(suite)
