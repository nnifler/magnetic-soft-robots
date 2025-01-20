import unittest
from src.units.Tesla import Tesla
from random import randrange

class TestInitMethods(unittest.TestCase):

    def testT(self):
        val = randrange(-1000, 1000)
        uut = Tesla.fromT(val)
        self.assertEqual(val, uut.T)

class TestSetMethods(unittest.TestCase):

    def testT(self):
        val = randrange(-1000, 1000)
        uut = Tesla(-2025)
        uut.T = val
        self.assertEqual(val, uut.T)


def suite() -> unittest.TestSuite: 
    suite = unittest.TestSuite()

    ## Insert new tests here
    tests = [
        TestInitMethods,
        TestSetMethods,
    ]

    ## Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    ## Add tests to test suite
    suite.addTests(loaded_tests)
    return suite
