from __future__ import annotations
from src.units.BaseUnit import BaseUnit
from enum import Enum


# TODO accept only positive values!!!
class Density(BaseUnit): # base: kgpm3
    
    class Unit(Enum):
        kgpm3 = 1
        gpcm3 = 1_000
        Mgpm3 = 1_000
        tpm3 = 1_000

    def __repr__(self) -> str:
        return f'{super().__repr__()} kg/m^3'

    @staticmethod
    def fromkgpm3(value: float) -> Density:
        return Density(value * Density.Unit.kgpm3.value)

    @property
    def kgpm3(self) -> float:
        return self._value / self.Unit.kgpm3.value
    
    @kgpm3.setter
    def kgpm3(self, value: int) -> None:
        self._value = value * self.Unit.kgpm3.value
    
    @staticmethod
    def fromgpcm3(value: float) -> Density:
        return Density(value * Density.Unit.gpcm3.value)

    @property
    def gpcm3(self) -> float:
        return self._value / self.Unit.gpcm3.value
    
    @gpcm3.setter
    def gpcm3(self, value: float) -> None:
        self._value = value * self.Unit.gpcm3.value

    tpm3 = Mgpm3 = gpcm3
    fromtpm3 = fromMgpm3 = fromgpcm3
