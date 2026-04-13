from typing import TYPE_CHECKING
from typing import NewType
from uuid import UUID

from tracker.domain.entities.base import Entity
from tracker.domain.entities.base import entity

if TYPE_CHECKING:
    from tracker.domain.entities.expense_category import ExpenseCategoryId
    from tracker.domain.entities.person import PersonId
    from tracker.domain.values.dough import Dough
    from tracker.domain.values.payment_schedule import PaymentSchedule

CreditDebtId = NewType("CreditDebtId", UUID)


@entity
class CreditDebt(Entity[CreditDebtId]):
    category: ExpenseCategoryId
    amount: Dough
    paid_by: PersonId
    schedule: PaymentSchedule
    description: str
