from datetime import UTC
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import has_properties
import pytest

from tracker.domain.entities.income import Income
from tracker.domain.entities.income import IncomeId
from tracker.domain.entities.income_category import IncomeCategoryId
from tracker.domain.entities.person import PersonId
from tracker.domain.enums.currency import Currency
from tracker.domain.values.dough import Dough


@pytest.mark.unit
class TestIncome:
    @staticmethod
    def _make_income(income_id: IncomeId | None = None) -> Income:
        return Income(
            id=income_id or IncomeId(uuid4()),
            amount=Dough(amount=Decimal("1000.00"), currency=Currency.RUB),
            category=IncomeCategoryId(uuid4()),
            description="Salary",
            received_by=PersonId(uuid4()),
            created_at=datetime(2024, 1, 31, 18, 0, tzinfo=UTC),
        )

    def test_creates_income_with_all_fields(self) -> None:
        income_id = IncomeId(uuid4())
        category_id = IncomeCategoryId(uuid4())
        person_id = PersonId(uuid4())
        amount = Dough(amount=Decimal("5000.00"), currency=Currency.RUB)
        created_at = datetime(2024, 12, 31, 23, 59, tzinfo=UTC)

        income = Income(
            id=income_id,
            amount=amount,
            category=category_id,
            description="Year-end bonus",
            received_by=person_id,
            created_at=created_at,
        )

        assert_that(
            income,
            has_properties(
                id=income_id,
                amount=amount,
                category=category_id,
                description="Year-end bonus",
                received_by=person_id,
                created_at=created_at,
            ),
        )

    def test_description_can_be_empty_string(self) -> None:
        income = Income(
            id=IncomeId(uuid4()),
            amount=Dough(amount=Decimal("100.00"), currency=Currency.RUB),
            category=IncomeCategoryId(uuid4()),
            description="",
            received_by=PersonId(uuid4()),
            created_at=datetime(2024, 1, 1, tzinfo=UTC),
        )

        assert_that(income.description, equal_to(""))
