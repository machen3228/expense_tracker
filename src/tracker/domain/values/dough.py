from typing import TYPE_CHECKING

from tracker.domain.errors import ValidationError
from tracker.domain.values.base import Value
from tracker.domain.values.base import value

if TYPE_CHECKING:
    from decimal import Decimal

    from tracker.domain.enums import Currency


@value
class Dough(Value):
    amount: Decimal
    currency: Currency

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.amount <= 0:
            raise ValidationError("Invalid dough: amount must be positive")
