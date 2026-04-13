import calendar
from datetime import date
from typing import TYPE_CHECKING
from typing import Self

from tracker.domain.errors.base import ValidationError
from tracker.domain.values.base import Value
from tracker.domain.values.base import value

if TYPE_CHECKING:
    from collections.abc import Iterable

_MAX_SCHEDULE_SPAN_DAYS: int = 100 * 365 + 25
_MIN_RECURRING_OCCURRENCES: int = 2
_MONTHS_PER_YEAR: int = 12


@value
class PaymentSchedule(Value):
    dates: frozenset[date]

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.dates:
            raise ValidationError("Invalid schedule: dates must not be empty")
        if len(self.dates) > 1:
            span = (max(self.dates) - min(self.dates)).days
            if span > _MAX_SCHEDULE_SPAN_DAYS:
                raise ValidationError("Invalid schedule: schedule cannot span more than 100 years")

    @classmethod
    def create_one_time_payment(cls, *, on: date) -> Self:
        return cls(dates=frozenset({on}))

    @classmethod
    def create_monthly_payment(cls, *, on: date, months_number: int) -> Self:
        if months_number < _MIN_RECURRING_OCCURRENCES:
            raise ValidationError("months_number must be at least 2; use create_one_time_payment for a single payment")
        dates: list[date] = []
        year, month, day = on.year, on.month, on.day
        for _ in range(months_number):
            dates.append(cls._clamp_to_month(year, month, day))
            month += 1
            if month > _MONTHS_PER_YEAR:
                year, month = year + 1, 1
        return cls(dates=frozenset(dates))

    @classmethod
    def create_yearly_payment(cls, *, on: date, year_number: int) -> Self:
        if year_number < _MIN_RECURRING_OCCURRENCES:
            raise ValidationError("year_number must be at least 2; use create_one_time_payment for a single payment")
        dates = [cls._clamp_to_month(on.year + i, on.month, on.day) for i in range(year_number)]
        return cls(dates=frozenset(dates))

    @classmethod
    def create_specific_dates_payment(cls, *, on: Iterable[date]) -> Self:
        collected = frozenset(on)
        if len(collected) < _MIN_RECURRING_OCCURRENCES:
            raise ValidationError("on must contain at least 2 dates; use create_one_time_payment for a single payment")
        return cls(dates=collected)

    @staticmethod
    def _clamp_to_month(year: int, month: int, day: int) -> date:
        max_day = calendar.monthrange(year, month)[1]
        return date(year, month, min(day, max_day))
