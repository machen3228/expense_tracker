from typing import TYPE_CHECKING

from adaptix import Provider
from adaptix import ProviderNotFoundError
from adaptix.conversion import get_converter

from tracker.application.errors.base import DataMapperError

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterable


def get_mapper[SrcType, DstType](
    src: type[SrcType],
    dst: type[DstType],
    *,
    recipe: Iterable[Provider] = (),
) -> Callable[[SrcType], DstType]:
    try:
        return get_converter(src, dst, recipe=recipe)
    except ProviderNotFoundError as e:
        raise DataMapperError from e
