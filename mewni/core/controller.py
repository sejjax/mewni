from typing import Callable
from mewni.utils.make_async import wrap_async
from abc import ABCMeta, abstractmethod
from types import CoroutineType
from typing import Type
from .mewni_object import MewniObject
from aiogram import Dispatcher


class Controller(MewniObject):
    __metaclass__ = ABCMeta
    handler: CoroutineType

    def __init__(self, handler: Callable | CoroutineType, *args, **kwargs):
        self.handler = wrap_async(handler)


def controller(class_: Type[Controller], require_parentheses: bool | None | Callable = None):
    def decorate(fn: Callable[[...], any]):
        is_parentheses_exist: bool

        def dec(*args, **kwargs):
            nonlocal is_parentheses_exist
            is_parentheses_exist = not (len(args) == 1 and callable(args[0]))

            def wrap(func_: Callable):
                controller_object = class_(func_, *args, **kwargs) if is_parentheses_exist else class_(func_, *(args[1:]))
                return controller_object

            if require_parentheses is None:
                if is_parentheses_exist:
                    return wrap
                return wrap(args[0])
            elif require_parentheses:
                if is_parentheses_exist:
                    return wrap
                raise RuntimeError('Parentheses are required, but they are not')
            elif not require_parentheses:
                if not is_parentheses_exist:
                    return wrap(args[0])
                raise RuntimeError('Parentheses are not required, but they are')

        return dec

    if callable(require_parentheses):
        # If decorator using without parentheses
        func = require_parentheses
        require_parentheses = None
        return decorate(func)
    return decorate
