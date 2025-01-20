from random import randrange
import unittest
from src.units import YoungsModulus


class TestInitMethods(unittest.TestCase):

    def test_Pa(self):
        val = randrange(1000)
        uut = YoungsModulus.from_Pa(val)
        self.assertEqual(val, uut.Pa)

    def test_hPa(self):
        val = randrange(1000)
        uut = YoungsModulus.from_hPa(val)
        self.assertEqual(val, uut.hPa)

    def test_MPa(self):
        val = randrange(1000)
        uut = YoungsModulus.from_MPa(val)
        self.assertEqual(val, uut.MPa)

    def test_GPa(self):
        val = randrange(1000)
        uut = YoungsModulus.from_GPa(val)
        self.assertEqual(val, uut.GPa)


class TestSetMethods(unittest.TestCase):

    def test_Pa(self):
        val = randrange(1, 1000)
        uut = YoungsModulus(0)
        uut.Pa = val
        self.assertEqual(val, uut.Pa)

    def test_hPa(self):
        val = randrange(1, 1000)
        uut = YoungsModulus(0)
        uut.hPa = val
        self.assertEqual(val, uut.hPa)

    def test_MPa(self):
        val = randrange(1, 1000)
        uut = YoungsModulus(0)
        uut.MPa = val
        self.assertEqual(val, uut.MPa)

    def test_GPa(self):
        val = randrange(1, 1000)
        uut = YoungsModulus(0)
        uut.GPa = val
        self.assertEqual(val, uut.GPa)


class TestExceptionalBehavior(unittest.TestCase):

    def test_negative_init(self):
        val = randrange(-1000, -1)
        with self.assertRaises(ValueError):
            YoungsModulus(val)
        with self.assertRaises(ValueError):
            YoungsModulus.from_Pa(val)
        with self.assertRaises(ValueError):
            YoungsModulus.from_hPa(val)
        with self.assertRaises(ValueError):
            YoungsModulus.from_MPa(val)
        with self.assertRaises(ValueError):
            YoungsModulus.from_GPa(val)

    def test_negative_set(self):
        val = randrange(-1000, -1)
        uut = YoungsModulus(0)
        with self.assertRaises(ValueError):
            uut.Pa = val
        with self.assertRaises(ValueError):
            uut.hPa = val
        with self.assertRaises(ValueError):
            uut.MPa = val
        with self.assertRaises(ValueError):
            uut.GPa = val


class TestConversion(unittest.TestCase):

    def test_Pa_to_hPa(self):
        val = randrange(1000)
        uut = YoungsModulus.from_Pa(val)
        self.assertEqual(val / 100, uut.hPa)

    def test_Mpa_to_GPa(self):
        val = randrange(1000)
        uut = YoungsModulus.from_MPa(val)
        self.assertEqual(val / 1000, uut.GPa)


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestInitMethods,
        TestSetMethods,
        TestExceptionalBehavior,
        TestConversion
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
