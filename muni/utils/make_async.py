from typing import Callable
from .is_async import is_async
from types import CoroutineType


def wrap_async(func: Callable | CoroutineType):
    async def wrapper(*args, **kwargs):
        if is_async(func):
            await func()
        else:
            func()
    return wrapper
