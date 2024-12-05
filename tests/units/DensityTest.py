import unittest
from src.units.Density import Density
from random import randrange

class TestInitMethods(unittest.TestCase):

    def testkgpm3(self):
        val = randrange(1000)
        uut = Density.fromkgpm3(val)
        self.assertEqual(val, uut.kgpm3)

    def testgpcm3(self):
        val = randrange(1000)
        uut = Density.fromgpcm3(val)
        self.assertEqual(val, uut.gpcm3)

    def testMgpm3(self):
        val = randrange(1000)
        uut = Density.fromMgpm3(val)
        self.assertEqual(val, uut.Mgpm3)

    def testtpm3(self):
        val = randrange(1000)
        uut = Density.fromtpm3(val)
        self.assertEqual(val, uut.tpm3)

class TestSetMethods(unittest.TestCase):

    def testkgpm3(self):
        val = randrange(1, 1000)
        uut = Density(0)
        uut.kgpm3 = val
        self.assertEqual(val, uut.kgpm3)


    def testgpcm3(self):
        val = randrange(1, 1000)
        uut = Density(0)
        uut.gpcm3 = val
        self.assertEqual(val, uut.gpcm3)

    def testMgpm3(self):
        val = randrange(1, 1000)
        uut = Density(0)
        uut.Mgpm3 = val
        self.assertEqual(val, uut.Mgpm3)

    def testtpm3(self):
        val = randrange(1, 1000)
        uut = Density(0)
        uut.tpm3 = val
        self.assertEqual(val, uut.tpm3)

class TestExceptionalBehavior(unittest.TestCase):
    
    def testNegativeInit(self):
        val = randrange(-1000,-1)
        with self.assertRaises(ValueError):
            Density(val)
        with self.assertRaises(ValueError):
            Density.fromkgpm3(val)
        with self.assertRaises(ValueError):
            Density.fromgpcm3(val)
        with self.assertRaises(ValueError):
            Density.fromMgpm3(val)
        with self.assertRaises(ValueError):
            Density.fromtpm3(val)

    def testNegativeSet(self):
        val = randrange(-1000,-1)
        uut = Density(0)
        with self.assertRaises(ValueError):
            uut.kgpm3 = val
        with self.assertRaises(ValueError):
            uut.gpcm3 = val
        with self.assertRaises(ValueError):
            uut.Mgpm3 = val
        with self.assertRaises(ValueError):
            uut.tpm3 = val

class TestConversion(unittest.TestCase):
    
    def testkgpm3_gpcm3(self):
        val = randrange(1000)
        uut = Density.fromkgpm3(val)
        self.assertEqual(val / 1000, uut.gpcm3)

    def testMgpm3_tpm3(self):
        val = randrange(1000)
        uut = Density.fromMgpm3(val)
        self.assertEqual(val, uut.tpm3)


def suite() -> unittest.TestSuite: 
    suite = unittest.TestSuite()

    ## Insert new tests here
    tests = [
        TestInitMethods,
        TestSetMethods,
        TestExceptionalBehavior,
        TestConversion
    ]

    ## Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    ## Add tests to test suite
    suite.addTests(loaded_tests)
    return suite
