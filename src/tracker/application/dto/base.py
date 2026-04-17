from typing import dataclass_transform

from pydantic import ConfigDict
from pydantic.dataclasses import dataclass


@dataclass_transform(kw_only_default=True, frozen_default=True)
def dto[ClsType](cls: type[ClsType]) -> type:
    return dataclass(
        cls,
        frozen=True,
        kw_only=True,
        config=ConfigDict(arbitrary_types_allowed=True),
    )
