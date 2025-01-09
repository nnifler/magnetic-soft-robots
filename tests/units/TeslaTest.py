import unittest
from src.units.Tesla import Tesla
from random import randrange

class TestInitMethods(unittest.TestCase):

    def testT(self):
        val = randrange(1000)
        uut = Tesla.fromT(val)
        self.assertEqual(val, uut.T)

class TestSetMethods(unittest.TestCase):

    def testkgpm3(self):
        val = randrange(1, 1000)
        uut = Tesla(0)
        uut.T = val
        self.assertEqual(val, uut.T)

class TestExceptionalBehavior(unittest.TestCase):
    
    def testNegativeInit(self):
        val = randrange(-1000,-1)
        with self.assertRaises(ValueError):
            Tesla(val)
        with self.assertRaises(ValueError):
            Tesla.fromT(val)

    def testNegativeSet(self):
        val = randrange(-1000,-1)
        uut = Tesla(0)
        with self.assertRaises(ValueError):
            uut.T = val

def suite() -> unittest.TestSuite: 
    suite = unittest.TestSuite()

    ## Insert new tests here
    tests = [
        TestInitMethods,
        TestSetMethods,
        TestExceptionalBehavior,
    ]

    ## Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    ## Add tests to test suite
    suite.addTests(loaded_tests)
    return suite
    