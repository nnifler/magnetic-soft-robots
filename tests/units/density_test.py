# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ #
#                        MSR, Magnetic Soft Robotics Simulation                        #
#   Copyright (C) 2025 Julius Hahnewald, Heiko Hellkamp, Finn Schubert, Carla Wehner   #
#                                                                                      #
# This program is free software; you can redistribute it and/or                        #
# modify it under the terms of the GNU Lesser General Public                           #
# License as published by the Free Software Foundation; either                         #
# version 2.1 of the License, or (at your option) any later version.                   #
#                                                                                      #
# This program is distributed in the hope that it will be useful,                      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU                    #
# Lesser General Public License for more details.                                      #
#                                                                                      #
# You should have received a copy of the GNU Lesser General Public                     #
# License along with this program; if not, write to the Free Software                  #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301            #
# USA                                                                                  #
# ------------------------------------------------------------------------------------ #
# Contact information: finn.s.schubert@gmail.com                                       #
# ____________________________________________________________________________________ #

from random import randrange
import unittest
from src.units import Density


class TestInitMethods(unittest.TestCase):

    def test_kgpm3(self) -> None:
        val = randrange(1000)
        uut = Density.from_kgpm3(val)
        self.assertEqual(val, uut.kgpm3)

    def test_gpcm3(self) -> None:
        val = randrange(1000)
        uut = Density.from_gpcm3(val)
        self.assertEqual(val, uut.gpcm3)

    def test_Mgpm3(self) -> None:
        val = randrange(1000)
        uut = Density.from_Mgpm3(val)
        self.assertEqual(val, uut.Mgpm3)

    def test_tpm3(self) -> None:
        val = randrange(1000)
        uut = Density.from_tpm3(val)
        self.assertEqual(val, uut.tpm3)


class TestSetMethods(unittest.TestCase):

    def test_kgpm3(self):
        val = randrange(1, 1000)
        uut = Density(0)
        uut.kgpm3 = val
        self.assertEqual(val, uut.kgpm3)

    def test_gpcm3(self):
        val = randrange(1, 1000)
        uut = Density(0)
        uut.gpcm3 = val
        self.assertEqual(val, uut.gpcm3)

    def test_Mgpm3(self):
        val = randrange(1, 1000)
        uut = Density(0)
        uut.Mgpm3 = val
        self.assertEqual(val, uut.Mgpm3)

    def test_tpm3(self):
        val = randrange(1, 1000)
        uut = Density(0)
        uut.tpm3 = val
        self.assertEqual(val, uut.tpm3)


class TestExceptionalBehavior(unittest.TestCase):

    def test_negative_init(self):
        val = randrange(-1000, -1)
        with self.assertRaises(ValueError):
            Density(val)
        with self.assertRaises(ValueError):
            Density.from_kgpm3(val)
        with self.assertRaises(ValueError):
            Density.from_gpcm3(val)
        with self.assertRaises(ValueError):
            Density.from_Mgpm3(val)
        with self.assertRaises(ValueError):
            Density.from_tpm3(val)

    def test_negative_set(self):
        val = randrange(-1000, -1)
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

    def test_kgpm3_to_gpcm3(self):
        val = randrange(1000)
        uut = Density.from_kgpm3(val)
        self.assertEqual(val / 1000, uut.gpcm3)

    def test_Mgpm3_to_tpm3(self):
        val = randrange(1000)
        uut = Density.from_Mgpm3(val)
        self.assertEqual(val, uut.tpm3)


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
