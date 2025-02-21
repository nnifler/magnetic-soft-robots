import unittest
import unittest.mock

import numpy as np

from src import AnalysisParameters

from gui import MSRDeformationAnalysisWidget


class TestAnalysisParameters(unittest.TestCase):

    def test_init(self):
        ap = AnalysisParameters()
        self.assertFalse(ap.max_deformation_analysis)
        self.assertIsNone(ap.max_deformation_input)
        self.assertIsNone(ap.max_deformation_widget)

    def test_set_max_deformation_parameters_indices(self):
        selection_mode = MSRDeformationAnalysisWidget.SelectionMode.INDICES
        widget_args = {
            'get_mode.return_value': selection_mode,
            'SelectionMode.INDICES': MSRDeformationAnalysisWidget.SelectionMode.INDICES,
            'SelectionMode.COORDINATES': MSRDeformationAnalysisWidget.SelectionMode.COORDINATES,
            'SelectionMode.ALL': MSRDeformationAnalysisWidget.SelectionMode.ALL,
        }
        widget = unittest.mock.Mock(**widget_args)

        ap = AnalysisParameters()
        input_list = np.random.randint(3, size=(3,)).tolist()
        ap.set_max_deformation_parameters(widget, input_list)
        self.assertTrue(ap.max_deformation_analysis)
        self.assertEqual(ap.max_deformation_widget, widget)
        self.assertListEqual(ap.max_deformation_input, input_list)

    def test_set_max_deformation_parameters_coords(self):
        selection_mode = MSRDeformationAnalysisWidget.SelectionMode.COORDINATES
        widget_args = {
            'get_mode.return_value': selection_mode,
            'SelectionMode.INDICES': MSRDeformationAnalysisWidget.SelectionMode.INDICES,
            'SelectionMode.COORDINATES': MSRDeformationAnalysisWidget.SelectionMode.COORDINATES,
            'SelectionMode.ALL': MSRDeformationAnalysisWidget.SelectionMode.ALL,
        }
        widget = unittest.mock.Mock(**widget_args)

        ap = AnalysisParameters()
        input_list = [(np.random.rand(3) - 0.5) * 100 for _ in range(3)]
        ap.set_max_deformation_parameters(widget, input_list)
        self.assertTrue(ap.max_deformation_analysis)
        self.assertEqual(ap.max_deformation_widget, widget)
        self.assertListEqual(ap.max_deformation_input, input_list)

    def test_set_max_deformation_parameters_all(self):
        selection_mode = MSRDeformationAnalysisWidget.SelectionMode.ALL
        widget_args = {
            'get_mode.return_value': selection_mode,
            'SelectionMode.INDICES': MSRDeformationAnalysisWidget.SelectionMode.INDICES,
            'SelectionMode.COORDINATES': MSRDeformationAnalysisWidget.SelectionMode.COORDINATES,
            'SelectionMode.ALL': MSRDeformationAnalysisWidget.SelectionMode.ALL,
        }
        widget = unittest.mock.Mock(**widget_args)

        ap = AnalysisParameters()
        input_list = None
        ap.set_max_deformation_parameters(widget, input_list)
        self.assertTrue(ap.max_deformation_analysis)
        self.assertEqual(ap.max_deformation_widget, widget)
        self.assertIsNone(ap.max_deformation_input)

    def test_set_max_deformation_parameters_exceptional(self):
        selection_mode = MSRDeformationAnalysisWidget.SelectionMode.INDICES
        widget_args = {
            'get_mode.return_value': selection_mode,
            'SelectionMode.INDICES': MSRDeformationAnalysisWidget.SelectionMode.INDICES,
            'SelectionMode.COORDINATES': MSRDeformationAnalysisWidget.SelectionMode.COORDINATES,
            'SelectionMode.ALL': MSRDeformationAnalysisWidget.SelectionMode.ALL,
        }
        widget = unittest.mock.Mock(**widget_args)

        ap = AnalysisParameters()
        input_list = None
        with self.assertRaises(ValueError):
            ap.set_max_deformation_parameters(widget, input_list)

    def test_disable_max_deformation_analysis(self):
        selection_mode = MSRDeformationAnalysisWidget.SelectionMode.INDICES
        widget_args = {
            'get_mode.return_value': selection_mode,
            'SelectionMode.INDICES': MSRDeformationAnalysisWidget.SelectionMode.INDICES,
            'SelectionMode.COORDINATES': MSRDeformationAnalysisWidget.SelectionMode.COORDINATES,
            'SelectionMode.ALL': MSRDeformationAnalysisWidget.SelectionMode.ALL,
        }
        widget = unittest.mock.Mock(**widget_args)

        ap = AnalysisParameters()
        input_list = np.random.randint(3, size=(3,)).tolist()
        ap.set_max_deformation_parameters(widget, input_list)

        ap.disable_max_deformation_analysis()
        self.assertFalse(ap.max_deformation_analysis)
        self.assertIsNone(ap.max_deformation_input)
        self.assertIsNone(ap.max_deformation_widget)


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestAnalysisParameters,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
