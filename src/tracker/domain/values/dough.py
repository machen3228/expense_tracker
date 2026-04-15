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

    def __add__(self, other: Dough) -> Dough:
        if self.currency != other.currency:
            raise ValidationError(f"Cannot add Dough: currency mismatch {self.currency!r} vs {other.currency!r}")
        return Dough(amount=self.amount + other.amount, currency=self.currency)

    def __sub__(self, other: Dough) -> Dough:
        if self.currency != other.currency:
            raise ValidationError(f"Cannot subtract Dough: currency mismatch {self.currency!r} vs {other.currency!r}")
        result = self.amount - other.amount
        if result <= 0:
            raise ValidationError("Cannot subtract Dough: result must be positive")
        return Dough(amount=result, currency=self.currency)
