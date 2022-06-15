from muni.core.constants import MUNI_META
from muni.core.types import MuniCallbackMeta, MuniCallbackMetaTypes
from typing import TypeVar

T = TypeVar('T')


def set_muni_meta(obj: T, meta: MuniCallbackMetaTypes) -> T:
    setattr(obj, MUNI_META, MuniCallbackMeta(meta))
    return obj


def get_muni_meta(obj) -> MuniCallbackMeta:
    return getattr(obj, MUNI_META)


def has_muni_meta(obj) -> bool:
    return hasattr(obj, MUNI_META)
