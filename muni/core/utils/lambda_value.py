from types import FunctionType


def lambda_value(value):
    if type(value) == FunctionType:
        return value()
    return value
