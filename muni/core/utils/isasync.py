from typing import Callable, Union
from types import CoroutineType
from asyncio import iscoroutinefunction


def is_async(func: Union[Callable, CoroutineType]):
    return iscoroutinefunction(func)
