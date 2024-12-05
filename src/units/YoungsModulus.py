from src.units.BaseUnit import BaseUnit
from enum import Enum

class YoungsModulus(BaseUnit):
    class Unit(Enum):
        Pa = 1
        hPa = 100
        MPa = 1000000
        GPa = 1000000000


    @staticmethod
    def Pa(value):
        return YoungsModulus(value * YoungsModulus.Unit.Pa.value)

    @property
    def Pa(self):
        return self._value * self.Unit.Pa.value
    
    @Pa.setter
    def Pa(self, value):
        self._value = value * self.Unit.Pa.value
    
    @staticmethod
    def hPa(value):
        return YoungsModulus(value * YoungsModulus.Unit.hPa.value)

    @property
    def hPa(self):
        return self._value * self.Unit.hPa.value
    
    @hPa.setter
    def hPa(self, value):
        self._value = value * self.Unit.hPa.value

    @staticmethod
    def MPa(value):
        return YoungsModulus(value * YoungsModulus.Unit.MPa.value)

    @property
    def MPa(self):
        return self._value * self.Unit.MPa.value
    
    @MPa.setter
    def MPa(self, value):
        self._value = value * self.Unit.MPa.value

    @staticmethod
    def GPa(value):
        return YoungsModulus(value * YoungsModulus.Unit.GPa.value)

    @property
    def GPa(self):
        return self._value * self.Unit.GPa.value
    
    @GPa.setter
    def GPa(self, value):
        self._value = value * self.Unit.GPa.value
