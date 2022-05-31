from typing import Optional, Union
from dataclasses import dataclass


@dataclass
class MuniScheduler:
    pass


@dataclass
class MuniCommand:
    command: str
    value: Optional[str]


MuniCallbackMetaTypes = Union[MuniCommand, MuniScheduler]


@dataclass
class MuniCallbackMeta:
    value: MuniCallbackMetaTypes
