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
