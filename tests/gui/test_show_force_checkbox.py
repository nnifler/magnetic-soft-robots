import unittest

import numpy as np
from PySide6.QtWidgets import QApplication

from src import Config
from gui.main_window import MainWindow


class TestShowForceCheckbox(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.app = QApplication([])
        self.uut_main_window = MainWindow()
        self.uut_main_window._very_secret_bool_to_stop_sofa_for_tests = True
        self.uut = self.uut_main_window._show_force_checkbox

    def tearDown(self):
        super().tearDown()
        self.app.shutdown()

    def test_default(self):
        self.assertFalse(self.uut.isChecked(), "should be turnt off")

    def test_regular_behaviour(self):
        data = np.random.uniform(-10, 10, 5)
        for d in data:
            b: bool = d > 0
            self.uut.setChecked(b)
            self.uut_main_window.apply_parameters()
            self.assertEqual(b, Config.get_show_force())


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestShowForceCheckbox,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
