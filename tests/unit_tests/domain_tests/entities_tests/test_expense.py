from datetime import UTC
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import has_properties
import pytest

from tracker.domain.entities.expense import Expense
from tracker.domain.entities.expense import ExpenseId
from tracker.domain.entities.expense_category import ExpenseCategoryId
from tracker.domain.entities.person import PersonId
from tracker.domain.enums.currency import Currency
from tracker.domain.values.dough import Dough


@pytest.mark.unit
class TestExpense:
    @staticmethod
    def _make_expense(expense_id: ExpenseId | None = None) -> Expense:
        return Expense(
            id=expense_id or ExpenseId(uuid4()),
            amount=Dough(amount=Decimal("50.00"), currency=Currency.RUB),
            category=ExpenseCategoryId(uuid4()),
            description="Groceries",
            paid_by=PersonId(uuid4()),
            created_at=datetime(2024, 1, 15, 10, 30, tzinfo=UTC),
        )

    def test_creates_expense_with_all_fields(self) -> None:
        expense_id = ExpenseId(uuid4())
        category_id = ExpenseCategoryId(uuid4())
        person_id = PersonId(uuid4())
        amount = Dough(amount=Decimal("99.99"), currency=Currency.RUB)
        created_at = datetime(2024, 6, 1, 12, 0, tzinfo=UTC)

        expense = Expense(
            id=expense_id,
            amount=amount,
            category=category_id,
            description="Lunch",
            paid_by=person_id,
            created_at=created_at,
        )

        assert_that(
            expense,
            has_properties(
                id=expense_id,
                amount=amount,
                category=category_id,
                description="Lunch",
                paid_by=person_id,
                created_at=created_at,
            ),
        )

    def test_description_can_be_empty_string(self) -> None:
        expense = Expense(
            id=ExpenseId(uuid4()),
            amount=Dough(amount=Decimal("10.00"), currency=Currency.RUB),
            category=ExpenseCategoryId(uuid4()),
            description="",
            paid_by=PersonId(uuid4()),
            created_at=datetime(2024, 1, 1, tzinfo=UTC),
        )

        assert_that(expense.description, equal_to(""))
