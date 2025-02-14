import unittest
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QDoubleSpinBox
# from PySide6.QtTest import QTest

import gui
from src.units import YoungsModulus, Density, Tesla


class TestYoungModulus(unittest.TestCase):
    """3. Input field with label for Young modulus: \n
            a. Input of positive values with up to four decimal digits possible \n
            b. Input of invalid characters not possible (negative numbers, non-numeric characters except comma or dot for decimal separator) \n\n

            checked for:
            default unit
            using 4 digits 
            provided unit selection
            text in associated label
            unit conversion from GPa initially
            success of values in range
            rejection of values below zero
            only input for numeric values allowed
        """

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
        lower_test_inputs = np.random.uniform(low=0, high=1e4, size=3)
        # test_inputs = np.random.uniform(low=0, high=1e12, size=3)

        # QTest.keyClicks(ym.spinbox, "21.36748")

        self.ym.spinbox.setValue(21.36748)
        self.assertAlmostEqual(float(self.ym.spinbox.value()), 21.3675,
                               msg=f"dummy test 21.3675 = {self.ym.spinbox.text()} fails")

        for ref in [*lower_test_inputs]:
            # QTest.keyClicks(ym.spinbox, self.keys_from_float(ref))
            self.ym.spinbox.setValue(ref)
            self.assertAlmostEqual(self.ym.spinbox.value(), round(ref, 4),
                                   msg=f"input in legal range with 4 digit rounding fails, {ref}")

    def testInvalidRange(self):
        self.assertTrue(
            isinstance(self.ym.spinbox, QDoubleSpinBox),
            "Spinbox not restricted to float values")
        init_ref = 123456789
        self.ym.spinbox.setValue(init_ref)
        lower_test_inputs = np.random.uniform(low=0, high=1e4, size=3)

        for ref in -1*[*lower_test_inputs]:
            # QTest.keyClicks(ym.spinbox, self.keys_from_float(ref))
            self.ym.spinbox.setValue(ref)
            self.assertAlmostEqual(
                self.ym.spinbox.value(), init_ref, msg="negative input succeeds")

    def testUnitSwitch(self):
        lower_test_inputs = np.random.uniform(low=0, high=1e4, size=3)

        for ref_init_val in [*lower_test_inputs]:
            self.ym.unit_selector.setCurrentText("GPa")
            self.ym.spinbox.setValue(ref_init_val)
            ref_ym = YoungsModulus.from_GPa(ref_init_val)
            for i, ref_tuple in enumerate(zip(self.ref_unit_list, self.ref_getter_list)):
                ref_unit = ref_tuple[0]
                ref_getter = ref_tuple[1]
                factor = YoungsModulus.UnitFactor[ref_unit].value / \
                    YoungsModulus.UnitFactor.GPa.value
                ref_val = round(ref_getter.fget(ref_ym) * factor, 4) / factor

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
                    places=1,
                    msg=f"value conversion fails from {ref_ym.GPa} GPa to {ref_unit} using {ref_getter.fget.__name__}")

                # for code coverage of value method:
                self.assertAlmostEqual(
                    round(ref_ym.GPa, 4),
                    self.ym.value().GPa,
                    msg="value func of MSRMaterialParameter fails"
                )


