from decimal import Decimal
from typing import TYPE_CHECKING

from tracker.domain.enums import FlowType
from tracker.domain.values.base import Value
from tracker.domain.values.base import value

if TYPE_CHECKING:
    from tracker.domain.values.budget_line import BudgetLine
    from tracker.domain.values.date_range import DateRange


@value
class BudgetReport(Value):
    period: DateRange
    lines: tuple[BudgetLine, ...]

    @property
    def total_income(self) -> Decimal:
        return sum(
            (line.amount.amount for line in self.lines if line.flow == FlowType.INCOME),
            start=Decimal(0),
        )

    @property
    def total_expenses(self) -> Decimal:
        return sum(
            (line.amount.amount for line in self.lines if line.flow == FlowType.EXPENSE),
            start=Decimal(0),
        )

    @property
    def net_balance(self) -> Decimal:
        return self.total_income - self.total_expenses
