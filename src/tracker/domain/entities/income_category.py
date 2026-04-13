from typing import TYPE_CHECKING
from typing import NewType
from uuid import UUID

from tracker.domain.entities.base import Entity
from tracker.domain.entities.base import entity
from tracker.domain.errors import ValidationError

if TYPE_CHECKING:
    from tracker.domain.entities.person import PersonId
    from tracker.domain.values.category_name import CategoryName

IncomeCategoryId = NewType("IncomeCategoryId", UUID)


@entity
class IncomeCategory(Entity[IncomeCategoryId]):
    name: CategoryName
    is_default: bool
    owner: PersonId | None

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.is_default and self.owner is not None:
            raise ValidationError("Default category must not have an owner")
        if not self.is_default and self.owner is None:
            raise ValidationError("Non-default category must have an owner")
