import unittest
import unittest.mock

import numpy as np
from PySide6.QtWidgets import QLabel

from gui.msr_stress_analysis_widget import MSRStressAnalysisWidget, MSRHeatmap, MSRHeatmapBar


class TestHeatmapWidget(unittest.TestCase):
    def test_defaults(self):
        uut = MSRHeatmap(unittest.mock.Mock())

        self.assertTrue(isinstance(uut._heatmap, MSRHeatmapBar))
        self.assertTrue(isinstance(uut._min_label, QLabel))
        self.assertTrue(isinstance(uut._max_label, QLabel))

        self.assertTrue("min: tbd" in uut._min_label)
        self.assertTrue("max: tbd" in uut._max_label)

    def test_min(self):
        uut = MSRHeatmap(unittest.mock.Mock())


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestHeatmapWidget
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
