from typing import TYPE_CHECKING
from typing import NewType
from uuid import UUID

from tracker.domain.entities.base import Entity
from tracker.domain.entities.base import entity

if TYPE_CHECKING:
    from datetime import date

    from tracker.domain.entities.income_category import IncomeCategoryId
    from tracker.domain.entities.person import PersonId
    from tracker.domain.enums.payment_type import PaymentType
    from tracker.domain.values.dough import Dough

DebitDebtId = NewType("DebitDebtId", UUID)


@entity
class DebitDebt(Entity[DebitDebtId]):
    category: IncomeCategoryId
    amount: Dough
    payment_type: PaymentType
    received_by: PersonId
    pay_at: date
    description: str
