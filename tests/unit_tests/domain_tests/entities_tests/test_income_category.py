from uuid import uuid4

from hamcrest import assert_that
from hamcrest import has_properties
from hamcrest import none
from hamcrest import not_none
import pytest

from tracker.domain.entities.income_category import IncomeCategory
from tracker.domain.entities.income_category import IncomeCategoryId
from tracker.domain.entities.person import PersonId
from tracker.domain.errors import ValidationError
from tracker.domain.values.category_name import CategoryName


@pytest.mark.unit
class TestIncomeCategory:
    @staticmethod
    def _make_default_category(category_id: IncomeCategoryId | None = None) -> IncomeCategory:
        return IncomeCategory(
            id=category_id or IncomeCategoryId(uuid4()),
            name=CategoryName(value="Salary"),
            is_default=True,
            owner=None,
        )

    @staticmethod
    def _make_custom_category(
        category_id: IncomeCategoryId | None = None,
        owner_id: PersonId | None = None,
    ) -> IncomeCategory:
        return IncomeCategory(
            id=category_id or IncomeCategoryId(uuid4()),
            name=CategoryName(value="Salary"),
            is_default=False,
            owner=owner_id or PersonId(uuid4()),
        )

    def test_default_category_has_no_owner(self) -> None:
        category = self._make_default_category()

        assert_that(category, has_properties(is_default=True, owner=none()))  # type: ignore[arg-type]

    def test_custom_category_has_owner(self) -> None:
        owner_id = PersonId(uuid4())
        category = self._make_custom_category(owner_id=owner_id)

        assert_that(category, has_properties(is_default=False, owner=not_none()))  # type: ignore[arg-type]

    @pytest.mark.parametrize("name", ["Salary", "Freelance", "ab", "A" * 50, "side-hustle", "income_2"])
    def test_accepts_valid_category_names(self, name: str) -> None:
        category = IncomeCategory(
            id=IncomeCategoryId(uuid4()),
            name=CategoryName(value=name),
            is_default=True,
            owner=None,
        )

        assert category.name == CategoryName(value=name)

    def test_default_category_with_owner_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError, match="default category must not have an owner"):
            IncomeCategory(
                id=IncomeCategoryId(uuid4()),
                name=CategoryName(value="Salary"),
                is_default=True,
                owner=PersonId(uuid4()),
            )

    def test_non_default_category_without_owner_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError, match="non-default category must have an owner"):
            IncomeCategory(
                id=IncomeCategoryId(uuid4()),
                name=CategoryName(value="Salary"),
                is_default=False,
                owner=None,
            )
