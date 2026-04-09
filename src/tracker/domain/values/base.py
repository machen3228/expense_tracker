from dataclasses import dataclass
from typing import Any
from typing import Self
from typing import dataclass_transform


@dataclass_transform(kw_only_default=True, frozen_default=True)
def value[ClsType](cls: type[ClsType]) -> type[ClsType]:
    return dataclass(cls, frozen=True, kw_only=True)


@value
class Value:
    def __new__(cls, *_args: Any, **_kwargs: Any) -> Self:
        if cls is Value:
            raise TypeError("Base Value cannot be instantiated directly")
        if not getattr(cls, "__dataclass_fields__", None):
            raise TypeError(f"{cls.__name__} must have at least one field")
        return object.__new__(cls)
