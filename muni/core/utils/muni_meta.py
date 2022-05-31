from muni.core.constants import MUNI_META
from muni.core.types import MuniCallbackMeta, MuniCallbackMetaTypes


def set_muni_meta(obj, meta: MuniCallbackMetaTypes):
    setattr(obj, MUNI_META, MuniCallbackMeta(meta))


def get_muni_meta(obj) -> MuniCallbackMeta:
    return getattr(obj, MUNI_META)

def has_muni_meta(obj) -> bool:
    return hasattr(obj, MUNI_META)
