from random import uniform, choices, choice, randint
import string
import unittest
import numpy as np
from src.config import Config
from src.units import YoungsModulus, Density, Tesla


class TestConfig(unittest.TestCase):
    def test_show_force(self):
        # Test False to True
        Config.set_show_force(False)
        self.assertFalse(Config.get_show_force())
        Config.set_show_force(True)
        self.assertTrue(Config.get_show_force())
        # Test if method is toggling True and False
        Config.set_show_force(True)
        self.assertTrue(Config.get_show_force())
        # Test True to False
        Config.set_show_force(False)
        self.assertFalse(Config.get_show_force())

    def test_model(self):
        ref_name = ''.join(
            choices(string.ascii_uppercase + string.digits, k=6))
        ref_scale = uniform(0, 100)

        Config.set_model(ref_name, ref_scale)

        self.assertEqual(Config.get_name(), ref_name,
                         msg="Model name is not correct")
        self.assertAlmostEqual(Config.get_scale(), ref_scale,
                               msg="Model scale is not correct")

    def test_model_exceptional(self):
        err_scale = uniform(-100, 0)

        with self.assertRaises(ValueError):
            Config.set_model("test", err_scale)

    def test_external_forces(self):
        ref_use_gravity = choice([True, False])
        ref_gravity_vec = np.random.uniform(0, 100, 3)
        ref_magnetic_force = Tesla.from_T(uniform(0, 100))
        ref_magnetic_dir = np.random.uniform(0, 20, 3)
        normalised_magnetic_dir = ref_magnetic_dir / \
            np.linalg.norm(ref_magnetic_dir)
        ref_b_field = ref_magnetic_force.T * normalised_magnetic_dir
        ref_initial_dipole_moment = np.random.uniform(0, 20, 3)

        Config.set_external_forces(
            ref_use_gravity,
            ref_gravity_vec,
            ref_magnetic_force,
            ref_magnetic_dir,
            ref_initial_dipole_moment
        )

        self.assertEqual(Config.get_use_gravity(),
                         ref_use_gravity, msg="Use gravity is not correct")
        for pair in zip(Config.get_gravity_vec(), ref_gravity_vec):
            self.assertAlmostEqual(*pair, msg="Gravity vector is not correct")
        self.assertAlmostEqual(Config.get_magnetic_force(
        ).T, ref_magnetic_force.T, msg="Magnetic force is not correct")
        for elem in np.cross(Config.get_magnetic_dir(), ref_magnetic_dir):
            self.assertAlmostEqual(
                elem, 0, msg="Magnetic direction is not correct")
        self.assertGreaterEqual(np.dot(Config.get_magnetic_dir(
        ), ref_magnetic_dir), 0, msg="Magnetic direction is not correct")
        self.assertAlmostEqual(np.linalg.norm(
            Config.get_magnetic_dir()), 1, msg="Magnetic direction is not normalized")
        for pair in zip(Config.get_b_field(), ref_b_field):
            self.assertAlmostEqual(*pair, msg="B field is not correct")
        for pair in zip(Config.get_initial_dipole_moment(), ref_initial_dipole_moment):
            self.assertAlmostEqual(
                *pair, msg="Initial dipole moment is not correct")

    def test_external_forces_exceptional(self):
        err_gravity_vec1 = np.random.uniform(0, 100, 4)
        err_gravity_vec2 = np.random.uniform(0, 100, (3, 1))
        err_magnetic_force = Tesla.from_T(uniform(-100, 0))
        err_magnetic_dir1 = np.random.uniform(0, 100, 4)
        err_magnetic_dir2 = np.random.uniform(0, 100, (3, 1))
        err_initial_dipole_moment1 = np.random.uniform(0, 100, 4)
        err_initial_dipole_moment2 = np.random.uniform(0, 100, (3, 1))

        with self.assertRaises(ValueError):
            Config.set_external_forces(
                True,
                err_gravity_vec1,
                Tesla(0),
                np.array([0, 0, 0]),
                np.array([0, 0, 0])
            )

        with self.assertRaises(ValueError):
            Config.set_external_forces(
                True,
                err_gravity_vec2,
                Tesla(0),
                np.array([0, 0, 0]),
                np.array([0, 0, 0])
            )

        with self.assertRaises(ValueError):
            Config.set_external_forces(
                True,
                np.array([0, 0, 0]),
                err_magnetic_force,
                np.array([0, 0, 0]),
                np.array([0, 0, 0])
            )

        with self.assertRaises(ValueError):
            Config.set_external_forces(
                True,
                np.array([0, 0, 0]),
                Tesla(0),
                err_magnetic_dir1,
                np.array([0, 0, 0])
            )

        with self.assertRaises(ValueError):
            Config.set_external_forces(
                True,
                np.array([0, 0, 0]),
                Tesla(0),
                err_magnetic_dir2,
                np.array([0, 0, 0])
            )

        with self.assertRaises(ValueError):
            Config.set_external_forces(
                True,
                np.array([0, 0, 0]),
                Tesla(0),
                np.array([0, 0, 0]),
                err_initial_dipole_moment1
            )

        with self.assertRaises(ValueError):
            Config.set_external_forces(
                True,
                np.array([0, 0, 0]),
                Tesla(0),
                np.array([0, 0, 0]),
                err_initial_dipole_moment2
            )

    def test_material_parameters(self):
        ref_poisson_ratio = uniform(0, 0.4999)
        ref_youngs_modulus = YoungsModulus.from_Pa(uniform(0, 100))
        ref_density = Density.from_kgpm3(uniform(0, 100))
        ref_remanence = Tesla.from_T(uniform(0, 100))

        Config.set_material_parameters(
            ref_poisson_ratio,
            ref_youngs_modulus,
            ref_density,
            ref_remanence
        )

        self.assertAlmostEqual(Config.get_poisson_ratio(
        ), ref_poisson_ratio, msg="Poisson ratio is not correct")
        self.assertAlmostEqual(Config.get_youngs_modulus(
        ).Pa, ref_youngs_modulus.Pa, msg="Youngs modulus is not correct")
        self.assertAlmostEqual(Config.get_density().kgpm3,
                               ref_density.kgpm3, msg="Density is not correct")
        self.assertAlmostEqual(Config.get_remanence().T,
                               ref_remanence.T, msg="Remanence is not correct")

    def test_material_parameters_exceptional(self):
        err_poisson_ratio1 = uniform(-100, -1)
        err_poisson_ratio2 = uniform(0.5, 100)

        with self.assertRaises(ValueError):
            Config.set_material_parameters(
                err_poisson_ratio1,
                YoungsModulus.from_Pa(0),
                Density.from_kgpm3(0),
                Tesla.from_T(0)
            )

        with self.assertRaises(ValueError):
            Config.set_material_parameters(
                err_poisson_ratio2,
                YoungsModulus.from_Pa(0),
                Density.from_kgpm3(0),
                Tesla.from_T(0)
            )

    def test_plugin_list(self):
        rand_len = randint(1, 20)
        ref_plugin_list = [''.join(
            choices(string.ascii_uppercase + string.digits, k=20)) for _ in range(rand_len)]

        Config.set_plugin_list(ref_plugin_list)

        for pair in zip(Config.get_plugin_list(), ref_plugin_list):
            self.assertEqual(*pair)

    def test_constraints(self):
        ref_a = np.random.uniform(0, 100, 3)
        ref_b = np.random.uniform(0, 100, 3)

        Config.set_constraints(ref_a, ref_b)

        for pair in zip(Config.get_constraints()[0], ref_a):
            self.assertAlmostEqual(
                *pair, msg=f"Constraint a is not correct, got {Config.get_constraints()[0]}, expected {ref_a}")
        for pair in zip(Config.get_constraints()[1], ref_b):
            self.assertAlmostEqual(
                *pair, msg=f"Constraint b is not correct, got {Config.get_constraints()[1]}, expected {ref_b}")
        self.assertTrue(Config.get_use_constraints())

    def test_default_constraints(self):
        ref_a = np.array([0, 0, 0])
        ref_b = np.array([0, 0, 0])
        Config.set_default_constraints()

        self.assertFalse(Config.get_use_constraints())
        for pair in zip(Config.get_constraints()[0], ref_a):
            self.assertAlmostEqual(
                *pair, msg=f"Constraint a is not correct, got {Config.get_constraints()[0]}, expected {ref_a}")
        for pair in zip(Config.get_constraints()[1], ref_b):
            self.assertAlmostEqual(
                *pair, msg=f"Constraint b is not correct, got {Config.get_constraints()[1]}, expected {ref_b}")

        names = ["beam", "butterfly", "gripper_3_arm",
                 "gripper_4_arm", "simple_butterfly"]
        refs_a = [
            [-0.005, 0, 0],
            [-0.001449, -0.00869, -0.00289],
            [-0.05, -0.05, 0.01],
            [-0.05, -0.05, 0.01],
            [-0.001449, -0.00869, -0.00289]
        ]
        refs_b = [
            [0.005, 0.05, 0.05],
            [0.001449, 0.000724, 0.001449],
            [0.05, 0.05, 0.03],
            [0.05, 0.05, 0.03],
            [0.001449, 0.000724, 0.001449]
        ]
        for i, name in enumerate(names):
            Config.set_model(name, 1)
            Config.set_default_constraints()
            self.assertTrue(Config.get_use_constraints())
            for pair in zip(Config.get_constraints()[0], refs_a[i]):
                self.assertAlmostEqual(
                    *pair, msg=f"Constraint a is not correct, got {Config.get_constraints()[0]}, expected {refs_a[i]}")
            for pair in zip(Config.get_constraints()[1], refs_b[i]):
                self.assertAlmostEqual(
                    *pair, msg=f"Constraint b is not correct, got {Config.get_constraints()[1]}, expected {refs_b[i]}")

    def test_constraints_exceptional(self):
        err_a1 = np.random.uniform(0, 100, 4)
        err_a2 = np.random.uniform(0, 100, (3, 1))
        err_b1 = np.random.uniform(0, 100, 4)
        err_b2 = np.random.uniform(0, 100, (3, 1))

        with self.assertRaises(ValueError):
            Config.set_constraints(err_a1, np.array([0, 0, 0]))

        with self.assertRaises(ValueError):
            Config.set_constraints(err_a2, np.array([0, 0, 0]))

        with self.assertRaises(ValueError):
            Config.set_constraints(np.array([0, 0, 0]), err_b1)

        with self.assertRaises(ValueError):
            Config.set_constraints(np.array([0, 0, 0]), err_b2)

    def test_stress_kwargs(self) -> None:
        ref_dict_0 = {
            'computeVonMisesStress': 0,
            'showVonMisesStressPerNodeColorMap': 0,
        }
        ref_dict_1 = {
            'computeVonMisesStress': 1,
            'showVonMisesStressPerNodeColorMap': 1,
        }
        self.assertFalse(Config.get_show_stress(), "default should be false")
        self.assertEqual(ref_dict_0, Config.get_stress_kwargs(),
                         msg="default should be dict with two keys and 0 vals")

        Config.set_stress_kwargs(True)
        self.assertTrue(Config.get_show_stress(),
                        "should be True after kwargs set to True")
        self.assertEqual(ref_dict_1, Config.get_stress_kwargs(),
                         msg="vals should hold value 1 after kwargs set to False")

        Config.set_stress_kwargs(False)
        self.assertFalse(Config.get_show_stress(),
                         "should be False after kwargs set to False")
        self.assertEqual(ref_dict_0, Config.get_stress_kwargs(),
                         msg="vals should hold value 0 after kwargs set to False")

        Config.set_stress_kwargs(True)
        Config._reset_stress_kwargs()
        self.assertFalse(Config.get_show_stress(),
                         "should be False after kwargs reset")
        self.assertEqual(ref_dict_0, Config.get_stress_kwargs(),
                         msg="vals should hold value 0 after kwargs reset")

        Config.set_stress_kwargs(True)
        Config.reset()
        self.assertFalse(Config.get_show_stress(),
                         "should be False after hard reset")
        self.assertEqual(ref_dict_0, Config.get_stress_kwargs(),
                         msg="vals should hold value 0 after hard reset")

    def tearDown(self) -> None:
        """Resets config after each test."""
        Config.reset()


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestConfig,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
