import unittest
import unittest.mock

import numpy as np

from src import AnalysisParameters


class TestAnalysisParameters(unittest.TestCase):

    def test_init(self):
        ap = AnalysisParameters(unittest.mock.Mock())
        self.assertFalse(ap.max_deformation_analysis)
        self.assertIsNone(ap.max_deformation_input)
        self.assertIsNone(ap.max_deformation_mode)

        self.assertFalse(ap._stress_analysis)

    def test_enable_max_deformation_analysis_indices(self):
        selection_mode = AnalysisParameters.SelectionMode.INDICES

        ap = AnalysisParameters(unittest.mock.Mock())
        input_list = np.random.randint(3, size=(3,)).tolist()
        ap.enable_max_deformation_analysis(selection_mode, input_list)
        self.assertTrue(ap.max_deformation_analysis)
        self.assertEqual(ap.max_deformation_mode, selection_mode)
        self.assertListEqual(ap.max_deformation_input, input_list)

    def test_enable_max_deformation_analysis_coords(self):
        selection_mode = AnalysisParameters.SelectionMode.COORDINATES

        ap = AnalysisParameters(unittest.mock.Mock())
        input_list = [(np.random.rand(3) - 0.5) * 100 for _ in range(3)]
        ap.enable_max_deformation_analysis(selection_mode, input_list)
        self.assertTrue(ap.max_deformation_analysis)
        self.assertEqual(ap.max_deformation_mode, selection_mode)
        self.assertListEqual(ap.max_deformation_input, input_list)

    def test_enable_max_deformation_analysis_all(self):
        selection_mode = AnalysisParameters.SelectionMode.ALL

        ap = AnalysisParameters(unittest.mock.Mock())
        input_list = None
        ap.enable_max_deformation_analysis(selection_mode, input_list)
        self.assertTrue(ap.max_deformation_analysis)
        self.assertEqual(ap.max_deformation_mode, selection_mode)
        self.assertIsNone(ap.max_deformation_input)

    def test_enable_max_deformation_analysis_exceptional(self):
        selection_mode = AnalysisParameters.SelectionMode.INDICES

        ap = AnalysisParameters(unittest.mock.Mock())
        input_list = None
        with self.assertRaises(ValueError):
            ap.enable_max_deformation_analysis(selection_mode, input_list)

    def test_disable_max_deformation_analysis(self):
        selection_mode = AnalysisParameters.SelectionMode.INDICES

        ap = AnalysisParameters(unittest.mock.Mock())
        input_list = np.random.randint(3, size=(3,)).tolist()
        ap.enable_max_deformation_analysis(selection_mode, input_list)

        ap.disable_max_deformation_analysis()
        self.assertFalse(ap.max_deformation_analysis)
        self.assertIsNone(ap.max_deformation_input)
        self.assertIsNone(ap.max_deformation_mode)

    def test_stress_enable(self):
        uut = AnalysisParameters(unittest.mock.Mock())
        uut.enable_stress_analysis()

        self.assertTrue(uut.stress_analysis,
                        "stress_analysis should be True after enabling")

    def test_stress_disable(self):
        uut = AnalysisParameters(unittest.mock.Mock())
        uut.disable_stress_analysis()
        self.assertFalse(uut.stress_analysis,
                         "stress_analysis should be False after disabling")

    def test_error_on_init(self):
        with self.assertRaises(ValueError):
            AnalysisParameters(None)


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
