import unittest
import unittest.mock
from random import uniform

from src import MaterialLoader
from src.units import Density, YoungsModulus, Tesla


class TestNormalBehavior(unittest.TestCase):

    def test_density(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        d = Density.from_kgpm3(uniform(0, 20))
        expected_density = d.kgpm3

        uut.set_density(d)
        uut.update_elastic_object()
        _, kwargs = eo.diagonal_mass.setDataValues.call_args
        self.assertAlmostEqual(kwargs['massDensity'], expected_density)
        self.assertAlmostEqual(uut.get_density().kgpm3, expected_density)

    def test_youngs_modulus(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        y = YoungsModulus.from_GPa(uniform(0, 20))
        expected_modulus = y.Pa

        uut.set_youngs_modulus(y)
        uut.update_elastic_object()
        _, kwargs = eo.FEM_force_field.setDataValues.call_args
        self.assertEqual(kwargs['youngModulus'], [expected_modulus]*3)
        self.assertEqual(uut.get_youngs_modulus().Pa, expected_modulus)

    def test_poissons_ratio(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        expected_poissons_ratio = uniform(-0.499, 0.499)

        uut.set_poissons_ratio(expected_poissons_ratio)
        uut.update_elastic_object()
        _, kwargs = eo.FEM_force_field.setDataValues.call_args
        self.assertAlmostEqual(kwargs['poissonRatio'], expected_poissons_ratio)
        self.assertAlmostEqual(uut.get_poissons_ratio(),
                               expected_poissons_ratio)

    def test_remanence(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        r = Tesla.from_T(uniform(-100, 100))
        expected_remanence = r.T

        uut.set_remanence(r)
        uut.update_elastic_object()
        self.assertAlmostEqual(eo.remanence.T, expected_remanence)
        self.assertAlmostEqual(uut.get_remanence().T, expected_remanence)

    def test_no_update_made(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        uut.update_elastic_object()
        for func in [
            eo.remanence,
            eo.FEM_force_field.setDataValues,
            eo.diagonal_mass.setDataValues,
        ]:
            func.assert_not_called()


class TestExceptionalBehavior(unittest.TestCase):
    def test_density(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        d = Density.from_kgpm3(uniform(0, 20))

        uut.set_density(d)
        _ = uut.get_density()
        eo.diagonal_mass.setDataValues.assert_called()

    def test_youngs_modulus(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        y = YoungsModulus.from_GPa(uniform(0, 20))

        uut.set_youngs_modulus(y)
        _ = uut.get_youngs_modulus()
        eo.FEM_force_field.setDataValues.assert_called()

    def test_poissons_ratio(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        expected_poissons_ratio = uniform(-0.499, 0.499)

        uut.set_poissons_ratio(expected_poissons_ratio)
        _ = uut.get_poissons_ratio()
        eo.FEM_force_field.setDataValues.assert_called()

    def test_remanence(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        r = Tesla.from_T(uniform(-100, 100))

        uut.set_remanence(r)
        _ = uut.get_remanence()
        self.assertEqual(eo.remanence.T, r.T)


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestNormalBehavior,
        TestExceptionalBehavior
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
