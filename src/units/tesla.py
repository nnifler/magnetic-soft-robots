"""This module contains the Tesla class which is the unit class for Tesla."""

from __future__ import annotations
from enum import Enum
from . import BaseUnit


class Tesla(BaseUnit):
    """Unit class for Tesla. The base unit is T."""

    def __init__(self, value: float) -> None:
        """Initializes the Tesla object with the given value.

        Args:
            value (float): The init base value of the unit.
        """
        super().__init__(0)  # Initialize super object with non-negative value
        self._value = value

    class UnitFactor(Enum):
        """Enum class for Tesla unit conversion factors."""
        T = 1

    def __repr__(self) -> str:
        """Returns the string representation of the Tesla object.

        Returns:
            str: The string representation of the Tesla object.
        """
        return f'{super().__repr__()} T'

    @staticmethod
    def from_T(value: float) -> Tesla:
        """Creates a Tesla Object from a value with T as its unit.

        Args:
            value (float): The value of the Tesla Object in T.

        Returns:
            Tesla: The Tesla Object with the given value.
        """
        return Tesla(value * Tesla.UnitFactor.T.value)

    @property
    def T(self) -> float:
        """Gets the value of the Tesla Object in T.

        Returns:
            float: The value of the Tesla Object in T.
        """
        return self._value / self.UnitFactor.T.value

    @T.setter
    def T(self, value: int) -> None:
        """Sets the value of the Tesla Object with a value with T as its unit.

        Args:
            value (int): The value of the Tesla Object in T.
        """
        self._value = value * self.UnitFactor.T.value
