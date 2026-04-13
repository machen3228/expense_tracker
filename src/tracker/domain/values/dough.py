import re
from typing import TYPE_CHECKING
from typing import ClassVar

from tracker.domain.errors import ValidationError
from tracker.domain.values.base import Value
from tracker.domain.values.base import value

if TYPE_CHECKING:
    from decimal import Decimal


@value
class Dough(Value):
    _CURRENCY_FMT: ClassVar[re.Pattern[str]] = re.compile(r"^[A-Z]{3}$")

    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.amount <= 0:
            raise ValidationError("Invalid dough: amount must be positive")

        if not self._CURRENCY_FMT.match(self.currency):
            raise ValidationError("Invalid dough: currency must be a valid ISO 4217 code (e.g. USD, EUR)")
