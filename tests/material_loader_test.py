import unittest
from typing import get_type_hints
from src.material_loader import MaterialLoader
from src import elastic_body
from src.units.BaseUnit import BaseUnit
from src.units.YoungsModulus import YoungsModulus
from src.units.Density import Density
from tests.assets.dummy_node import DummyNode
from random import choice, randint


class TestNormalBehavior(unittest.TestCase):
    def test(self):
        root = DummyNode()
        elastic_object = elastic_body.createElasticObject(
            root, 'beam', 0., YoungsModulus.fromPa(0), Density.fromgpcm3(0), 1.)
        uut = MaterialLoader(elastic_object)
        methods = [[uut.set_density], [uut.set_youngs_modulus],
                   [uut.set_poissons_ratio], [uut.set_remanence]]
        for method in methods:
            value = None
            if issubclass(method_type := get_type_hints(method)['value'], BaseUnit):
                method_type_unit = choice(list(method_type.Unit)).name
                value = getattr(method_type, f'from{method_type_unit}')(
                    randint(0, 1000))
                method.append(value._value)
            else:
                value = randint(0, 1000000)/1000.
            method[0](value)

        uut.update_elastic_object()
        self.assertEqual(
            elastic_object.diagonal_mass.massDensity, methods[0][1])
        self.assertEqual(
            elastic_object.FEM_force_field.youngModulus, methods[1][1])
        self.assertEqual(
            elastic_object.FEM_force_field.poissonRatio, methods[2][1])
        self.assertEqual(
            elastic_object.FEM_force_field.poissonRatio, methods[2][1])
        self.assertEqual(
            elastic_object.remanence, methods[3][1])


def suite() -> unittest.TestSuite:
    suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestNormalBehavior,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    suite.addTests(loaded_tests)
    return suite
