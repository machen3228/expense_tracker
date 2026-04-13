from typing import TYPE_CHECKING
from typing import NewType
from uuid import UUID

from tracker.domain.entities.base import Entity
from tracker.domain.entities.base import entity

if TYPE_CHECKING:
    from datetime import date

    from tracker.domain.entities.expense_category import ExpenseCategoryId
    from tracker.domain.entities.person import PersonId
    from tracker.domain.enums.payment_type import PaymentType
    from tracker.domain.values.dough import Dough

CreditDebtId = NewType("CreditDebtId", UUID)


@entity
class CreditDebt(Entity[CreditDebtId]):
    category: ExpenseCategoryId
    amount: Dough
    payment_type: PaymentType
    paid_by: PersonId
    pay_at: date
    description: str
