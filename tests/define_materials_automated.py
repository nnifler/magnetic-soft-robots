import numpy as np
import unittest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
# from PySide6.QtTest import QTest

import gui
from src.units import YoungsModulus


class TestYoungModulus(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.app = QApplication([])
        self.uut_main_window = gui.MainWindow()
        self.uut_mat_group = self.uut_main_window.material_group
        self.uut_params = self.uut_mat_group.parameters

        self.ym = self.uut_params["youngs_modulus"]
        self.ref_unit_list = ["GPa", "hPa", "MPa", "Pa"]
        self.ref_getter_list = [YoungsModulus.GPa, YoungsModulus.hPa,
                                YoungsModulus.MPa, YoungsModulus.Pa]

    def tearDown(self):
        super().tearDown()
        self.app.shutdown()

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
            rejection of values below zero

        """

    def testLabel(self):
        self.assertTrue("Young's Modulus" in self.ym.label.text(),
                        "label not clear")

    def testDefaultUnit(self):
        self.assertTrue(self.ym.unit_selector.currentText()
                        == "GPa", "wrong default unit")

    def testUnitSelection(self):
        actual_unit_list = [self.ym.unit_selector.itemText(i)
                            for i in range(self.ym.unit_selector.count())]

        self.assertTrue(set(actual_unit_list) == set(
            self.ref_unit_list), "different content in selectable units")
        self.assertTrue(len(actual_unit_list) == len(
            self.ref_unit_list), "different len in selectable units")

    def testOkValueRange(self):
        # TODO: actual range is til 1e12; overflow errors
        lower_test_inputs = np.random.uniform(low=0, high=1e4, size=10)
        # test_inputs = np.random.uniform(low=0, high=1e12, size=10)

        # QTest.keyClicks(ym.spinbox, "21.36748")
        # TODO: this is not okay! we want to test user inputs
        self.ym.spinbox.setValue(21.36748)
        self.assertAlmostEqual(float(self.ym.spinbox.value()), 21.3675,
                               msg=f"dummy test 21.3675 = {self.ym.spinbox.text()} fails")

        for ref in [*lower_test_inputs]:
            # QTest.keyClicks(ym.spinbox, self.keys_from_float(ref))
            self.ym.spinbox.setValue(ref)
            self.assertAlmostEqual(self.ym.spinbox.value(), round(ref, 4),
                                   msg=f"input in legal range with 4 digit rounding fails, {ref}")

    def testInvalidRange(self):
        init_ref = 123456789
        self.ym.spinbox.setValue(init_ref)
        lower_test_inputs = np.random.uniform(low=0, high=1e4, size=10)

        for ref in -1*[*lower_test_inputs]:
            # QTest.keyClicks(ym.spinbox, self.keys_from_float(ref))
            self.ym.spinbox.setValue(ref)
            self.assertAlmostEqual(
                self.ym.spinbox.value(), init_ref, msg="negative input succeeds")

    def testUnitSwitch(self):
        lower_test_inputs = np.random.uniform(low=0, high=1e4, size=10)

        for ref_init_val in [*lower_test_inputs]:
            self.ym.spinbox.setValue(ref_init_val)
            ref_ym = YoungsModulus.from_GPa(round(ref_init_val, 4))

            for i, ref_tuple in enumerate(zip(self.ref_unit_list, self.ref_getter_list)):
                ref_unit = ref_tuple[0]
                ref_getter = ref_tuple[1]
                ref_val = round(ref_getter.fget(ref_ym), 4)

                # automatically select each unit in the combo box:
                # QTest.keyClicks(self.ym.unit_selector, ref_unit)
                # self.ym.unit_selector.setCurrentIndex(i)
                self.ym.unit_selector.setCurrentText(ref_unit)
                actual_value = self.ym.spinbox.value()

                self.assertEqual(
                    ref_unit,
                    self.ym.unit_selector.currentText(),
                    msg=f"unit selection {i} failed"
                )

                self.assertAlmostEqual(
                    ref_val,
                    actual_value,
                    msg=f"value conversion fails from {ref_ym.GPa} GPa to {ref_unit} using {ref_getter.fget.__name__}")

                # for code coverage of value method:
                self.assertAlmostEqual(
                    round(ref_ym.GPa, 4),
                    self.ym.value().GPa,
                    msg="value func of MSRMaterialParameter fails"
                )


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestYoungModulus,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
