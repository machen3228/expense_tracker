from datetime import date
from decimal import Decimal
from uuid import uuid4

from hamcrest import assert_that
from hamcrest import has_length
from hamcrest import has_properties
import pytest

from tracker.domain.entities.credit_debt import CreditDebt
from tracker.domain.entities.credit_debt import CreditDebtId
from tracker.domain.entities.expense_category import ExpenseCategoryId
from tracker.domain.entities.person import PersonId
from tracker.domain.enums.currency import Currency
from tracker.domain.values.dough import Dough
from tracker.domain.values.payment_schedule import PaymentSchedule


@pytest.mark.unit
class TestCreditDebt:
    @staticmethod
    def _make_credit_debt(debt_id: CreditDebtId | None = None) -> CreditDebt:
        return CreditDebt(
            id=debt_id or CreditDebtId(uuid4()),
            category=ExpenseCategoryId(uuid4()),
            amount=Dough(amount=Decimal("500.00"), currency=Currency.RUB),
            paid_by=PersonId(uuid4()),
            schedule=PaymentSchedule.create_one_time_payment(on=date(2024, 6, 1)),
            description="Rent",
        )

    def test_creates_credit_debt_with_all_fields(self) -> None:
        debt_id = CreditDebtId(uuid4())
        category_id = ExpenseCategoryId(uuid4())
        person_id = PersonId(uuid4())
        amount = Dough(amount=Decimal("1200.00"), currency=Currency.RUB)
        schedule = PaymentSchedule.create_one_time_payment(on=date(2024, 12, 1))

        debt = CreditDebt(
            id=debt_id,
            category=category_id,
            amount=amount,
            paid_by=person_id,
            schedule=schedule,
            description="Monthly rent",
        )

        assert_that(
            debt,
            has_properties(
                id=debt_id,
                category=category_id,
                amount=amount,
                paid_by=person_id,
                schedule=schedule,
                description="Monthly rent",
            ),
        )

    def test_accepts_recurring_monthly_schedule(self) -> None:
        schedule = PaymentSchedule.create_monthly_payment(on=date(2024, 1, 1), months_number=12)
        debt = CreditDebt(
            id=CreditDebtId(uuid4()),
            category=ExpenseCategoryId(uuid4()),
            amount=Dough(amount=Decimal("100.00"), currency=Currency.RUB),
            paid_by=PersonId(uuid4()),
            schedule=schedule,
            description="",
        )

        assert_that(debt.schedule.dates, has_length(12))

    def test_description_can_be_empty_string(self) -> None:
        debt = self._make_credit_debt()
        debt.description = ""

        assert debt.description == ""
