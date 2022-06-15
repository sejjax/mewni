from typing import Callable
from types import CoroutineType
from asyncio import iscoroutinefunction


def is_async(func: Callable | CoroutineType) -> bool:
    return iscoroutinefunction(func)
