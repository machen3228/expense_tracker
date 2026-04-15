from typing import TYPE_CHECKING

from tracker.domain.values.base import Value
from tracker.domain.values.base import value

if TYPE_CHECKING:
    from tracker.domain.entities.credit_debt import CreditDebt
    from tracker.domain.entities.debit_debt import DebitDebt
    from tracker.domain.entities.expense import Expense
    from tracker.domain.entities.expense_split import ExpenseSplit
    from tracker.domain.entities.income import Income
    from tracker.domain.entities.person import PersonId


@value
class PersonLedger(Value):
    person_id: PersonId
    expenses: tuple[Expense, ...]
    incomes: tuple[Income, ...]
    credit_debts: tuple[CreditDebt, ...]
    debit_debts: tuple[DebitDebt, ...]
    expense_splits: tuple[tuple[Expense, ExpenseSplit], ...]
