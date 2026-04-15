from datetime import UTC
from datetime import date
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from hamcrest import assert_that
from hamcrest import contains_inanyorder
from hamcrest import empty
from hamcrest import equal_to
from hamcrest import has_length
from hamcrest import has_properties
import pytest

from tracker.domain.entities.credit_debt import CreditDebt
from tracker.domain.entities.credit_debt import CreditDebtId
from tracker.domain.entities.debit_debt import DebitDebt
from tracker.domain.entities.debit_debt import DebitDebtId
from tracker.domain.entities.expense import Expense
from tracker.domain.entities.expense import ExpenseId
from tracker.domain.entities.expense_category import ExpenseCategoryId
from tracker.domain.entities.expense_split import ExpenseSplit
from tracker.domain.entities.expense_split import ExpenseSplitId
from tracker.domain.entities.income import Income
from tracker.domain.entities.income import IncomeId
from tracker.domain.entities.income_category import IncomeCategoryId
from tracker.domain.entities.person import PersonId
from tracker.domain.enums import BudgetSource
from tracker.domain.enums import FlowType
from tracker.domain.enums.currency import Currency
from tracker.domain.services.budget_calculator import BudgetCalculator
from tracker.domain.values.date_range import DateRange
from tracker.domain.values.dough import Dough
from tracker.domain.values.payment_schedule import PaymentSchedule
from tracker.domain.values.person_ledger import PersonLedger


