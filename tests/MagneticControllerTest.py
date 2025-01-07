import unittest
from src.magnetic_controller import MagneticController
from src.elastic_body import ElasticObject, createElasticObject

import numpy as np
from scipy.spatial.transform import Rotation


class TestAngles(unittest.TestCase):

    def testRightAngle(self):
        actual = MagneticController.calculate_angle([0,0,-1], [0,1,0], 'x')
        ref = np.pi / 2
        self.assertAlmostEqual(actual, ref)

    def testParallel(self):
        actual = MagneticController.calculate_angle([0,0,1], [0,0,1], 'x')
        ref = 0
        self.assertAlmostEqual(actual, ref)

    def testAntiParallel(self):
        actual = MagneticController.calculate_angle([0,0,-1], [0,0,1], 'x')
        ref = np.pi
        self.assertAlmostEqual(np.abs(actual), ref)

    def testSignChange(self):
        a,b = [0, 0, -1], [0, 1, 0]
        actual1 = MagneticController.calculate_angle(a,b, 'x')
        actual2 = MagneticController.calculate_angle(b,a, 'x')
        self.assertAlmostEqual(actual1, -1*actual2)

    def testRandomized(self):
        rand_vec = (np.random.rand(3) - 0.5) * 20
        rand_angs = (np.random.rand(3) - 0.5) * 2*np.pi

        if False:
            r = Rotation.from_euler('xyz', rand_angs, degrees=False)
            rotated_vec = r.apply(rand_vec)

            for i, subscript in enumerate(['x', lambda x: x[::2], lambda x: x[:2]]):
                a = MagneticController.calculate_angle(rand_vec, rotated_vec, subscript)
                self.assertAlmostEqual(a, rand_angs[i], msg=f"index {i}")
        # was hier passiert stimmt nicht. die winkel werden im nachhinein nochmal verändert werden.
        # stell dir vor, du schaust aus einer Richtung auf einen 45 grad winkel und drehst dann nochmal um die vertikale achse. 
        # dann spitzt sich der winkel der projektion logischerweise zu, da er ja irgendwann 0 werden muss (wenn der vektor so steht dass wir gerade draufsehen)
        # dh der erste winkel ist nicht notwendigerweise nach der letzten rotation so, wie wir ihn initial durchs drehen gebaut haben

        for i, subscript in enumerate('xyz'):
            one_axis = 'xyz'[i]
            one_angle = rand_angs[i]

            r = Rotation.from_euler(one_axis, one_angle, degrees=False)
            rotated_vec = r.apply(rand_vec)

            a = MagneticController.calculate_angle(rand_vec, rotated_vec, subscript) # sign error still persists, swapping order of compared vecs only changes axis in which they occur (y, if swapped x)
            self.assertAlmostEqual(a, one_angle, msg=f"axis {one_axis}")

    def testOne0(self):
        rand_vec = (np.random.rand(3) - 0.5) * 20
        actual = MagneticController.calculate_angle([0,0,0], rand_vec, 'x')
        ref = 0
        self.assertAlmostEqual(np.abs(actual), ref)

        rand_vec = (np.random.rand(3) - 0.5) * 20
        actual = MagneticController.calculate_angle(rand_vec, [0,0,0], 'x')
        ref = 0
        self.assertAlmostEqual(np.abs(actual), ref)

    def testBoth0(self):
        actual = MagneticController.calculate_angle([0,0,0], [0,0,0], 'x')
        ref = 0
        self.assertAlmostEqual(np.abs(actual), ref)
        
    def testAxisErrors(self):
        with self.assertRaises(ValueError):
            MagneticController.calculate_angle([0,0,0], [1,1,1], 'w')
            
        with self.assertRaises(ValueError):
            MagneticController.calculate_angle([0,0,0], [1,1,1], 69)



class TestRotation(unittest.TestCase):
    def testRandomized(self):
        rand_base_vector = (np.random.rand(3) - 0.5) * 20
        rand_angles = (np.random.rand(3) - 0.5) * 2*np.pi

        reference_rotation = Rotation.from_euler("xyz", rand_angles, degrees=False)
        reference_vector = reference_rotation.apply(rand_base_vector)

        rot_under_test = MagneticController.calculate_rotation(rand_base_vector, reference_vector)
        #result_under_test = rot_under_test.apply(rand_base_vector)
        result_under_test = rot_under_test.apply(rand_base_vector)

        for pair in zip(reference_vector, result_under_test):
            self.assertAlmostEqual(*pair, msg=f"{reference_vector} expected but found {result_under_test}, reference_rotation: {reference_rotation.as_euler('xyz')}, rot_under_test: {rot_under_test}")

    def testNoRot(self):
        rand_base_vector = (np.random.rand(3) - 0.5) * 20
        noRot_angles = [0,0,0]

        reference_rotation = Rotation.from_euler("xyz", noRot_angles, degrees=False)
        reference_vector = reference_rotation.apply(rand_base_vector)

        rot_under_test = MagneticController.calculate_rotation(rand_base_vector, reference_vector)
        #result_under_test = rot_under_test.apply(rand_base_vector)
        result_under_test = rot_under_test.apply(rand_base_vector)

        for pair in zip(reference_vector, result_under_test):
            self.assertAlmostEqual(*pair, msg=f"{reference_vector} expected but found {result_under_test}, reference_rotation: {reference_rotation.as_euler('xyz')}, rot_under_test: {rot_under_test}")

    def testAntiParallel(self):
        rand_base_vector = (np.random.rand(3) - 0.5) * 20
        reverse_base_vector = -1 * rand_base_vector

        rot_under_test = MagneticController.calculate_rotation(rand_base_vector, reverse_base_vector)
        #result_under_test = rot_under_test.apply(rand_base_vector)
        result_under_test = rot_under_test.apply(rand_base_vector)

        for pair in zip(reverse_base_vector, result_under_test):
            self.assertAlmostEqual(*pair, msg=f"{reverse_base_vector} expected but found {result_under_test}", places=5)



def suite() -> unittest.TestSuite: 
    suite = unittest.TestSuite()

    ## Insert new tests here
    tests = [
        TestAngles,
        TestRotation,
    ]

    ## Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    ## Add tests to test suite
    suite.addTests(loaded_tests)
    return suite
