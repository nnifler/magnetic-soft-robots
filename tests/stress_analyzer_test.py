import unittest
import unittest.mock
import numpy as np

from src import StressAnalyzer, AnalysisParameters


class TestStressAnalyzer(unittest.TestCase):
    def test_regular_behaviour(self):
        eo_mock = unittest.mock.MagicMock()
        von_mises_vals = [
            [0]*5,
            [1]*5,
            [-0.3]*5,
            [3.8]*7,
            [5, 5, 5, 7.2, 5],
            [4.5]*5,
        ]

        type(eo_mock.FEM_force_field.vonMisesPerNode).value = unittest.mock.PropertyMock(
            side_effect=von_mises_vals
        )

        params = AnalysisParameters(unittest.mock.Mock())
        params.enable_stress_analysis()

        uut = StressAnalyzer(elastic_object=eo_mock, parameters=params)
        for _ in range(len(von_mises_vals)):
            uut.onAnimateBeginEvent(None)

        self.assertAlmostEqual(7.2, uut.max_stress)
        self.assertAlmostEqual(-0.3, uut.min_stress)

    def test_none_args(self):
        mock = unittest.mock.Mock()
        with self.assertRaises(ValueError):
            StressAnalyzer(None, None)
        with self.assertRaises(ValueError):
            StressAnalyzer(mock, None)
        with self.assertRaises(ValueError):
            StressAnalyzer(None, mock)

    def test_no_change(self):
        params = AnalysisParameters(unittest.mock.Mock())
        params.disable_stress_analysis()
        eo_mock = unittest.mock.MagicMock()

        uut = StressAnalyzer(eo_mock, params)
        uut.onAnimateBeginEvent(None)

        eo_mock.assert_not_called()


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestStressAnalyzer
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
