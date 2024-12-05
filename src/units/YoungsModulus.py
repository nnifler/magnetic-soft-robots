from __future__ import annotations
from src.units.BaseUnit import BaseUnit
from enum import Enum


# TODO accept only positive values!!!
class YoungsModulus(BaseUnit):

    ## Define conversion factors
    class Unit(Enum):
        Pa = 1
        hPa = 100
        MPa = 1_000_000
        GPa = 1_000_000_000

    ## String representation
    def __repr__(self) -> str:
        return f'{super().__repr__()} Pa'

    ## Create a YoungsModulus Object from a value with Pa as its unit
    @staticmethod
    def fromPa(value: int) -> YoungsModulus:
        return YoungsModulus(value * YoungsModulus.Unit.Pa.value)

    ## Get the value of the YoungsModulus Object in Pa
    @property
    def Pa(self) -> int:
        return self._value // self.Unit.Pa.value
    
    ## Set the value of the YoungsModulus Object with a value with Pa as its unit
    @Pa.setter
    def Pa(self, value: int) -> None:
        self._value = value * self.Unit.Pa.value
    
    ## Create a YoungsModulus Object from a value with hPa as its unit
    @staticmethod
    def fromhPa(value: float) -> YoungsModulus:
        return YoungsModulus(value * YoungsModulus.Unit.hPa.value)

    ## Get the value of the YoungsModulus Object in hPa
    @property
    def hPa(self) -> float:
        return self._value / self.Unit.hPa.value
    
    ## Set the value of the YoungsModulus Object with a value with hPa as its unit
    @hPa.setter
    def hPa(self, value: float) -> None:
        self._value = value * self.Unit.hPa.value

    ## Create a YoungsModulus Object from a value with MPa as its unit
    @staticmethod
    def fromMPa(value: float) -> YoungsModulus:
        return YoungsModulus(value * YoungsModulus.Unit.MPa.value)

    ## Get the value of the YoungsModulus Object in MPa
    @property
    def MPa(self) -> float:
        return self._value / self.Unit.MPa.value
    
    ## Set the value of the YoungsModulus Object with a value with MPa as its unit
    @MPa.setter
    def MPa(self, value: float) -> None:
        self._value = value * self.Unit.MPa.value

    ## Create a YoungsModulus Object from a value with GPa as its unit
    @staticmethod
    def fromGPa(value: float) -> YoungsModulus:
        return YoungsModulus(value * YoungsModulus.Unit.GPa.value)

    ## Get the value of the YoungsModulus Object in GPa
    @property
    def GPa(self) -> float:
        return self._value / self.Unit.GPa.value
    
    ## Set the value of the YoungsModulus Object with a value with GPa as its unit
    @GPa.setter
    def GPa(self, value: float) -> None:
        self._value = value * self.Unit.GPa.value
