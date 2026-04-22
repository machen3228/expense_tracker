from datetime import datetime
from typing import NewType
from uuid import UUID

from tracker.domain.entities.base import Entity
from tracker.domain.entities.base import entity
from tracker.domain.entities.expense_category import ExpenseCategoryId
from tracker.domain.entities.person import PersonId
from tracker.domain.values.dough import Dough

ExpenseId = NewType("ExpenseId", UUID)


@entity
class Expense(Entity[ExpenseId]):
    amount: Dough
    category: ExpenseCategoryId
    description: str
    paid_by: PersonId
    created_at: datetime