class TestDensity(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.app = QApplication([])
        self.uut_main_window = gui.MainWindow()
        self.uut_mat_group = self.uut_main_window.material_group
        self.uut_params = self.uut_mat_group.parameters

        self.density = self.uut_params["density"]
        self.ref_unit_list = ["kg/m³", "g/cm³", "Mg/m³", "t/m³"]
        self.ref_getter_list = [Density.kgpm3, Density.gpcm3,
                                Density.Mgpm3, Density.tpm3]
        self.ref_setter_list = [Density.from_kgpm3, Density.from_gpcm3,
                                Density.from_Mgpm3, Density.from_tpm3]

    def tearDown(self):
        super().tearDown()
        self.app.shutdown()

    def testLabel(self):
        self.assertTrue("Density" in self.density.label.text(),
                        "label not clear")

    def testDefaultUnit(self):
        self.assertTrue(self.density.unit_selector.currentText()
                        == "kg/m³", "wrong default unit")

    def testUnitSelection(self):
        actual_unit_list = [self.density.unit_selector.itemText(i)
                            for i in range(self.density.unit_selector.count())]

        self.assertTrue(set(actual_unit_list) == set(
            self.ref_unit_list), "different content in selectable units")
        self.assertTrue(len(actual_unit_list) == len(
            self.ref_unit_list), "different len in selectable units")

    def testOkValueRange(self):
        lower_test_inputs = np.random.uniform(low=0, high=30000, size=3)

        self.density.spinbox.setValue(21.36748)
        self.assertAlmostEqual(float(self.density.spinbox.value()), 21.37,
                               msg=f"dummy test 21.367 = {self.density.spinbox.text()} fails")

        for ref in [*lower_test_inputs]:
            self.density.spinbox.setValue(ref)
            self.assertAlmostEqual(self.density.spinbox.value(), round(ref, 2),
                                   msg=f"input in legal range with 2 digit rounding fails, {ref}")

    def testInvalidRange(self):
        self.assertTrue(
            isinstance(self.density.spinbox, QDoubleSpinBox),
            "Spinbox not restricted to float values")
        init_ref = 12345.67
        self.density.spinbox.setValue(init_ref)
        lower_test_inputs = np.random.uniform(low=0, high=30000, size=3)

        for ref in -1*[*lower_test_inputs]:
            self.density.spinbox.setValue(ref)
            self.assertAlmostEqual(
                self.density.spinbox.value(), init_ref, msg="negative input succeeds")

        for ref in [*lower_test_inputs]:
            ref += 30000
            self.density.spinbox.setValue(ref)
            self.assertAlmostEqual(
                self.density.spinbox.value(), 30000, msg="too large input succeeds")
            self.density.spinbox.setValue(init_ref)

    def testUnitSwitch(self):
        lower_test_inputs = np.random.uniform(low=1000, high=30000, size=3)

        for ref_init_val in [*lower_test_inputs]:
            self.density.unit_selector.setCurrentText("kg/m³")
            self.density.spinbox.setValue(ref_init_val)
            ref_density = Density.from_kgpm3(self.density.spinbox.value())
            for i, ref_tuple in enumerate(zip(self.ref_unit_list, self.ref_getter_list, self.ref_setter_list)):
                ref_unit = ref_tuple[0]
                ref_getter = ref_tuple[1]
                ref_setter = ref_tuple[2]

                ref_val = ref_getter.fget(ref_density)

                # make the change
                self.density.unit_selector.setCurrentText(ref_unit)
                actual_value = self.density.spinbox.value()

                self.assertEqual(
                    ref_unit,
                    self.density.unit_selector.currentText(),
                    msg=f"unit selection {i} failed"
                )

                self.assertAlmostEqual(
                    ref_val,
                    actual_value,
                    places=1,
                    msg=f"value conversion fails from {ref_density.kgpm3} kg/m³ to {ref_unit} using {ref_getter.fget.__name__}")

                # for code coverage of value method:

                if i == 0:
                    self.assertAlmostEqual(
                        round(ref_density.kgpm3, 2),
                        self.density.value().kgpm3,
                        msg="value func of MSRMaterialParameter fails"
                    )

                ref_density = ref_setter(self.density.spinbox.value())


class TestTesla(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.app = QApplication([])
        self.uut_main_window = gui.MainWindow()
        self.uut_mat_group = self.uut_main_window.material_group
        self.uut_params = self.uut_mat_group.parameters

        self.decimals = 3
        self.remanence = self.uut_params["remanence"]

    def tearDown(self):
        super().tearDown()
        self.app.shutdown()

    def testUnitSelection(self):
        self.assertTrue(isinstance(self.remanence.unit_selector, QLabel))

    def testLabel(self):
        self.assertTrue("Remanence" in self.remanence.label.text(),
                        "label not clear")

    def testDefaultUnit(self):
        self.assertTrue(self.remanence.unit_selector.text()
                        == "T", "wrong default unit")

    def testOkValueRange(self):
        lower_test_inputs = np.random.uniform(low=-2, high=2, size=3)

        self.remanence.spinbox.setValue(1.36748)
        self.assertAlmostEqual(float(self.remanence.spinbox.value()), 1.367,
                               msg=f"dummy test 1.3675 = {self.remanence.spinbox.text()} fails")

        for ref in [*lower_test_inputs]:
            self.remanence.spinbox.setValue(ref)
            self.assertAlmostEqual(self.remanence.spinbox.value(), round(ref, self.decimals),
                                   msg=f"input in legal range with {self.decimals} digit rounding fails, {ref}")

    def testInvalidRange(self):
        self.assertTrue(
            isinstance(self.remanence.spinbox, QDoubleSpinBox),
            "Spinbox not restricted to float values")
        init_ref = 1.67
        self.remanence.spinbox.setValue(init_ref)
        too_low_inputs = np.random.uniform(low=-1000, high=-2, size=3)
        too_high_inputs = np.random.uniform(low=2.01, high=2000, size=3)
        for ref in [*too_low_inputs]:
            self.remanence.spinbox.setValue(ref)
            self.assertAlmostEqual(
                self.remanence.spinbox.value(), -2, msg="too low input succeeds")
            self.remanence.spinbox.setValue(init_ref)

        for ref in [*too_high_inputs]:
            self.remanence.spinbox.setValue(ref)
            self.assertAlmostEqual(
                self.remanence.spinbox.value(), 2, msg="too large input succeeds")
            self.remanence.spinbox.setValue(init_ref)


class TestPoissonsRatio(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.app = QApplication([])
        self.uut_main_window = gui.MainWindow()
        self.uut_mat_group = self.uut_main_window.material_group
        self.uut_params = self.uut_mat_group.parameters

        self.decimals = 4
        self.poisson = self.uut_params["poissons_ratio"]

    def tearDown(self):
        super().tearDown()
        self.app.shutdown()

    def testUnitSelection(self):
        self.assertTrue(
            isinstance(self.poisson.unit_selector, QLabel)
            and self.poisson.unit_selector.text() == "",
            "should have a empty label only as no unit is defined")

    def testLabel(self):
        self.assertTrue("Poisson's Ratio" in self.poisson.label.text(),
                        "label not clear")

    def testOkValueRange(self):
        lower_test_inputs = np.random.uniform(low=0, high=0.4999, size=3)

        self.poisson.spinbox.setValue(0.36748)
        self.assertAlmostEqual(float(self.poisson.spinbox.value()), 0.3675,
                               msg=f"dummy test 0.3675 = {self.poisson.spinbox.text()} fails")

        for ref in [*lower_test_inputs]:
            self.poisson.spinbox.setValue(ref)
            self.assertAlmostEqual(self.poisson.spinbox.value(), round(ref, self.decimals),
                                   msg=f"input in legal range with {self.decimals} digit rounding fails, {ref}")

    def testInvalidRange(self):
        self.assertTrue(
            isinstance(self.poisson.spinbox, QDoubleSpinBox),
            "Spinbox not restricted to float values")
        init_ref = 1.67
        self.poisson.spinbox.setValue(init_ref)
        too_low_inputs = np.random.uniform(low=-1000, high=0, size=3)
        too_high_inputs = np.random.uniform(low=0.5, high=2000, size=3)
        for ref in [*too_low_inputs]:
            self.poisson.spinbox.setValue(ref)
            self.assertAlmostEqual(
                self.poisson.spinbox.value(), 0, msg="too low input succeeds")
            self.poisson.spinbox.setValue(init_ref)

        for ref in [*too_high_inputs]:
            self.poisson.spinbox.setValue(ref)
            self.assertAlmostEqual(
                self.poisson.spinbox.value(), 0.4999, msg="too large input succeeds")
            self.poisson.spinbox.setValue(init_ref)


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestYoungModulus,
        TestDensity,
        TestTesla,
        TestPoissonsRatio,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
