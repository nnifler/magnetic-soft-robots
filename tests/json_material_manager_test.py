import json
import os
from pathlib import Path
from random import randint, uniform
import unittest

from src import JsonMaterialManager
from src.units import Tesla, Density, YoungsModulus


class TestJsonMaterialManager(unittest.TestCase):

    def test_default_generation(self):
        # Checks for windows, as calculations are slightly different on windows.
        # Since reading out bytes cannot account for this, we skip this test on windows.
        operating_system = os.name
        if operating_system == 'nt':
            return

        json_path = Path(__file__).parents[1] / 'lib/materials/default.json'
        json_ref_path = Path(__file__).parent / \
            'assets/json_material_manager_test/default.json'
        json_ref = json_ref_path.read_bytes()
        JsonMaterialManager.save_default_materials()
        json_data = json_path.read_bytes()
        self.assertEqual(json_data, json_ref)

    def test_append_material(self):
        uut = JsonMaterialManager()
        density = Density.from_kgpm3(randint(1, 100))
        youngs_modulus = YoungsModulus.from_Pa(randint(1, 100))
        poissons_ratio = randint(1, 100)
        remanence = Tesla.from_T(randint(1, 100))

        uut.append_material('test', density, youngs_modulus,
                            poissons_ratio, remanence)
        self.assertEqual(uut.materials[0]['name'], 'test')
        self.assertEqual(uut.materials[0]['density'],
                         density.kgpm3)
        self.assertEqual(
            uut.materials[0]['youngs_modulus'], youngs_modulus.Pa)
        self.assertEqual(uut.materials[0]['poissons_ratio'], poissons_ratio)
        self.assertEqual(uut.materials[0]['remanence'], remanence.T)

    def test_save_to_json(self):
        uut = JsonMaterialManager()
        density = Density.from_kgpm3(randint(1, 100))
        youngs_modulus = YoungsModulus.from_Pa(randint(1, 100))
        poissons_ratio = randint(1, 100)
        remanence = Tesla.from_T(randint(1, 100))

        uut.append_material('test', density, youngs_modulus,
                            poissons_ratio, remanence)
        json_path = Path(__file__).parent / \
            'assets/json_material_manager_test/abc.json'
        uut.save_to_json(json_path)
        with open(json_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            self.assertEqual(json_data[0]['name'], 'test')
            self.assertEqual(json_data[0]['density'], density.kgpm3)
            self.assertEqual(json_data[0]['youngs_modulus'], youngs_modulus.Pa)
            self.assertEqual(json_data[0]['poissons_ratio'], poissons_ratio)
            self.assertEqual(json_data[0]['remanence'], remanence.T)

    def test_calculate_mean_normal_behavior(self):
        uut = JsonMaterialManager()
        values = [uniform(1, 100) for _ in range(2)]
        ref_mean = sum(values) / len(values)
        range_str = '-'.join(map(str, values))
        self.assertAlmostEqual(uut._calculate_mean(range_str), ref_mean)

    def test_calculate_mean_exceptional_behavior(self):
        uut = JsonMaterialManager()
        values = [uniform(1, 100) for _ in range(3)]
        range_str = '-'.join(map(str, values))
        with self.assertRaises(ValueError):
            uut._calculate_mean(range_str)


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestJsonMaterialManager,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
