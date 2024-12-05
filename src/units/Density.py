from __future__ import annotations
from src.units.BaseUnit import BaseUnit
from enum import Enum


# TODO accept only positive values!!!
class Density(BaseUnit): # base: kgpm3
    
    ## Define conversion factors
    class Unit(Enum):
        kgpm3 = 1
        gpcm3 = 1_000
        Mgpm3 = 1_000
        tpm3 = 1_000

    ## String representation
    def __repr__(self) -> str:
        return f'{super().__repr__()} kg/m^3'

    ## Create a Density Object from a value with kg/m^3 as its unit
    @staticmethod
    def fromkgpm3(value: float) -> Density:
        return Density(value * Density.Unit.kgpm3.value)

    ## Get the value of the Density Object in kg/m^3
    @property
    def kgpm3(self) -> float:
        return self._value / self.Unit.kgpm3.value
    
    ## Set the value of the Density Object with a value with kg/m^3 as its unit
    @kgpm3.setter
    def kgpm3(self, value: int) -> None:
        self._value = value * self.Unit.kgpm3.value
    
    ## Create a Density Object from a value with g/cm^3 as its unit
    @staticmethod
    def fromgpcm3(value: float) -> Density:
        return Density(value * Density.Unit.gpcm3.value)

    ## Get the value of the Density Object in g/cm^3
    @property
    def gpcm3(self) -> float:
        return self._value / self.Unit.gpcm3.value
    
    ## Set the value of the Density Object with a value with g/cm^3 as its unit
    @gpcm3.setter
    def gpcm3(self, value: float) -> None:
        self._value = value * self.Unit.gpcm3.value

    ## Define getter and setter for t/m^3 and Mg/m^3
    tpm3 = Mgpm3 = gpcm3
    ## Define create methods for t/m^3 and Mg/m^3
    fromtpm3 = fromMgpm3 = fromgpcm3
