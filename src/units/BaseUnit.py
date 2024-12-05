class BaseUnit:
    _value = 0
    def __init__(self, value):
        self._value = value

    def __repr__(self) -> str:
        return f'{self._value}'
