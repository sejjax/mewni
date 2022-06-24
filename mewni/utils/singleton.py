from typing import TypeVar

T = TypeVar('T')


def singleton(class_: T) -> T:
    INSTANCE_ATTRIBUTE_NAME = '__instance__'

    def getinstance(*args, **kwargs):
        if not hasattr(class_, INSTANCE_ATTRIBUTE_NAME) or type(getattr(class_, INSTANCE_ATTRIBUTE_NAME)) != class_:
            setattr(class_, INSTANCE_ATTRIBUTE_NAME, class_(*args, **kwargs))
        return getattr(class_, INSTANCE_ATTRIBUTE_NAME)
    return getinstance
