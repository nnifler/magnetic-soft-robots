class BaseUnit:
    _value = 0

    ## Basic init method to create a BaseUnit Object with the given value
    def __init__(self, value):
        self._value = value

    ## String representation
    def __repr__(self) -> str:
        return f'{self._value}'
