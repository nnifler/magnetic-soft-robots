import unittest
import unittest.mock

import numpy as np
from PySide6.QtWidgets import QLabel, QApplication
from PySide6.QtGui import QColor

from gui.main_window import MainWindow
from gui.msr_stress_analysis_widget import MSRHeatmapBar

from src.units import YoungsModulus


class TestGradient(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.app = QApplication([])
        self.uut_main_window = MainWindow()
        self.uut = self.uut_main_window.stress_analysis._heatmap._heatmap

    def tearDown(self):
        super().tearDown()
        self.app.shutdown()

    def test_gradient(self):
        img = self.uut.grab().toImage()
        self.assertTrue(img.pixelColor(0, 0), QColor("red"))


class TestHeatmapWidget(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.app = QApplication([])
        self.uut_main_window = MainWindow()
        self.uut = self.uut_main_window.stress_analysis._heatmap

    def tearDown(self):
        super().tearDown()
        self.app.shutdown()

    def test_defaults(self):
        uut = self.uut

        self.assertTrue(isinstance(uut._heatmap, MSRHeatmapBar))
        self.assertTrue(isinstance(uut._min_label, QLabel))
        self.assertTrue(isinstance(uut._max_label, QLabel))

        self.assertTrue("min: tbd" in uut._min_label.text())
        self.assertTrue("max: tbd" in uut._max_label.text())

    def test_min(self):
        uut = self.uut
        input_val = np.random.uniform(0, 100, None)

        uut.set_max(input_val + 10)
        with self.assertRaises(ValueError, msg="no ValueError when min higher than max"):
            uut.set_min(input_val + 20)

        uut.set_min(input_val)
        self.assertEqual(
            f"min: {round(YoungsModulus.from_Pa(input_val).Pa, 2)} Pa",
            uut._min_label.text(),
            msg=str(input_val))

        with self.assertRaises(ValueError, msg="no ValueError when min higher than previous min"):
            uut.set_min(input_val + 1)

        with self.assertRaises(ValueError, msg="no ValueError with negative input"):
            uut.set_min(-1)

    def test_max(self):
        uut = self.uut
        input_val = np.random.uniform(20.1, 10000, None)

        uut.set_min(input_val - 10)
        with self.assertRaises(ValueError, msg="no ValueError when max lower than min"):
            uut.set_max(input_val - 20)

        uut.set_max(input_val)
        self.assertEqual(
            f"max: {round(YoungsModulus.from_Pa(input_val).MPa, 2)} MPa",
            uut._max_label.text(),
            msg=str(input_val))

        with self.assertRaises(ValueError, msg="no ValueError when max lower than previous max"):
            uut.set_max(input_val - 1)

        with self.assertRaises(ValueError, msg="no ValueError with negative input"):
            uut.set_max(-1)


class TestStressWidget(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.app = QApplication([])
        self.uut_main_window = MainWindow()
        self.uut = self.uut_main_window.stress_analysis

    def tearDown(self):
        super().tearDown()
        self.app.shutdown()

    def test_max(self):
        uut = self.uut
        input_val = np.random.uniform(20.1, 10000, None)

        uut.set_min(input_val - 10)
        with self.assertRaises(ValueError, msg="no ValueError when max lower than min"):
            uut.set_max(input_val - 20)

        uut.set_max(input_val)
        self.assertEqual(
            f"max: {round(YoungsModulus.from_Pa(input_val).MPa, 2)} MPa",
            uut._heatmap._max_label.text(),
            msg=str(input_val))

        with self.assertRaises(ValueError, msg="no ValueError when max lower than previous max"):
            uut.set_max(input_val - 1)

        with self.assertRaises(ValueError, msg="no ValueError with negative input"):
            uut.set_max(-1)

    def test_min(self):
        uut = self.uut
        input_val = np.random.uniform(0, 100, None)

        uut.set_max(input_val + 10)
        with self.assertRaises(ValueError, msg="no ValueError when min higher than max"):
            uut.set_min(input_val + 20)

        uut.set_min(input_val)
        self.assertEqual(
            f"min: {round(YoungsModulus.from_Pa(input_val).Pa, 2)} Pa",
            uut._heatmap._min_label.text(),
            msg=str(input_val))

        with self.assertRaises(ValueError, msg="no ValueError when min higher than previous min"):
            uut.set_min(input_val + 1)

        with self.assertRaises(ValueError, msg="no ValueError with negative input"):
            uut.set_min(-1)

    def test_show_stress(self):
        uut = self.uut
        self.assertFalse(uut.show_stress)

        uut._stress_checkbox.setChecked(True)
        self.assertTrue(uut.show_stress)

        uut._stress_checkbox.setChecked(False)
        self.assertFalse(uut.show_stress)


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestGradient,
        TestHeatmapWidget,
        TestStressWidget,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
