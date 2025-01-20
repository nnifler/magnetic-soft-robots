import unittest
import unittest.mock
from random import uniform

from src.material_loader import MaterialLoader
from src.units.YoungsModulus import YoungsModulus
from src.units.Density import Density
from src.units.Tesla import Tesla


class TestNormalBehavior(unittest.TestCase):
    def test_density(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        d = Density.fromkgpm3(uniform(0, 20))
        expected_density = d.kgpm3

        uut.set_density(d)
        uut.update_elastic_object()
        _, kwargs = eo.diagonal_mass.setDataValues.call_args
        self.assertAlmostEqual(kwargs['massDensity'], expected_density)
        self.assertAlmostEqual(uut.get_density().kgpm3, expected_density)

    def test_youngs_modulus(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        y = YoungsModulus.fromGPa(uniform(0, 20))
        expected_modulus = y.Pa

        uut.set_youngs_modulus(y)
        uut.update_elastic_object()
        _, kwargs = eo.FEM_force_field.setDataValues.call_args
        self.assertEqual(kwargs['youngModulus'], expected_modulus)
        self.assertEqual(uut.get_youngs_modulus().Pa, expected_modulus)

    def test_poissons_ratio(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        expected_poissons_ratio = uniform(-0.499, 0.499)

        uut.set_poissons_ratio(expected_poissons_ratio)
        uut.update_elastic_object()
        _, kwargs = eo.FEM_force_field.setDataValues.call_args
        self.assertAlmostEqual(kwargs['poissonRatio'], expected_poissons_ratio)
        self.assertAlmostEqual(uut.get_poissons_ratio(), expected_poissons_ratio)

    def test_remanence(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        r = Tesla.fromT(uniform(-100, 100))
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
        d = Density.fromkgpm3(uniform(0, 20))

        uut.set_density(d)
        with self.assertRaises(ValueError):
            uut.get_density()

    def test_youngs_modulus(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        y = YoungsModulus.fromGPa(uniform(0, 20))

        uut.set_youngs_modulus(y)
        with self.assertRaises(ValueError):
            uut.get_youngs_modulus()

    def test_poissons_ratio(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        expected_poissons_ratio = uniform(-0.499, 0.499)

        uut.set_poissons_ratio(expected_poissons_ratio)
        with self.assertRaises(ValueError):
            uut.get_poissons_ratio(),

    def test_remanence(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        r = Tesla.fromT(uniform(-100, 100))
        
        uut.set_remanence(r)
        with self.assertRaises(ValueError):
            uut.get_remanence()


def suite() -> unittest.TestSuite:
    suite = unittest.TestSuite()

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
    suite.addTests(loaded_tests)
    return suite
