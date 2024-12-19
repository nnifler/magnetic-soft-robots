import unittest
from src.magnetic_controller import MagneticController
from src.elastic_body import ElasticObject, createElasticObject

import numpy as np
from scipy.spatial.transform import Rotation


class TestAngles(unittest.TestCase):

    def testRightAngle(self):
        actual = MagneticController.calculate_angle(None, [0,0,-1], [0,1,0], lambda x: x[1:])
        ref = np.pi / 2
        self.assertAlmostEqual(actual, ref)

    def testParallel(self):
        actual = MagneticController.calculate_angle(None, [0,0,1], [0,0,1], lambda x: x[1:])
        ref = 0
        self.assertAlmostEqual(actual, ref)

    def testAntiParallel(self):
        actual = MagneticController.calculate_angle(None, [0,0,-1], [0,0,1], lambda x: x[1:])
        ref = np.pi
        self.assertAlmostEqual(np.abs(actual), ref)

    def testSignChange(self):
        a,b = [0, 0, -1], [0, 1, 0]
        actual1 = MagneticController.calculate_angle(None, a,b, lambda x: x[1:])
        actual2 = MagneticController.calculate_angle(None, b,a, lambda x: x[1:])
        self.assertAlmostEqual(actual1, -1*actual2)

    def testRandomized(self):
        rand_vec = (np.random.rand(3) - 0.5) * 20
        rand_angs = (np.random.rand(3) - 0.5) * 2*np.pi
        r = Rotation.from_euler('xyz', rand_angs, degrees=False)
        rotated_vec = r.apply(rand_vec)

        for i, subscript in enumerate([lambda x: x[1:], lambda x: x[::2], lambda x: x[:2]]):
            a = MagneticController.calculate_angle(None, rand_vec, rotated_vec, subscript)
            self.assertAlmostEqual(a, rand_angs[i], msg=f"index {i}")

    def testOne0(self):
        rand_vec = (np.random.rand(3) - 0.5) * 20
        actual = MagneticController.calculate_angle(None, [0,0,0], rand_vec, lambda x: x[1:])
        ref = 0
        self.assertAlmostEqual(np.abs(actual), ref)

        rand_vec = (np.random.rand(3) - 0.5) * 20
        actual = MagneticController.calculate_angle(None, rand_vec, [0,0,0], lambda x: x[1:])
        ref = 0
        self.assertAlmostEqual(np.abs(actual), ref)

    def testBoth0(self):
        actual = MagneticController.calculate_angle(None, [0,0,0], [0,0,0], lambda x: x[1:])
        ref = 0
        self.assertAlmostEqual(np.abs(actual), ref)

def suite() -> unittest.TestSuite: 
    suite = unittest.TestSuite()

    ## Insert new tests here
    tests = [
        TestAngles
    ]

    ## Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    ## Add tests to test suite
    suite.addTests(loaded_tests)
    return suite