@pytest.mark.unit
class TestBudgetCalculator:
    def setup_method(self) -> None:
        self.calculator = BudgetCalculator()
        self.person_id = PersonId(uuid4())
        self.period = DateRange.for_month(year=2024, month=1)

    @staticmethod
    def _rub(amount: str) -> Dough:
        return Dough(amount=Decimal(amount), currency=Currency.RUB)

    @staticmethod
    def _at(d: date) -> datetime:
        return datetime(d.year, d.month, d.day, 12, 0, tzinfo=UTC)

    def _make_expense(
        self, *, paid_by: PersonId, amount: str, created_at: date, description: str = "Expense"
    ) -> Expense:
        return Expense(
            id=ExpenseId(uuid4()),
            amount=self._rub(amount),
            category=ExpenseCategoryId(uuid4()),
            description=description,
            paid_by=paid_by,
            created_at=self._at(created_at),
        )

    def _make_income(
        self, *, received_by: PersonId, amount: str, created_at: date, description: str = "Income"
    ) -> Income:
        return Income(
            id=IncomeId(uuid4()),
            amount=self._rub(amount),
            category=IncomeCategoryId(uuid4()),
            description=description,
            received_by=received_by,
            created_at=self._at(created_at),
        )

    def _make_credit_debt(
        self, *, paid_by: PersonId, amount: str, schedule: PaymentSchedule, description: str = "Credit debt"
    ) -> CreditDebt:
        return CreditDebt(
            id=CreditDebtId(uuid4()),
            category=ExpenseCategoryId(uuid4()),
            amount=self._rub(amount),
            paid_by=paid_by,
            schedule=schedule,
            description=description,
        )

    def _make_debit_debt(
        self, *, received_by: PersonId, amount: str, schedule: PaymentSchedule, description: str = "Debit debt"
    ) -> DebitDebt:
        return DebitDebt(
            id=DebitDebtId(uuid4()),
            category=IncomeCategoryId(uuid4()),
            amount=self._rub(amount),
            received_by=received_by,
            schedule=schedule,
            description=description,
        )

    def _make_split(self, *, expense: Expense, shares: dict[PersonId, Dough]) -> ExpenseSplit:
        total = sum((s.amount for s in shares.values()), start=Decimal(0))
        return ExpenseSplit(
            id=ExpenseSplitId(uuid4()),
            expense_id=expense.id,
            total_amount=self._rub(str(total)),
            shares=shares,
        )

    def _make_ledger(
        self,
        *,
        expenses: tuple[Expense, ...] = (),
        incomes: tuple[Income, ...] = (),
        credit_debts: tuple[CreditDebt, ...] = (),
        debit_debts: tuple[DebitDebt, ...] = (),
        expense_splits: tuple[tuple[Expense, ExpenseSplit], ...] = (),
    ) -> PersonLedger:
        return PersonLedger(
            person_id=self.person_id,
            expenses=expenses,
            incomes=incomes,
            credit_debts=credit_debts,
            debit_debts=debit_debts,
            expense_splits=expense_splits,
        )

    def test_empty_ledger_returns_empty_report(self) -> None:
        report = self.calculator.calculate(self.period, self._make_ledger())

        assert_that(report.lines, empty())

    def test_empty_ledger_totals_are_zero(self) -> None:
        report = self.calculator.calculate(self.period, self._make_ledger())

        assert_that(
            report,
            has_properties(
                total_income=Decimal(0),
                total_expenses=Decimal(0),
                net_balance=Decimal(0),
            ),
        )

    def test_income_owned_by_person_appears_in_report(self) -> None:
        income = self._make_income(received_by=self.person_id, amount="500.00", created_at=date(2024, 1, 10))

        report = self.calculator.calculate(self.period, self._make_ledger(incomes=(income,)))

        assert_that(report.lines, has_length(1))
        assert_that(
            report.lines[0],
            has_properties(
                flow=FlowType.INCOME,
                source=BudgetSource.INCOME,
                amount=self._rub("500.00"),
                date=date(2024, 1, 10),
                description="Income",
            ),
        )

    def test_income_owned_by_another_person_is_excluded(self) -> None:
        other = PersonId(uuid4())
        income = self._make_income(received_by=other, amount="500.00", created_at=date(2024, 1, 10))

        report = self.calculator.calculate(self.period, self._make_ledger(incomes=(income,)))

        assert_that(report.lines, empty())

    def test_income_outside_period_is_excluded(self) -> None:
        income = self._make_income(received_by=self.person_id, amount="500.00", created_at=date(2024, 2, 1))

        report = self.calculator.calculate(self.period, self._make_ledger(incomes=(income,)))

        assert_that(report.lines, empty())

    def test_expense_paid_by_person_appears_in_report(self) -> None:
        expense = self._make_expense(paid_by=self.person_id, amount="200.00", created_at=date(2024, 1, 5))

        report = self.calculator.calculate(self.period, self._make_ledger(expenses=(expense,)))

        assert_that(report.lines, has_length(1))
        assert_that(
            report.lines[0],
            has_properties(
                flow=FlowType.EXPENSE,
                source=BudgetSource.EXPENSE,
                amount=self._rub("200.00"),
                date=date(2024, 1, 5),
            ),
        )

    def test_expense_paid_by_another_person_is_excluded(self) -> None:
        other = PersonId(uuid4())
        expense = self._make_expense(paid_by=other, amount="200.00", created_at=date(2024, 1, 5))

        report = self.calculator.calculate(self.period, self._make_ledger(expenses=(expense,)))

        assert_that(report.lines, empty())

    def test_expense_outside_period_is_excluded(self) -> None:
        expense = self._make_expense(paid_by=self.person_id, amount="200.00", created_at=date(2023, 12, 31))

        report = self.calculator.calculate(self.period, self._make_ledger(expenses=(expense,)))

        assert_that(report.lines, empty())

    def test_credit_debt_payment_within_period_appears_as_expense(self) -> None:
        schedule = PaymentSchedule.create_one_time_payment(on=date(2024, 1, 15))
        debt = self._make_credit_debt(paid_by=self.person_id, amount="300.00", schedule=schedule)

        report = self.calculator.calculate(self.period, self._make_ledger(credit_debts=(debt,)))

        assert_that(report.lines, has_length(1))
        assert_that(
            report.lines[0],
            has_properties(
                flow=FlowType.EXPENSE,
                source=BudgetSource.CREDIT_DEBT,
                amount=self._rub("300.00"),
                date=date(2024, 1, 15),
            ),
        )

    def test_credit_debt_of_another_person_is_excluded(self) -> None:
        other = PersonId(uuid4())
        schedule = PaymentSchedule.create_one_time_payment(on=date(2024, 1, 15))
        debt = self._make_credit_debt(paid_by=other, amount="300.00", schedule=schedule)

        report = self.calculator.calculate(self.period, self._make_ledger(credit_debts=(debt,)))

        assert_that(report.lines, empty())

    def test_credit_debt_payment_outside_period_is_excluded(self) -> None:
        schedule = PaymentSchedule.create_monthly_payment(on=date(2024, 2, 1), months_number=2)
        debt = self._make_credit_debt(paid_by=self.person_id, amount="100.00", schedule=schedule)

        report = self.calculator.calculate(self.period, self._make_ledger(credit_debts=(debt,)))

        assert_that(report.lines, empty())

    def test_credit_debt_only_payments_within_period_are_included(self) -> None:
        schedule = PaymentSchedule.create_monthly_payment(on=date(2024, 1, 5), months_number=3)
        debt = self._make_credit_debt(paid_by=self.person_id, amount="100.00", schedule=schedule)

        report = self.calculator.calculate(self.period, self._make_ledger(credit_debts=(debt,)))

        january_lines = [line for line in report.lines if line.date.month == 1]
        assert_that(january_lines, has_length(1))

    def test_debit_debt_payment_within_period_appears_as_income(self) -> None:
        schedule = PaymentSchedule.create_one_time_payment(on=date(2024, 1, 20))
        debt = self._make_debit_debt(received_by=self.person_id, amount="150.00", schedule=schedule)

        report = self.calculator.calculate(self.period, self._make_ledger(debit_debts=(debt,)))

        assert_that(report.lines, has_length(1))
        assert_that(
            report.lines[0],
            has_properties(
                flow=FlowType.INCOME,
                source=BudgetSource.DEBIT_DEBT,
                amount=self._rub("150.00"),
                date=date(2024, 1, 20),
            ),
        )

    def test_debit_debt_of_another_person_is_excluded(self) -> None:
        other = PersonId(uuid4())
        schedule = PaymentSchedule.create_one_time_payment(on=date(2024, 1, 20))
        debt = self._make_debit_debt(received_by=other, amount="150.00", schedule=schedule)

        report = self.calculator.calculate(self.period, self._make_ledger(debit_debts=(debt,)))

        assert_that(report.lines, empty())

    def test_split_receivable_appears_when_person_paid_and_has_own_share(self) -> None:
        other = PersonId(uuid4())
        expense = self._make_expense(paid_by=self.person_id, amount="100.00", created_at=date(2024, 1, 10))
        split = self._make_split(
            expense=expense,
            shares={self.person_id: self._rub("50.00"), other: self._rub("50.00")},
        )

        report = self.calculator.calculate(self.period, self._make_ledger(expense_splits=((expense, split),)))

        receivable_lines = [line for line in report.lines if line.source == BudgetSource.SPLIT_RECEIVABLE]
        assert_that(receivable_lines, has_length(1))
        assert_that(
            receivable_lines[0],
            has_properties(
                flow=FlowType.INCOME,
                amount=self._rub("50.00"),
                description="Split receivable: Expense",
            ),
        )

    def test_split_receivable_not_created_when_person_holds_full_share(self) -> None:
        expense = self._make_expense(paid_by=self.person_id, amount="100.00", created_at=date(2024, 1, 10))
        split = self._make_split(
            expense=expense,
            shares={self.person_id: self._rub("100.00")},
        )

        report = self.calculator.calculate(self.period, self._make_ledger(expense_splits=((expense, split),)))

        receivable_lines = [line for line in report.lines if line.source == BudgetSource.SPLIT_RECEIVABLE]
        assert_that(receivable_lines, empty())

    def test_split_receivable_not_created_when_person_is_not_the_payer(self) -> None:
        other = PersonId(uuid4())
        expense = self._make_expense(paid_by=other, amount="100.00", created_at=date(2024, 1, 10))
        split = self._make_split(
            expense=expense,
            shares={other: self._rub("60.00"), self.person_id: self._rub("40.00")},
        )

        report = self.calculator.calculate(self.period, self._make_ledger(expense_splits=((expense, split),)))

        receivable_lines = [line for line in report.lines if line.source == BudgetSource.SPLIT_RECEIVABLE]
        assert_that(receivable_lines, empty())

    def test_split_payable_appears_when_person_has_share_and_did_not_pay(self) -> None:
        other = PersonId(uuid4())
        expense = self._make_expense(paid_by=other, amount="100.00", created_at=date(2024, 1, 10))
        split = self._make_split(
            expense=expense,
            shares={other: self._rub("60.00"), self.person_id: self._rub("40.00")},
        )

        report = self.calculator.calculate(self.period, self._make_ledger(expense_splits=((expense, split),)))

        payable_lines = [line for line in report.lines if line.source == BudgetSource.SPLIT_PAYABLE]
        assert_that(payable_lines, has_length(1))
        assert_that(
            payable_lines[0],
            has_properties(
                flow=FlowType.EXPENSE,
                amount=self._rub("40.00"),
                description="Split payable: Expense",
            ),
        )

    def test_split_payable_not_created_when_person_has_no_share(self) -> None:
        other1, other2 = PersonId(uuid4()), PersonId(uuid4())
        expense = self._make_expense(paid_by=other1, amount="100.00", created_at=date(2024, 1, 10))
        split = self._make_split(
            expense=expense,
            shares={other1: self._rub("50.00"), other2: self._rub("50.00")},
        )

        report = self.calculator.calculate(self.period, self._make_ledger(expense_splits=((expense, split),)))

        assert_that(report.lines, empty())

    def test_split_outside_period_is_excluded(self) -> None:
        other = PersonId(uuid4())
        expense = self._make_expense(paid_by=other, amount="100.00", created_at=date(2024, 2, 5))
        split = self._make_split(
            expense=expense,
            shares={other: self._rub("60.00"), self.person_id: self._rub("40.00")},
        )

        report = self.calculator.calculate(self.period, self._make_ledger(expense_splits=((expense, split),)))

        assert_that(report.lines, empty())

    def test_lines_are_sorted_by_date(self) -> None:
        expense1 = self._make_expense(paid_by=self.person_id, amount="100.00", created_at=date(2024, 1, 20))
        expense2 = self._make_expense(paid_by=self.person_id, amount="50.00", created_at=date(2024, 1, 5))
        income = self._make_income(received_by=self.person_id, amount="200.00", created_at=date(2024, 1, 12))

        report = self.calculator.calculate(
            self.period,
            self._make_ledger(expenses=(expense1, expense2), incomes=(income,)),
        )

        dates = [line.date for line in report.lines]
        assert_that(dates, equal_to(sorted(dates)))

    def test_net_balance_combines_income_and_expenses(self) -> None:
        income = self._make_income(received_by=self.person_id, amount="1000.00", created_at=date(2024, 1, 10))
        expense = self._make_expense(paid_by=self.person_id, amount="400.00", created_at=date(2024, 1, 15))

        report = self.calculator.calculate(
            self.period,
            self._make_ledger(expenses=(expense,), incomes=(income,)),
        )

        assert_that(
            report,
            has_properties(
                total_income=Decimal("1000.00"),
                total_expenses=Decimal("400.00"),
                net_balance=Decimal("600.00"),
            ),
        )

    def test_report_period_matches_requested_period(self) -> None:
        report = self.calculator.calculate(self.period, self._make_ledger())

        assert_that(report.period, equal_to(self.period))

    def test_mixed_sources_produce_correct_line_count(self) -> None:
        income = self._make_income(received_by=self.person_id, amount="500.00", created_at=date(2024, 1, 1))
        expense = self._make_expense(paid_by=self.person_id, amount="200.00", created_at=date(2024, 1, 2))
        credit_schedule = PaymentSchedule.create_one_time_payment(on=date(2024, 1, 10))
        credit = self._make_credit_debt(paid_by=self.person_id, amount="100.00", schedule=credit_schedule)
        debit_schedule = PaymentSchedule.create_one_time_payment(on=date(2024, 1, 20))
        debit = self._make_debit_debt(received_by=self.person_id, amount="50.00", schedule=debit_schedule)

        report = self.calculator.calculate(
            self.period,
            self._make_ledger(
                incomes=(income,),
                expenses=(expense,),
                credit_debts=(credit,),
                debit_debts=(debit,),
            ),
        )

        sources: set[BudgetSource] = {line.source for line in report.lines}
        assert_that(report.lines, has_length(4))
        assert_that(  # type: ignore[misc]
            sources,
            contains_inanyorder(
                BudgetSource.INCOME,
                BudgetSource.EXPENSE,
                BudgetSource.CREDIT_DEBT,
                BudgetSource.DEBIT_DEBT,
            ),
        )
