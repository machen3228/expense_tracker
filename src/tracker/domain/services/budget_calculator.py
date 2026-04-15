from typing import TYPE_CHECKING
from typing import Any

from tracker.domain.enums import BudgetSource
from tracker.domain.enums import FlowType
from tracker.domain.values.budget_line import BudgetLine
from tracker.domain.values.budget_report import BudgetReport
from tracker.domain.values.dough import Dough

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterable

    from tracker.domain.entities.expense import Expense
    from tracker.domain.entities.expense_split import ExpenseSplit
    from tracker.domain.values.date_range import DateRange
    from tracker.domain.values.person_ledger import PersonLedger


class BudgetCalculator:
    def calculate(self, period: DateRange, ledger: PersonLedger) -> BudgetReport:
        lines = (
            self._income_lines(period, ledger)
            + self._expense_lines(period, ledger)
            + self._credit_debt_lines(period, ledger)
            + self._debit_debt_lines(period, ledger)
            + self._split_lines(period, ledger)
        )
        lines.sort(key=lambda line: line.date)
        return BudgetReport(period=period, lines=tuple(lines))

    def _income_lines(self, period: DateRange, ledger: PersonLedger) -> list[BudgetLine]:
        return self._lines_from_items(
            ledger.incomes,
            lambda i: i.received_by == ledger.person_id,
            period,
            FlowType.INCOME,
            BudgetSource.INCOME,
        )

    def _expense_lines(self, period: DateRange, ledger: PersonLedger) -> list[BudgetLine]:
        return self._lines_from_items(
            ledger.expenses,
            lambda e: e.paid_by == ledger.person_id,
            period,
            FlowType.EXPENSE,
            BudgetSource.EXPENSE,
        )

    @staticmethod
    def _lines_from_items(
        items: Iterable[Any],
        is_owner: Callable[[Any], bool],
        period: DateRange,
        flow: FlowType,
        source: BudgetSource,
    ) -> list[BudgetLine]:
        lines: list[BudgetLine] = []
        for item in items:
            if not is_owner(item):
                continue
            if not period.contains(item.created_at.date()):
                continue
            lines.append(
                BudgetLine(
                    date=item.created_at.date(),
                    amount=item.amount,
                    flow=flow,
                    source=source,
                    description=item.description,
                )
            )
        return lines

    def _credit_debt_lines(self, period: DateRange, ledger: PersonLedger) -> list[BudgetLine]:
        return self._debt_lines(
            ledger.credit_debts,
            lambda d: d.paid_by == ledger.person_id,
            period,
            FlowType.EXPENSE,
            BudgetSource.CREDIT_DEBT,
        )

    def _debit_debt_lines(self, period: DateRange, ledger: PersonLedger) -> list[BudgetLine]:
        return self._debt_lines(
            ledger.debit_debts,
            lambda d: d.received_by == ledger.person_id,
            period,
            FlowType.INCOME,
            BudgetSource.DEBIT_DEBT,
        )

    @staticmethod
    def _debt_lines(
        debts: Iterable[Any],
        is_owner: Callable[[Any], bool],
        period: DateRange,
        flow: FlowType,
        source: BudgetSource,
    ) -> list[BudgetLine]:
        lines: list[BudgetLine] = []
        for debt in debts:
            if not is_owner(debt):
                continue
            lines.extend(
                BudgetLine(
                    date=payment_date,
                    amount=debt.amount,
                    flow=flow,
                    source=source,
                    description=debt.description,
                )
                for payment_date in debt.schedule.dates
                if period.contains(payment_date)
            )
        return lines

    def _split_lines(self, period: DateRange, ledger: PersonLedger) -> list[BudgetLine]:
        lines: list[BudgetLine] = []
        for expense, split in ledger.expense_splits:
            if not period.contains(expense.created_at.date()):
                continue
            if expense.paid_by == ledger.person_id:
                lines.extend(self._split_receivable_lines(expense, split, ledger))
            elif ledger.person_id in split.shares:
                lines.append(self._split_payable_line(expense, split, ledger))
        return lines

    @staticmethod
    def _split_receivable_lines(expense: Expense, split: ExpenseSplit, ledger: PersonLedger) -> list[BudgetLine]:
        own_share = split.shares.get(ledger.person_id)
        if own_share is None:
            return []
        others_total = split.total_amount.amount - own_share.amount
        if others_total <= 0:
            return []
        return [
            BudgetLine(
                date=expense.created_at.date(),
                amount=Dough(amount=others_total, currency=split.total_amount.currency),
                flow=FlowType.INCOME,
                source=BudgetSource.SPLIT_RECEIVABLE,
                description=f"Split receivable: {expense.description}",
            )
        ]

    @staticmethod
    def _split_payable_line(expense: Expense, split: ExpenseSplit, ledger: PersonLedger) -> BudgetLine:
        return BudgetLine(
            date=expense.created_at.date(),
            amount=split.shares[ledger.person_id],
            flow=FlowType.EXPENSE,
            source=BudgetSource.SPLIT_PAYABLE,
            description=f"Split payable: {expense.description}",
        )
