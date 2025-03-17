import unittest
import unittest.mock

from pathlib import Path
import numpy as np
import Sofa

from src import (SimulationAnalyser, MeshLoader, ElasticObject,
                 Config, SimulationAnalysisController, AnalysisParameters)
from src import sofa_instantiator
from src.mesh_loader import Mode
from src.units import YoungsModulus, Density

from gui import MSRDeformationAnalysisWidget


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

    def test_nearest_node_exceptional(self):
        positions = [
            np.random.rand(1),
            np.random.rand(2),
            np.random.rand(6),
            np.random.rand(3, 2)
        ]

        for pos in positions:
            with self.assertRaises(ValueError):
                self.analyser.calculate_nearest_node(pos)

    @classmethod
    def tearDownClass(cls):
        Config.reset()


class TestDeformation(unittest.TestCase):
    def setUp(self):
        Config.set_test_env()

        self.root = Sofa.Core.Node("root")
        self.root.addObject(
            "RequiredPlugin", pluginName=Config.get_plugin_list())

        mesh_loader = MeshLoader()
        mesh_loader.load_file(
            Path("tests/assets/simulation_analyser_test/beam.msh"), Mode.VOLUMETRIC)
        mesh_loader.load_file(
            Path("tests/assets/simulation_analyser_test/beam.stl"), Mode.SURFACE)

        self.eo = ElasticObject(
            self.root, mesh_loader, 0.3, YoungsModulus.from_Pa(0), Density.from_kgpm3(0))

        self.initial_positions = self.eo.mech_obj.position.value.copy()

        self.analyser = SimulationAnalyser(self.root)

    def test_deformation_full(self):
        positions = self.eo.mech_obj.position.value
        random_deformation = (np.random.rand(len(positions), 3) - 0.5) * 10

        maxima = random_deformation.max(axis=0)
        minima = random_deformation.min(axis=0)
        max_min = np.stack((maxima, minima))

        maxima_ind = random_deformation.argmax(axis=0)
        minima_ind = random_deformation.argmin(axis=0)
        max_min_ind = np.stack((maxima_ind, minima_ind))

        self.eo.mech_obj.position = (positions + random_deformation).tolist()
        self.analyser.update_deformation()
        values, indices = self.analyser.calculate_deformation()
        np.testing.assert_allclose(values, max_min)
        np.testing.assert_allclose(indices, max_min_ind)

    def test_deformation_selective(self):
        positions = self.eo.mech_obj.position.value
        random_deformation = (np.random.rand(len(positions), 3) - 0.5) * 10

        points = list(range(len(positions)))
        random_points = np.random.choice(points, 10, replace=False)
        deformation_to_analyse = random_deformation[random_points]

        maxima = deformation_to_analyse.max(axis=0)
        minima = deformation_to_analyse.min(axis=0)
        max_min = np.stack((maxima, minima))

        points_arr = np.array(random_points)
        maxima_ind = points_arr[deformation_to_analyse.argmax(axis=0)]
        minima_ind = points_arr[deformation_to_analyse.argmin(axis=0)]
        max_min_ind = np.stack((maxima_ind, minima_ind))

        self.eo.mech_obj.position = (positions + random_deformation).tolist()
        self.analyser.update_deformation()
        values, indices = self.analyser.calculate_deformation(
            random_points.tolist())
        np.testing.assert_allclose(values, max_min)
        np.testing.assert_allclose(indices, max_min_ind)

    def test_max_deformation_full(self):
        positions = self.eo.mech_obj.position.value
        random_deformation = (np.random.rand(len(positions), 3) - 0.5) * 10

        maxima = random_deformation.max(axis=0)

        maxima_ind = random_deformation.argmax(axis=0)

        self.eo.mech_obj.position = (positions + random_deformation).tolist()
        self.analyser.update_deformation()
        values, indices = self.analyser.calculate_maximum_deformation()
        np.testing.assert_allclose(values, maxima)
        np.testing.assert_allclose(indices, maxima_ind)

    def test_max_deformation_selective(self):
        positions = self.eo.mech_obj.position.value
        random_deformation = (np.random.rand(len(positions), 3) - 0.5) * 10

        points = list(range(len(positions)))
        random_points = np.random.choice(points, 10, replace=False)
        deformation_to_analyse = random_deformation[random_points]

        maxima = deformation_to_analyse.max(axis=0)

        points_arr = np.array(random_points)
        maxima_ind = points_arr[deformation_to_analyse.argmax(axis=0)]

        self.eo.mech_obj.position = (positions + random_deformation).tolist()
        self.analyser.update_deformation()
        values, indices = self.analyser.calculate_maximum_deformation(
            random_points.tolist())
        np.testing.assert_allclose(values, maxima)
        np.testing.assert_allclose(indices, maxima_ind)

    def test_min_deformation_full(self):
        positions = self.eo.mech_obj.position.value
        random_deformation = (np.random.rand(len(positions), 3) - 0.5) * 10

        minima = random_deformation.min(axis=0)

        minima_ind = random_deformation.argmin(axis=0)

        self.eo.mech_obj.position = (positions + random_deformation).tolist()
        self.analyser.update_deformation()
        values, indices = self.analyser.calculate_minimum_deformation()
        np.testing.assert_allclose(values, minima)
        np.testing.assert_allclose(indices, minima_ind)

    def test_min_deformation_selective(self):
        positions = self.eo.mech_obj.position.value
        random_deformation = (np.random.rand(len(positions), 3) - 0.5) * 10

        points = list(range(len(positions)))
        random_points = np.random.choice(points, 10, replace=False)
        deformation_to_analyse = random_deformation[random_points]

        minima = deformation_to_analyse.min(axis=0)

        points_arr = np.array(random_points)
        minima_ind = points_arr[deformation_to_analyse.argmin(axis=0)]

        self.eo.mech_obj.position = (positions + random_deformation).tolist()
        self.analyser.update_deformation()
        values, indices = self.analyser.calculate_minimum_deformation(
            random_points.tolist())
        np.testing.assert_allclose(values, minima)
        np.testing.assert_allclose(indices, minima_ind)

    def test_deformation_multiple_changes(self):
        positions = self.eo.mech_obj.position.value
        random_deformations = (np.random.rand(4, len(positions), 3) - 0.5) * 10

        deformation_steps = np.array([
            random_deformations[0],
            random_deformations[0:2].sum(axis=0),
            random_deformations[0:3].sum(axis=0),
            random_deformations.sum(axis=0)
        ])
        max_deformations = deformation_steps.max(axis=0)
        min_deformations = deformation_steps.min(axis=0)

        maxima = max_deformations.max(axis=0)
        minima = min_deformations.min(axis=0)
        max_min = np.stack((maxima, minima))

        maxima_ind = max_deformations.argmax(axis=0)
        minima_ind = min_deformations.argmin(axis=0)
        max_min_ind = np.stack((maxima_ind, minima_ind))

        for random_deformation in random_deformations:
            self.eo.mech_obj.position = (
                positions + random_deformation).tolist()
            positions = self.eo.mech_obj.position.value
            self.analyser.update_deformation()

        values, indices = self.analyser.calculate_deformation()
        np.testing.assert_allclose(values, max_min)
        np.testing.assert_allclose(indices, max_min_ind)

    def test_deformation_exceptional(self):
        positions = self.eo.mech_obj.position.value

        points = list(range(len(positions)))
        random_points = np.random.choice(points, 10, replace=False)
        wrong_point = np.random.randint(len(positions), len(positions) * 2)
        random_points = np.append(random_points, wrong_point)
        np.random.shuffle(random_points)

        # Test empty list
        with self.assertRaises(ValueError):
            self.analyser.calculate_deformation([])

        # Test point not in model
        with self.assertRaises(ValueError):
            self.analyser.calculate_deformation(random_points.tolist())

    @classmethod
    def tearDown(cls):
        Config.reset()


