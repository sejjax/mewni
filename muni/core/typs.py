from typing import Optional, Union
from dataclasses import dataclass


class MuniScheduler:
    pass


class MuniOnStartup:
    pass


class MuniOnStop:
    pass


@dataclass
class MuniCommand:
    command: str
    value: Optional[str]


MuniCallbackMetaTypes = Union[MuniCommand, MuniScheduler, MuniOnStartup, MuniOnStop]


@dataclass
class MuniCallbackMeta:
    value: MuniCallbackMetaTypes
