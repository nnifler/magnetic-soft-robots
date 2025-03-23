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

"""This module contains the Density class which is the unit class for Density."""

from __future__ import annotations
from enum import Enum
from . import BaseUnit


class Density(BaseUnit):
    """Density unit class. Base unit is kg/m^3."""

    class UnitFactor(Enum):
        """Enum class for Density unit conversion factors."""
        kgpm3 = 1
        gpcm3 = 1_000
        Mgpm3 = 1_000
        tpm3 = 1_000

    def __repr__(self) -> str:
        """Returns the string representation of the Density object.

        Returns:
            str: The string representation of the Density object.
        """
        return f'{super().__repr__()} kg/m\u00b3'

    @staticmethod
    def from_kgpm3(value: float) -> Density:
        """Creates a Density Object from a value with kg/m^3 as its unit.

        Args:
            value (float): The value of the Density Object in kg/m^3.

        Raises:
            ValueError: If the value is negative.

        Returns:
            Density: The Density Object with the given value.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        return Density(value * Density.UnitFactor.kgpm3.value)

    @property
    def kgpm3(self) -> float:
        """Gets the value of the Density Object in kg/m^3.

        Returns:
            float: The value of the Density Object in kg/m^3.
        """
        return self._value / self.UnitFactor.kgpm3.value

    @kgpm3.setter
    def kgpm3(self, value: int) -> None:
        """Sets the value of the Density Object with a value with kg/m^3 as its unit.

        Args:
            value (int): The value of the Density Object in kg/m^3.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        self._value = value * self.UnitFactor.kgpm3.value

    @staticmethod
    def from_gpcm3(value: float) -> Density:
        """Creates a Density Object from a value with g/cm^3 as its unit.

        Args:
            value (float): The value of the Density Object in g/cm^3.

        Raises:
            ValueError: If the value is negative.

        Returns:
            Density: The Density Object with the given value.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        return Density(value * Density.UnitFactor.gpcm3.value)

    @property
    def gpcm3(self) -> float:
        """Gets the value of the Density Object in g/cm^3.

        Returns:
            float: The value of the Density Object in g/cm^3.
        """
        return self._value / self.UnitFactor.gpcm3.value

    @gpcm3.setter
    def gpcm3(self, value: float) -> None:
        """Sets the value of the Density Object with a value with g/cm^3 as its unit.

        Args:
            value (float): The value of the Density Object in g/cm^3.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        self._value = value * self.UnitFactor.gpcm3.value

    @staticmethod
    def from_Mgpm3(value: float) -> Density:
        """Creates a Density Object from a value with Mg/m^3 as its unit.

        Args:
            value (float): The value of the Density Object in Mg/m^3.

        Raises:
            ValueError: If the value is negative.

        Returns:
            Density: The Density Object with the given value.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        return Density(value * Density.UnitFactor.Mgpm3.value)

    @property
    def Mgpm3(self) -> float:
        """Gets the value of the Density Object in Mg/m^3.

        Returns:
            float: The value of the Density Object in Mg/m^3.
        """
        return self._value / self.UnitFactor.Mgpm3.value

    @Mgpm3.setter
    def Mgpm3(self, value: float) -> None:
        """Sets the value of the Density Object with a value with Mg/m^3 as its unit.

        Args:
            value (float): The value of the Density Object in Mg/m^3.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        self._value = value * self.UnitFactor.Mgpm3.value

    @staticmethod
    def from_tpm3(value: float) -> Density:
        """Creates a Density Object from a value with t/m^3 as its unit.

        Args:
            value (float): The value of the Density Object in t/m^3.

        Raises:
            ValueError: If the value is negative.

        Returns:
            Density: The Density Object with the given value.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        return Density(value * Density.UnitFactor.tpm3.value)

    @property
    def tpm3(self) -> float:
        """Gets the value of the Density Object in t/m^3.

        Returns:
            float: The value of the Density Object in t/m^3.
        """
        return self._value / self.UnitFactor.tpm3.value

    @tpm3.setter
    def tpm3(self, value: float) -> None:
        """Sets the value of the Density Object with a value with t/m^3 as its unit.

        Args:
            value (float): The value of the Density Object in t/m^3.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        self._value = value * self.UnitFactor.tpm3.value
