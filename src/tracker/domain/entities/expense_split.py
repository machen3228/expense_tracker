from decimal import Decimal
from typing import NewType
from uuid import UUID

from tracker.domain.entities.base import Entity
from tracker.domain.entities.base import entity
from tracker.domain.entities.expense import ExpenseId
from tracker.domain.entities.person import PersonId
from tracker.domain.errors import ValidationError
from tracker.domain.values.dough import Dough

ExpenseSplitId = NewType("ExpenseSplitId", UUID)


@entity
class ExpenseSplit(Entity[ExpenseSplitId]):
    expense_id: ExpenseId
    total_amount: Dough
    shares: dict[PersonId, Dough]

    def __post_init__(self) -> None:
        self.shares = dict(self.shares)
        self._validate()

    def _validate(self) -> None:
        if not self.shares:
            raise ValidationError("Invalid expense split: expenseSplit must have at least one share")

        for person_id, share in self.shares.items():
            if share.currency != self.total_amount.currency:
                raise ValidationError(
                    f"Invalid expense split: Share for {person_id} uses currency {share.currency!r} "
                    f"but expense uses {self.total_amount.currency!r}"
                )

        total: Decimal = sum(
            (share.amount for share in self.shares.values()),
            start=Decimal(0),
        )
        if total != self.total_amount.amount:
            raise ValidationError(
                f"Invalid expense split: Shares sum to {total} but expense total is {self.total_amount.amount}"
            )
