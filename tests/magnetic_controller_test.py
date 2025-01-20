import unittest
import numpy as np
from scipy.spatial.transform import Rotation

from src import MagneticController


class TestAngles(unittest.TestCase):

    def test_right_angle(self):
        actual = MagneticController.calculate_angle([0, 0, -1], [0, 1, 0], 'x')
        ref = np.pi / 2
        self.assertAlmostEqual(actual, ref)

    def test_parallel(self):
        actual = MagneticController.calculate_angle([0, 0, 1], [0, 0, 1], 'x')
        ref = 0
        self.assertAlmostEqual(actual, ref)

    def test_anti_parallel(self):
        actual = MagneticController.calculate_angle([0, 0, -1], [0, 0, 1], 'x')
        ref = np.pi
        self.assertAlmostEqual(np.abs(actual), ref)

    def test_sign_change(self):
        a, b = [0, 0, -1], [0, 1, 0]
        actual1 = MagneticController.calculate_angle(a, b, 'x')
        actual2 = MagneticController.calculate_angle(b, a, 'x')
        self.assertAlmostEqual(actual1, -1*actual2)

    def test_randomized(self):
        rand_vec = (np.random.rand(3) - 0.5) * 20
        rand_angs = (np.random.rand(3) - 0.5) * 2*np.pi

        for i, subscript in enumerate('xyz'):
            one_axis = 'xyz'[i]
            one_angle = rand_angs[i]

            r = Rotation.from_euler(one_axis, one_angle, degrees=False)
            rotated_vec = r.apply(rand_vec)

            # sign error still persists, swapping order of compared vecs
            # only changes axis in which they occur (y, if swapped x)
            a = MagneticController.calculate_angle(
                rand_vec, rotated_vec, subscript)
            self.assertAlmostEqual(a, one_angle, msg=f"axis {one_axis}")

    def test_one_0(self):
        rand_vec = (np.random.rand(3) - 0.5) * 20
        actual = MagneticController.calculate_angle([0, 0, 0], rand_vec, 'x')
        ref = 0
        self.assertAlmostEqual(np.abs(actual), ref)

        rand_vec = (np.random.rand(3) - 0.5) * 20
        actual = MagneticController.calculate_angle(rand_vec, [0, 0, 0], 'x')
        ref = 0
        self.assertAlmostEqual(np.abs(actual), ref)

    def test_both_0(self):
        actual = MagneticController.calculate_angle([0, 0, 0], [0, 0, 0], 'x')
        ref = 0
        self.assertAlmostEqual(np.abs(actual), ref)

    def test_axis_errors(self):
        with self.assertRaises(ValueError):
            MagneticController.calculate_angle([0, 0, 0], [1, 1, 1], 'w')

        with self.assertRaises(ValueError):
            MagneticController.calculate_angle([0, 0, 0], [1, 1, 1], 69)


class TestRotation(unittest.TestCase):
    def test_randomized(self):
        rand_base_vector = (np.random.rand(3) - 0.5) * 20
        rand_angles = (np.random.rand(3) - 0.5) * 2*np.pi

        reference_rotation = Rotation.from_euler(
            "xyz", rand_angles, degrees=False)
        reference_vector = reference_rotation.apply(rand_base_vector)

        rot_under_test = MagneticController.calculate_rotation(
            rand_base_vector, reference_vector)
        # result_under_test = rot_under_test.apply(rand_base_vector)
        result_under_test = rot_under_test.apply(rand_base_vector)

        for pair in zip(reference_vector, result_under_test):
            self.assertAlmostEqual(
                *pair, msg=f"{reference_vector} expected but found {result_under_test}, " +
                f"reference_rotation: {reference_rotation.as_euler('xyz')}, " +
                f"rot_under_test: {rot_under_test}"
            )

    def test_no_rot(self):
        rand_base_vector = (np.random.rand(3) - 0.5) * 20
        no_rot_angles = [0, 0, 0]

        reference_rotation = Rotation.from_euler(
            "xyz", no_rot_angles, degrees=False)
        reference_vector = reference_rotation.apply(rand_base_vector)

        rot_under_test = MagneticController.calculate_rotation(
            rand_base_vector, reference_vector)
        # result_under_test = rot_under_test.apply(rand_base_vector)
        result_under_test = rot_under_test.apply(rand_base_vector)

        for pair in zip(reference_vector, result_under_test):
            self.assertAlmostEqual(
                *pair, msg=f"{reference_vector} expected but found {result_under_test}, " +
                f"reference_rotation: {reference_rotation.as_euler('xyz')}, " +
                f"rot_under_test: {rot_under_test}"
            )

    def test_anti_parallel(self):
        rand_base_vector = (np.random.rand(3) - 0.5) * 20
        reverse_base_vector = -1 * rand_base_vector

        rot_under_test = MagneticController.calculate_rotation(
            rand_base_vector, reverse_base_vector)
        # result_under_test = rot_under_test.apply(rand_base_vector)
        result_under_test = rot_under_test.apply(rand_base_vector)

        for pair in zip(reverse_base_vector, result_under_test):
            self.assertAlmostEqual(
                *pair, msg=f"{reverse_base_vector} expected but found {result_under_test}",
                places=5
            )


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestAngles,
        TestRotation,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
