from typing import TYPE_CHECKING
from typing import NewType
from uuid import UUID

from tracker.domain.entities.base import Entity
from tracker.domain.entities.base import entity

if TYPE_CHECKING:
    from tracker.domain.values.category_name import CategoryName

CategoryId = NewType("CategoryId", UUID)


@entity
class Category(Entity[CategoryId]):
    name: CategoryName
    is_default: bool
