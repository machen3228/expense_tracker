from typing import TYPE_CHECKING
from typing import NewType
from uuid import UUID

from tracker.domain.entities.base import Entity
from tracker.domain.entities.base import entity

if TYPE_CHECKING:
    from datetime import datetime

    from tracker.domain.entities.person import PersonId
    from tracker.domain.values.dough import Dough

ExpenseId = NewType("ExpenseId", UUID)


@entity
class Expense(Entity[ExpenseId]):
    amount: Dough
    description: str
    paid_by: PersonId
    created_at: datetime
