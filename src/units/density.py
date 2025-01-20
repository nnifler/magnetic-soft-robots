"""This module contains the Density class which is the unit class for Density."""

from __future__ import annotations
from enum import Enum
from . import BaseUnit


class Density(BaseUnit):
    """Density unit class. Base unit is kg/m^3."""

    class Unit(Enum):
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
        return Density(value * Density.Unit.kgpm3.value)

    @property
    def kgpm3(self) -> float:
        """Gets the value of the Density Object in kg/m^3.

        Returns:
            float: The value of the Density Object in kg/m^3.
        """
        return self._value / self.Unit.kgpm3.value

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
        self._value = value * self.Unit.kgpm3.value

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
        return Density(value * Density.Unit.gpcm3.value)

    @property
    def gpcm3(self) -> float:
        """Gets the value of the Density Object in g/cm^3.

        Returns:
            float: _description_
        """
        return self._value / self.Unit.gpcm3.value

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
        self._value = value * self.Unit.gpcm3.value

    # Define getter and setter for t/m^3 and Mg/m^3
    tpm3 = Mgpm3 = gpcm3
    # Define create methods for t/m^3 and Mg/m^3
    from_tpm3 = from_Mgpm3 = from_gpcm3
