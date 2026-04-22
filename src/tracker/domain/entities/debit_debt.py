from typing import NewType
from uuid import UUID

from tracker.domain.entities.base import Entity
from tracker.domain.entities.base import entity
from tracker.domain.entities.income_category import IncomeCategoryId
from tracker.domain.entities.person import PersonId
from tracker.domain.values.dough import Dough
from tracker.domain.values.payment_schedule import PaymentSchedule

DebitDebtId = NewType("DebitDebtId", UUID)


@entity
class DebitDebt(Entity[DebitDebtId]):
    category: IncomeCategoryId
    amount: Dough
    received_by: PersonId
    schedule: PaymentSchedule
    description: str
