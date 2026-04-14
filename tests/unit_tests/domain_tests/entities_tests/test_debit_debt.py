from datetime import date
from decimal import Decimal
from uuid import uuid4

from hamcrest import assert_that
from hamcrest import has_length
from hamcrest import has_properties
import pytest

from tracker.domain.entities.debit_debt import DebitDebt
from tracker.domain.entities.debit_debt import DebitDebtId
from tracker.domain.entities.income_category import IncomeCategoryId
from tracker.domain.entities.person import PersonId
from tracker.domain.enums.currency import Currency
from tracker.domain.values.dough import Dough
from tracker.domain.values.payment_schedule import PaymentSchedule


@pytest.mark.unit
class TestDebitDebt:
    @staticmethod
    def _make_debit_debt(debt_id: DebitDebtId | None = None) -> DebitDebt:
        return DebitDebt(
            id=debt_id or DebitDebtId(uuid4()),
            category=IncomeCategoryId(uuid4()),
            amount=Dough(amount=Decimal("300.00"), currency=Currency.RUB),
            received_by=PersonId(uuid4()),
            schedule=PaymentSchedule.create_one_time_payment(on=date(2024, 6, 1)),
            description="Loan repayment",
        )

    def test_creates_debit_debt_with_all_fields(self) -> None:
        debt_id = DebitDebtId(uuid4())
        category_id = IncomeCategoryId(uuid4())
        person_id = PersonId(uuid4())
        amount = Dough(amount=Decimal("750.00"), currency=Currency.RUB)
        schedule = PaymentSchedule.create_one_time_payment(on=date(2024, 3, 15))

        debt = DebitDebt(
            id=debt_id,
            category=category_id,
            amount=amount,
            received_by=person_id,
            schedule=schedule,
            description="Friend repayment",
        )

        assert_that(
            debt,
            has_properties(
                id=debt_id,
                category=category_id,
                amount=amount,
                received_by=person_id,
                schedule=schedule,
                description="Friend repayment",
            ),
        )

    def test_accepts_recurring_yearly_schedule(self) -> None:
        schedule = PaymentSchedule.create_yearly_payment(on=date(2024, 1, 1), year_number=5)
        debt = DebitDebt(
            id=DebitDebtId(uuid4()),
            category=IncomeCategoryId(uuid4()),
            amount=Dough(amount=Decimal("100.00"), currency=Currency.RUB),
            received_by=PersonId(uuid4()),
            schedule=schedule,
            description="",
        )

        assert_that(debt.schedule.dates, has_length(5))

    def test_description_can_be_empty_string(self) -> None:
        debt = self._make_debit_debt()
        debt.description = ""

        assert debt.description == ""
