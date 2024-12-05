import unittest
from src.units.YoungsModulus import YoungsModulus
from random import randrange

class TestInitMethods(unittest.TestCase):

    def testPa(self):
        val = randrange(1000)
        uut = YoungsModulus.fromPa(val)
        self.assertEqual(val, uut.Pa)

    def testhPa(self):
        val = randrange(1000)
        uut = YoungsModulus.fromhPa(val)
        self.assertEqual(val, uut.hPa)

    def testMPa(self):
        val = randrange(1000)
        uut = YoungsModulus.fromMPa(val)
        self.assertEqual(val, uut.MPa)

    def testGPa(self):
        val = randrange(1000)
        uut = YoungsModulus.fromGPa(val)
        self.assertEqual(val, uut.GPa)

class TestSetMethods(unittest.TestCase):

    def testPa(self):
        val = randrange(1, 1000)
        uut = YoungsModulus(0)
        uut.Pa = val
        self.assertEqual(val, uut.Pa)


    def testhPa(self):
        val = randrange(1, 1000)
        uut = YoungsModulus(0)
        uut.hPa = val
        self.assertEqual(val, uut.hPa)

    def testMPa(self):
        val = randrange(1, 1000)
        uut = YoungsModulus(0)
        uut.MPa = val
        self.assertEqual(val, uut.MPa)

    def testGPa(self):
        val = randrange(1, 1000)
        uut = YoungsModulus(0)
        uut.GPa = val
        self.assertEqual(val, uut.GPa)

class TestExceptionalBehavior(unittest.TestCase):
    
    def testNegativeInit(self):
        val = randrange(-1000,-1)
        with self.assertRaises(ValueError):
            YoungsModulus(val)
        with self.assertRaises(ValueError):
            YoungsModulus.fromPa(val)
        with self.assertRaises(ValueError):
            YoungsModulus.fromhPa(val)
        with self.assertRaises(ValueError):
            YoungsModulus.fromMPa(val)
        with self.assertRaises(ValueError):
            YoungsModulus.fromGPa(val)

    def testNegativeSet(self):
        val = randrange(-1000,-1)
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
    
    def testPa_hPa(self):
        val = randrange(1000)
        uut = YoungsModulus.fromPa(val)
        self.assertEqual(val / 100, uut.hPa)

    def testMpa_GPa(self):
        val = randrange(1000)
        uut = YoungsModulus.fromMPa(val)
        self.assertEqual(val / 1000, uut.GPa)