class TestAnalysisController(unittest.TestCase):

    @classmethod
    def setUp(cls):
        Config.reset()
        Config.set_test_env()
        Config.set_model('beam', 1)

    def test_init_deform_indices(self):
        selection_mode = MSRDeformationAnalysisWidget.SelectionMode.INDICES
        widget_args = {
            'get_mode.return_value': selection_mode,
            'SelectionMode.INDICES': MSRDeformationAnalysisWidget.SelectionMode.INDICES,
            'SelectionMode.COORDINATES': MSRDeformationAnalysisWidget.SelectionMode.COORDINATES,
            'SelectionMode.ALL': MSRDeformationAnalysisWidget.SelectionMode.ALL,
        }
        widget = unittest.mock.Mock(**widget_args)

        deform_input = np.random.randint(100, size=(25,)).tolist()

        parameters = AnalysisParameters(unittest.mock.Mock())
        parameters.enable_max_deformation_analysis(widget, deform_input)
        Config.set_analysis_parameters(parameters)

        root = Sofa.Core.Node("root")
        sofa_instantiator.createScene(root)

        controller: SimulationAnalysisController = root.getObject(
            'AnalysisController')

        self.assertTrue(controller.max_deformation_analysis)
        self.assertListEqual(controller.max_deformation_input, deform_input)
        self.assertEqual(controller.max_deformation_widget, widget)
        self.assertEqual(controller.max_deformation_mode, selection_mode)

    def test_init_deform_coords(self):
        selection_mode = MSRDeformationAnalysisWidget.SelectionMode.COORDINATES
        widget_args = {
            'get_mode.return_value': selection_mode,
            'SelectionMode.INDICES': MSRDeformationAnalysisWidget.SelectionMode.INDICES,
            'SelectionMode.COORDINATES': MSRDeformationAnalysisWidget.SelectionMode.COORDINATES,
            'SelectionMode.ALL': MSRDeformationAnalysisWidget.SelectionMode.ALL,
        }
        widget = unittest.mock.Mock(**widget_args)

        deform_input = [np.random.randint(10, size=(3,)) for _ in range(25)]

        parameters = AnalysisParameters(unittest.mock.Mock())
        parameters.enable_max_deformation_analysis(widget, deform_input)
        Config.set_analysis_parameters(parameters)

        root = Sofa.Core.Node("root")
        sofa_instantiator.createScene(root)
        analyser = SimulationAnalyser(root)

        controller: SimulationAnalysisController = root.getObject(
            'AnalysisController')

        self.assertTrue(controller.max_deformation_analysis)
        self.assertEqual(controller.max_deformation_widget, widget)
        self.assertEqual(controller.max_deformation_mode, selection_mode)

        ref_indices = [analyser.calculate_nearest_node(
            coord) for coord in deform_input]

        self.assertListEqual(controller.max_deformation_input, ref_indices)

    def test_simulation_behaviour_indices(self):
        deform_input = np.random.randint(100, size=(25,)).tolist()

        widget_args = {
            'get_mode.return_value': MSRDeformationAnalysisWidget.SelectionMode.INDICES,
            'SelectionMode.INDICES': MSRDeformationAnalysisWidget.SelectionMode.INDICES,
            'SelectionMode.COORDINATES': MSRDeformationAnalysisWidget.SelectionMode.COORDINATES,
            'SelectionMode.ALL': MSRDeformationAnalysisWidget.SelectionMode.ALL,
        }
        widget = unittest.mock.Mock(**widget_args)
        callpoint = unittest.mock.Mock()
        parameters = AnalysisParameters(callpoint)
        parameters.enable_max_deformation_analysis(widget, deform_input)
        Config.set_analysis_parameters(parameters)

        root = Sofa.Core.Node("root")
        sofa_instantiator.createScene(root)
        analyser = SimulationAnalyser(root)

        Sofa.Simulation.init(root)
        Sofa.Simulation.animate(root, root.dt.value)
        analyser.update_deformation()
        for _ in range(10):
            Sofa.Simulation.animate(root, root.dt.value)
            ref_values, ref_indices = analyser.calculate_deformation(
                deform_input)
            args = callpoint.send.call_args[0][0]
            callname, args = args
            self.assertEqual(callname, "deform_update")
            values = np.array(args[0])
            indices = np.array(args[1])

            ref_maxima = np.absolute(ref_values).argmax(axis=0)
            ref_values = np.array([
                ref_values[ref_maxima[0], 0],
                ref_values[ref_maxima[1], 1],
                ref_values[ref_maxima[2], 2],
            ])
            ref_indices = np.array([
                ref_indices[ref_maxima[0], 0],
                ref_indices[ref_maxima[1], 1],
                ref_indices[ref_maxima[2], 2],
            ])

            np.testing.assert_allclose(values, ref_values, atol=1e-6)
            np.testing.assert_allclose(indices, ref_indices)

            # Update after comparing controller output, because the controller
            # is apparently called before the actual simulation step
            analyser.update_deformation()

    def test_simulation_behaviour_all(self):
        widget_args = {
            'get_mode.return_value': MSRDeformationAnalysisWidget.SelectionMode.ALL,
            'SelectionMode.INDICES': MSRDeformationAnalysisWidget.SelectionMode.INDICES,
            'SelectionMode.COORDINATES': MSRDeformationAnalysisWidget.SelectionMode.COORDINATES,
            'SelectionMode.ALL': MSRDeformationAnalysisWidget.SelectionMode.ALL,
        }
        widget = unittest.mock.Mock(**widget_args)
        callpoint = unittest.mock.Mock()
        parameters = AnalysisParameters(callpoint)
        parameters.enable_max_deformation_analysis(widget, None)
        Config.set_analysis_parameters(parameters)

        root = Sofa.Core.Node("root")
        sofa_instantiator.createScene(root)
        analyser = SimulationAnalyser(root)

        Sofa.Simulation.init(root)
        Sofa.Simulation.animate(root, root.dt.value)
        analyser.update_deformation()
        for _ in range(10):
            Sofa.Simulation.animate(root, root.dt.value)
            ref_values, ref_indices = analyser.calculate_deformation()
            args = callpoint.send.call_args[0][0]
            callname, args = args
            self.assertEqual(callname, "deform_update")
            values = np.array(args[0])
            indices = np.array(args[1])

            ref_maxima = np.absolute(ref_values).argmax(axis=0)
            ref_values = np.array([
                ref_values[ref_maxima[0], 0],
                ref_values[ref_maxima[1], 1],
                ref_values[ref_maxima[2], 2],
            ])
            ref_indices = np.array([
                ref_indices[ref_maxima[0], 0],
                ref_indices[ref_maxima[1], 1],
                ref_indices[ref_maxima[2], 2],
            ])

            np.testing.assert_allclose(values, ref_values, atol=1e-6)
            np.testing.assert_allclose(indices, ref_indices)

            # Update after comparing controller output, because the controller
            # is apparently called before the actual simulation step
            analyser.update_deformation()

    def test_simulation_error(self):
        widget_args = {
            'get_mode.return_value': MSRDeformationAnalysisWidget.SelectionMode.INDICES,
            'SelectionMode.INDICES': MSRDeformationAnalysisWidget.SelectionMode.INDICES,
            'SelectionMode.COORDINATES': MSRDeformationAnalysisWidget.SelectionMode.COORDINATES,
            'SelectionMode.ALL': MSRDeformationAnalysisWidget.SelectionMode.ALL,
        }
        widget = unittest.mock.Mock(**widget_args)

        deform_input = [int(1e10)]
        callpoint = unittest.mock.Mock()
        parameters = AnalysisParameters(callpoint)
        parameters.enable_max_deformation_analysis(widget, deform_input)
        Config.set_analysis_parameters(parameters)

        root = Sofa.Core.Node("root")
        sofa_instantiator.createScene(root)

        Sofa.Simulation.init(root)
        Sofa.Simulation.animate(root, root.dt.value)

        callpoint.send.assert_called_with(
            ("deform_error", ['Point 10000000000 is not part of the model.']))
        # widget.update_results.assert_not_called()


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestAnalyserUtils,
        TestDeformation,
        TestAnalysisController,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
