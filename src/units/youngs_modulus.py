"""This module contains the YoungsModulus class which is the unit class for YoungsModulus."""

from __future__ import annotations
from enum import Enum
from . import BaseUnit


class YoungsModulus(BaseUnit):
    """Unit class for YoungsModulus. The base unit is Pa."""
    class UnitFactor(Enum):
        """Enum class for YoungsModulus unit conversion factors."""
        Pa = 1
        hPa = 100
        MPa = 1_000_000
        GPa = 1_000_000_000

    def __repr__(self) -> str:
        """Returns the string representation of the YoungsModulus object.

        Returns:
            str: The string representation of the YoungsModulus object.
        """
        return f'{super().__repr__()} Pa'

    @staticmethod
    def from_Pa(value: int) -> YoungsModulus:
        """Creates a YoungsModulus Object from a value with Pa as its unit.

        Args:
            value (int): The value of the YoungsModulus Object in Pa.

        Raises:
            ValueError: If the value is negative.

        Returns:
            YoungsModulus: The YoungsModulus Object with the given value.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        return YoungsModulus(value * YoungsModulus.UnitFactor.Pa.value)

    @property
    def Pa(self) -> int:
        """Gets the value of the YoungsModulus Object in Pa.

        Returns:
            int: The value of the YoungsModulus Object in Pa.
        """
        return self._value // self.UnitFactor.Pa.value

    @Pa.setter
    def Pa(self, value: int) -> None:
        """Sets the value of the YoungsModulus Object with a value with Pa as its unit.

        Args:
            value (int): The value of the YoungsModulus Object in Pa.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        self._value = value * self.UnitFactor.Pa.value

    @staticmethod
    def from_hPa(value: float) -> YoungsModulus:
        """Creates a YoungsModulus Object from a value with hPa as its unit.

        Args:
            value (float): _description_

        Raises:
            ValueError: _description_

        Returns:
            YoungsModulus: _description_
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        return YoungsModulus(value * YoungsModulus.UnitFactor.hPa.value)

    @property
    def hPa(self) -> float:
        """Gets the value of the YoungsModulus Object in hPa.

        Returns:
            float: The value of the YoungsModulus Object in hPa.
        """
        return self._value / self.UnitFactor.hPa.value

    @hPa.setter
    def hPa(self, value: float) -> None:
        """Sets the value of the YoungsModulus Object with a value with hPa as its unit.

        Args:
            value (float): The value of the YoungsModulus Object in hPa.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        self._value = value * self.UnitFactor.hPa.value

    @staticmethod
    def from_MPa(value: float) -> YoungsModulus:
        """Creates a YoungsModulus Object from a value with MPa as its unit.

        Args:
            value (float): The value of the YoungsModulus Object in MPa.

        Raises:
            ValueError: If the value is negative.

        Returns:
            YoungsModulus: The YoungsModulus Object with the given value.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        return YoungsModulus(value * YoungsModulus.UnitFactor.MPa.value)

    @property
    def MPa(self) -> float:
        """Gets the value of the YoungsModulus Object in MPa.

        Returns:
            float: The value of the YoungsModulus Object in MPa.
        """
        return self._value / self.UnitFactor.MPa.value

    @MPa.setter
    def MPa(self, value: float) -> None:

        if value < 0:
            raise ValueError('Value cannot be negative!')
        self._value = value * self.UnitFactor.MPa.value

    @staticmethod
    def from_GPa(value: float) -> YoungsModulus:
        """Creates a YoungsModulus Object from a value with GPa as its unit.

        Args:
            value (float): The value of the YoungsModulus Object in GPa.

        Raises:
            ValueError: If the value is negative.

        Returns:
            YoungsModulus: The YoungsModulus Object with the given value.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        return YoungsModulus(value * YoungsModulus.UnitFactor.GPa.value)

    @property
    def GPa(self) -> float:
        """Gets the value of the YoungsModulus Object in GPa.

        Returns:
            float: The value of the YoungsModulus Object in GPa.
        """
        return self._value / self.UnitFactor.GPa.value

    @GPa.setter
    def GPa(self, value: float) -> None:
        """Sets the value of the YoungsModulus Object with a value with GPa as its unit.

        Args:
            value (float): The value of the YoungsModulus Object in GPa.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        self._value = value * self.UnitFactor.GPa.value
