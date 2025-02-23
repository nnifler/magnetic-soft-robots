import unittest
import unittest.mock
import numpy as np

from src import StressAnalyzer


class TestStressAnalyzer(unittest.TestCase):
    def test_regular_behaviour(self):
        eo_mock = unittest.mock.MagicMock()
        von_mises_vals = [
            # "dummy call",
            [0]*5,
            [1]*5,
            [-0.3]*5,
            [3.8]*7,
            [5] * 5,
            [4.5]*5,
        ]

        type(eo_mock.FEM_force_field.vonMisesPerNode).value = unittest.mock.PropertyMock(
            side_effect=von_mises_vals
        )

        # print(eo_mock.FEM_force_field.vonMisesPerNode.value)

        para_mock = unittest.mock.MagicMock()
        para_mock.stress_analysis = True

        uut = StressAnalyzer(elastic_object=eo_mock, parameters=para_mock)
        for _ in range(len(von_mises_vals)):
            uut.onAnimateBeginEvent(None)

        self.assertEqual(5, uut.max_stress)
        self.assertAlmostEqual(-0.3, uut.min_stress)


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
