from typing import NewType
from uuid import UUID

from tracker.domain.entities.base import Entity
from tracker.domain.entities.base import entity
from tracker.domain.entities.person import PersonId
from tracker.domain.errors import ValidationError
from tracker.domain.values.category_name import CategoryName

ExpenseCategoryId = NewType("ExpenseCategoryId", UUID)


@entity
class ExpenseCategory(Entity[ExpenseCategoryId]):
    name: CategoryName
    is_default: bool
    owner: PersonId | None

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.is_default and self.owner is not None:
            raise ValidationError("Invalid expense category: default category must not have an owner")
        if not self.is_default and self.owner is None:
            raise ValidationError("Invalid expense category: non-default category must have an owner")
