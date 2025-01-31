import numpy as np
import unittest
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest

import gui
from src.units import YoungsModulus


class TestDefineMateials(unittest.TestCase):
    def setUp(self):
        super().setUp()
        app = QApplication([])
        self.uut_main_window = gui.MainWindow()
        self.uut_mat_group = self.uut_main_window.material_group
        self.uut_params = self.uut_mat_group.parameters

    def testYoungsModulus(self):
        """3. Input field with label for Young modulus: \n
            a. Input of positive values with up to four decimal digits possible \n
            b. Input of invalid characters not possible (negative numbers, non-numeric characters except comma or dot for decimal separator) \n\n

            checked for:
            default unit
            using 4 digits 
            provided unit selection
            text in associated label
            unit conversion
            success of values in range

        """
        ym = self.uut_params["youngs_modulus"]
        ref_unit_list = ["GPa", "Pa", "hPa", "MPa"]
        ref_getter_list = [YoungsModulus.GPa, YoungsModulus.Pa,
                           YoungsModulus.hPa, YoungsModulus.MPa]

        # "with label for YM"
        self.assertTrue("Young's Modulus" in ym.label.text(),
                        "label not clear")

        self.assertTrue(ym.unit_selector.currentText()
                        == "GPa", "wrong default unit")

        actual_unit_list = [ym.unit_selector.itemText(i)
                            for i in range(ym.unit_selector.count())]

        self.assertTrue(set(actual_unit_list) == set(
            ref_unit_list), "different content in selectable units")
        self.assertTrue(len(actual_unit_list) == len(
            ref_unit_list), "different len in selectable units")

        test_inputs = np.random.uniform(low=0, high=1e12, size=10)

        for ref_init_val in [*test_inputs]:
            ym.spinbox.setValue(ref_init_val)
            ref_ym = YoungsModulus.from_GPa(ref_init_val)

            for ref_unit, ref_getter in zip(ref_unit_list, ref_getter_list):
                ref_val = round(ref_getter.fget(ref_ym), 4)

                # automatically select each unit in the combo box:
                QTest.keyClicks(ym.unit_selector, ref_unit)
                actual_value = ym.spinbox.value()

                self.assertAlmostEqual(
                    ref_val, actual_value, msg=f"Value conversion fails for {ref_unit} using {ref_getter}")
                # for code coverage of value method:
                self.assertAlmostEqual(round(ref_ym.GPa, 4), ym.value(
                ).GPa, msg="value func of MSRMaterialParameter fails")


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestDefineMateials,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
