import unittest
import unittest.mock
from random import uniform

from src.material_loader import MaterialLoader
from src.units.YoungsModulus import YoungsModulus
from src.units.Density import Density


class TestRegularBehavior(unittest.TestCase):
    def test_density(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        d = Density.fromkgpm3(uniform(0, 20))
        expected_density = d.kgpm3

        uut.set_density(d)
        uut.update_elastic_object()
        _, kwargs = eo.diagonal_mass.setDataValues.call_args
        self.assertEqual(kwargs['massDensity'], expected_density)
        self.assertEqual(uut.get_density().kgpm3, expected_density)

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
        self.assertEqual(kwargs['poissonRatio'], expected_poissons_ratio)
        self.assertEqual(uut.get_poissons_ratio(), expected_poissons_ratio)

    def test_remanence(self):
        eo = unittest.mock.Mock()
        uut = MaterialLoader(eo)
        expected_remanence = uniform(-100, 100)
        uut.set_remanence(expected_remanence)
        uut.update_elastic_object()
        self.assertEqual(eo.remanence, expected_remanence)
        self.assertEqual(uut.get_remanence(), expected_remanence)

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


def suite() -> unittest.TestSuite:
    suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestRegularBehavior,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    suite.addTests(loaded_tests)
    return suite
