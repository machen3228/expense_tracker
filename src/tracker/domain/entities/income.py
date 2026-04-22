from datetime import datetime
from typing import NewType
from uuid import UUID

from tracker.domain.entities.base import Entity
from tracker.domain.entities.base import entity
from tracker.domain.entities.income_category import IncomeCategoryId
from tracker.domain.entities.person import PersonId
from tracker.domain.values.dough import Dough

IncomeId = NewType("IncomeId", UUID)


@entity
class Income(Entity[IncomeId]):
    amount: Dough
    category: IncomeCategoryId
    description: str
    received_by: PersonId
    created_at: datetime
