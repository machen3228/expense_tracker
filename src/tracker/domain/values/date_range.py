import calendar
from datetime import date
from typing import Self

from tracker.domain.errors import ValidationError
from tracker.domain.values.base import Value
from tracker.domain.values.base import value


@value
class DateRange(Value):
    start: date
    end: date

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.end < self.start:
            raise ValidationError("Invalid date range: end must not be before start")

    def contains(self, d: date) -> bool:
        return self.start <= d <= self.end

    @classmethod
    def for_month(cls, *, year: int, month: int) -> Self:
        last_day = calendar.monthrange(year, month)[1]
        return cls(start=date(year, month, 1), end=date(year, month, last_day))

    @classmethod
    def for_year(cls, *, year: int) -> Self:
        return cls(start=date(year, 1, 1), end=date(year, 12, 31))

    @classmethod
    def between(cls, *, start: date, end: date) -> Self:
        return cls(start=start, end=end)
