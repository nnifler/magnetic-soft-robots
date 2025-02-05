import unittest

from pathlib import Path
import numpy as np
import Sofa

from src import SimulationAnalyser, MeshLoader, ElasticObject, Config
from src.mesh_loader import Mode
from src.units import YoungsModulus, Density

# largest disatance: 0.125


class TestAnalyserUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Config.set_test_env()

        cls.root = Sofa.Core.Node("root")
        cls.root.addObject(
            "RequiredPlugin", pluginName=Config.get_plugin_list())

        mesh_loader = MeshLoader()
        mesh_loader.load_file(
            Path("tests/assets/simulation_analyser_test/beam.msh"), Mode.VOLUMETRIC)
        mesh_loader.load_file(
            Path("tests/assets/simulation_analyser_test/beam.stl"), Mode.SURFACE)

        cls.eo = ElasticObject(
            cls.root, mesh_loader, 0.3, YoungsModulus.from_Pa(0), Density.from_kgpm3(0))

        cls.analyser = SimulationAnalyser(cls.root)

    def test_nearest_node_exact(self):
        positions = self.eo.mech_obj.position.value
        random_index = np.random.randint(len(positions))
        self.assertEqual(random_index,
                         self.analyser.calculate_nearest_node(positions[random_index]))

    def test_nearest_node_approx(self):
        positions = self.eo.mech_obj.position.value
        random_index = np.random.randint(len(positions))
        # Since the maximum distance between points in the beam mesh is 0.125,
        # this point should always be nearest to the point at the index.
        random_point = positions[random_index] + \
            (np.random.rand(3) - 0.5) * 0.12
        self.assertEqual(random_index,
                         self.analyser.calculate_nearest_node(random_point))

    @classmethod
    def tearDownClass(cls):
        Config.reset()


class TestDeformation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Config.set_test_env()

        cls.root = Sofa.Core.Node("root")
        cls.root.addObject(
            "RequiredPlugin", pluginName=Config.get_plugin_list())

        mesh_loader = MeshLoader()
        mesh_loader.load_file(
            Path("tests/assets/simulation_analyser_test/beam.msh"), Mode.VOLUMETRIC)
        mesh_loader.load_file(
            Path("tests/assets/simulation_analyser_test/beam.stl"), Mode.SURFACE)

        cls.eo = ElasticObject(
            cls.root, mesh_loader, 0.3, YoungsModulus.from_Pa(0), Density.from_kgpm3(0))

        cls.initial_positions = cls.eo.mech_obj.position.value.copy()

        cls.analyser = SimulationAnalyser(cls.root)

    def test_deformation_full(self):
        positions = self.eo.mech_obj.position.value
        random_deformation = (np.random.rand(len(positions), 3) - 0.5) * 10

        maxima = random_deformation.max(axis=0)
        minima = random_deformation.min(axis=0)
        max_min = np.stack((maxima, minima))

        points = list(range(len(positions)))
        self.eo.mech_obj.position = (positions + random_deformation).tolist()
        np.testing.assert_allclose(
            self.analyser.calculate_deformation(points), max_min)

    def test_deformation_selective(self):
        positions = self.eo.mech_obj.position.value
        random_deformation = (np.random.rand(len(positions), 3) - 0.5) * 10

        points = list(range(len(positions)))
        random_points = np.random.choice(points, 10, replace=False)
        deformation_to_analyse = random_deformation[random_points]

        maxima = deformation_to_analyse.max(axis=0)
        minima = deformation_to_analyse.min(axis=0)
        max_min = np.stack((maxima, minima))

        self.eo.mech_obj.position = (positions + random_deformation).tolist()
        np.testing.assert_allclose(
            self.analyser.calculate_deformation(random_points), max_min)

    def test_max_deformation_full(self):
        positions = self.eo.mech_obj.position.value
        random_deformation = (np.random.rand(len(positions), 3) - 0.5) * 10

        maxima = random_deformation.max(axis=0)

        points = list(range(len(positions)))
        self.eo.mech_obj.position = (positions + random_deformation).tolist()
        np.testing.assert_allclose(
            self.analyser.calculate_maximum_deformation(points), maxima)

    def test_max_deformation_selective(self):
        positions = self.eo.mech_obj.position.value
        random_deformation = (np.random.rand(len(positions), 3) - 0.5) * 10

        points = list(range(len(positions)))
        random_points = np.random.choice(points, 10, replace=False)
        deformation_to_analyse = random_deformation[random_points]

        maxima = deformation_to_analyse.max(axis=0)

        self.eo.mech_obj.position = (positions + random_deformation).tolist()
        np.testing.assert_allclose(
            self.analyser.calculate_maximum_deformation(random_points), maxima)

    def test_min_deformation_full(self):
        positions = self.eo.mech_obj.position.value
        random_deformation = (np.random.rand(len(positions), 3) - 0.5) * 10

        minima = random_deformation.min(axis=0)

        points = list(range(len(positions)))
        self.eo.mech_obj.position = (positions + random_deformation).tolist()
        np.testing.assert_allclose(
            self.analyser.calculate_minimum_deformation(points), minima)

    def test_min_deformation_selective(self):
        positions = self.eo.mech_obj.position.value
        random_deformation = (np.random.rand(len(positions), 3) - 0.5) * 10

        points = list(range(len(positions)))
        random_points = np.random.choice(points, 10, replace=False)
        deformation_to_analyse = random_deformation[random_points]

        minima = deformation_to_analyse.min(axis=0)

        self.eo.mech_obj.position = (positions + random_deformation).tolist()
        np.testing.assert_allclose(
            self.analyser.calculate_minimum_deformation(random_points), minima)

    def tearDown(self):
        self.eo.mech_obj.position = self.initial_positions

    @classmethod
    def tearDownClass(cls):
        Config.reset()


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestAnalyserUtils,
        TestDeformation,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
