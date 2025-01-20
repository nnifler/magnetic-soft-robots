from random import randrange
import unittest
from src.units import Tesla


class TestInitMethods(unittest.TestCase):

    def test_T(self):
        val = randrange(-1000, 1000)
        uut = Tesla.from_T(val)
        self.assertEqual(val, uut.T)


class TestSetMethods(unittest.TestCase):

    def test_T(self):
        val = randrange(-1000, 1000)
        uut = Tesla(-2025)
        uut.T = val
        self.assertEqual(val, uut.T)


def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestInitMethods,
        TestSetMethods,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
