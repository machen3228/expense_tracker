from typing import TYPE_CHECKING

from tracker.domain.values.base import Value
from tracker.domain.values.base import value

if TYPE_CHECKING:
    from datetime import date

    from tracker.domain.enums import BudgetSource
    from tracker.domain.enums import FlowType
    from tracker.domain.values.dough import Dough


@value
class BudgetLine(Value):
    date: date
    amount: Dough
    flow: FlowType
    source: BudgetSource
    description: str
