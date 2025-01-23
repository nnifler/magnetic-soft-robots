"""This module contains the BaseUnit class which is the base class for all units."""

from numbers import Number


class BaseUnit:
    """Base class for all units."""
    _value = 0

    def __init__(self, value: Number) -> None:
        """Initializes the Unit object with the given value.
        Args:
            value (Number): The init base value of the unit.

        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError('Value cannot be negative!')
        self._value = value

    def __repr__(self) -> str:
        """Returns the string representation of the Unit object.

        Returns:
            str: The string representation of the Unit object.
        """
        return f'{self._value}'
