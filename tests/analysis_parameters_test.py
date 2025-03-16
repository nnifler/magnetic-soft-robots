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

        self.assertFalse(ap._stress_analysis)
        self.assertIsNone(ap._stress_widget)

    def test_enable_max_deformation_analysis_indices(self):
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
        ap.enable_max_deformation_analysis(widget, input_list)
        self.assertTrue(ap.max_deformation_analysis)
        self.assertEqual(ap.max_deformation_widget, widget)
        self.assertListEqual(ap.max_deformation_input, input_list)

    def test_enable_max_deformation_analysis_coords(self):
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
        ap.enable_max_deformation_analysis(widget, input_list)
        self.assertTrue(ap.max_deformation_analysis)
        self.assertEqual(ap.max_deformation_widget, widget)
        self.assertListEqual(ap.max_deformation_input, input_list)

    def test_enable_max_deformation_analysis_all(self):
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
        ap.enable_max_deformation_analysis(widget, input_list)
        self.assertTrue(ap.max_deformation_analysis)
        self.assertEqual(ap.max_deformation_widget, widget)
        self.assertIsNone(ap.max_deformation_input)

    def test_enable_max_deformation_analysis_exceptional(self):
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
            ap.enable_max_deformation_analysis(widget, input_list)

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
        ap.enable_max_deformation_analysis(widget, input_list)

        ap.disable_max_deformation_analysis()
        self.assertFalse(ap.max_deformation_analysis)
        self.assertIsNone(ap.max_deformation_input)
        self.assertIsNone(ap.max_deformation_widget)

    def test_stress_enable(self):
        uut = AnalysisParameters()
        widget_mock = unittest.mock.MagicMock()
        uut.enable_stress_analysis(widget_mock)

        self.assertTrue(uut.stress_analysis,
                        "stress_analysis should be True after enabling")
        self.assertEqual(uut.stress_widget, widget_mock,
                         "stress_widget is not given as provided")

    def test_stress_disable(self):
        uut = AnalysisParameters()
        uut.disable_stress_analysis()
        self.assertFalse(uut.stress_analysis,
                         "stress_analysis should be False after disabling")
        with self.assertRaises(ValueError, msg="not raised ValueError for undefined widget"):
            _ = uut.stress_widget

    def test_stress_enable_errors(self):
        mock_no_min, mock_no_max = unittest.mock.MagicMock(), unittest.mock.MagicMock()
        del mock_no_max.set_max
        del mock_no_min.set_min
        erroneous_widgets = [
            None,
            mock_no_min,
            mock_no_max,
        ]
        for widget in erroneous_widgets:
            with self.assertRaises(ValueError):
                AnalysisParameters().enable_stress_analysis(widget)


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
