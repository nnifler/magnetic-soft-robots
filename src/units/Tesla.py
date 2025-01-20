from __future__ import annotations
from src.units.BaseUnit import BaseUnit
from enum import Enum

class Tesla(BaseUnit): # base: T

    def __init__(self, value):
        self._value = value

    ## Define conversion factors
    class Unit(Enum):
        T = 1

    ## String representation
    def __repr__(self) -> str:
        return f'{super().__repr__()} T'
    
    ## Create a Tesla Object from a value with T as its unit
    @staticmethod
    def fromT(value: float) -> Tesla:
        return Tesla(value * Tesla.Unit.T.value)

    ## Get the value of the Tesla Object in T
    @property
    def T(self) -> float:
        return self._value / self.Unit.T.value
    
    ## Set the value of the Tesla Object with a value with T as its unit
    @T.setter
    def T(self, value: int) -> None:
        self._value = value * self.Unit.T.value
