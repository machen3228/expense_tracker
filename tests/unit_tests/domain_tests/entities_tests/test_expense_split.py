from decimal import Decimal
from uuid import uuid4

from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import has_entries
from hamcrest import has_length
from hamcrest import has_properties
import pytest

from tracker.domain.entities.expense import ExpenseId
from tracker.domain.entities.expense_split import ExpenseSplit
from tracker.domain.entities.expense_split import ExpenseSplitId
from tracker.domain.entities.person import PersonId
from tracker.domain.enums.currency import Currency
from tracker.domain.errors import ValidationError
from tracker.domain.values.dough import Dough


@pytest.mark.unit
class TestExpenseSplit:
    @staticmethod
    def _rub(amount: str) -> Dough:
        return Dough(amount=Decimal(amount), currency=Currency.RUB)

    def _make_split(
        self,
        *,
        split_id: ExpenseSplitId | None = None,
        total: str = "100.00",
        shares: dict[PersonId, Dough] | None = None,
    ) -> ExpenseSplit:
        if shares is None:
            person = PersonId(uuid4())
            shares = {person: self._rub(total)}
        return ExpenseSplit(
            id=split_id or ExpenseSplitId(uuid4()),
            expense_id=ExpenseId(uuid4()),
            total_amount=self._rub(total),
            shares=shares,
        )

    def test_single_person_receives_full_amount(self) -> None:
        person = PersonId(uuid4())

        split = self._make_split(total="150.00", shares={person: self._rub("150.00")})

        assert_that(
            split,
            has_properties(
                total_amount=self._rub("150.00"),
                shares=has_entries({person: self._rub("150.00")}),  # type: ignore[arg-type]
            ),
        )

    def test_two_persons_split_equally(self) -> None:
        p1, p2 = PersonId(uuid4()), PersonId(uuid4())

        split = self._make_split(total="100.00", shares={p1: self._rub("50.00"), p2: self._rub("50.00")})

        assert_that(split.shares, has_entries({p1: self._rub("50.00"), p2: self._rub("50.00")}))

    def test_stores_all_persons_in_shares(self) -> None:
        persons = [PersonId(uuid4()) for _ in range(5)]
        shares = {p: self._rub("20.00") for p in persons}

        split = self._make_split(total="100.00", shares=shares)

        assert_that(split.shares, has_length(5))

    @pytest.mark.parametrize(
        ("total", "share_amounts"),
        [
            ("100.00", ["50.00", "50.00"]),
            ("200.00", ["100.00", "60.00", "40.00"]),
            ("0.01", ["0.01"]),
            ("999.99", ["333.33", "333.33", "333.33"]),
        ],
    )
    def test_valid_splits_are_accepted(self, total: str, share_amounts: list[str]) -> None:
        persons = [PersonId(uuid4()) for _ in share_amounts]
        shares = dict(zip(persons, [self._rub(a) for a in share_amounts], strict=True))

        split = self._make_split(total=total, shares=shares)

        assert_that(split.total_amount, equal_to(self._rub(total)))

    def test_mutating_original_dict_does_not_affect_split(self) -> None:
        person = PersonId(uuid4())
        original_shares: dict[PersonId, Dough] = {person: self._rub("100.00")}
        split = ExpenseSplit(
            id=ExpenseSplitId(uuid4()),
            expense_id=ExpenseId(uuid4()),
            total_amount=self._rub("100.00"),
            shares=original_shares,
        )

        extra_person = PersonId(uuid4())
        original_shares[extra_person] = self._rub("50.00")

        assert extra_person not in split.shares

    def test_empty_shares_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError, match="must have at least one share"):
            ExpenseSplit(
                id=ExpenseSplitId(uuid4()),
                expense_id=ExpenseId(uuid4()),
                total_amount=self._rub("100.00"),
                shares={},
            )

    def test_shares_summing_more_than_total_raises_validation_error(self) -> None:
        p1, p2 = PersonId(uuid4()), PersonId(uuid4())

        with pytest.raises(ValidationError, match="Shares sum to"):
            ExpenseSplit(
                id=ExpenseSplitId(uuid4()),
                expense_id=ExpenseId(uuid4()),
                total_amount=self._rub("100.00"),
                shares={p1: self._rub("60.00"), p2: self._rub("60.00")},
            )

    def test_shares_summing_less_than_total_raises_validation_error(self) -> None:
        person = PersonId(uuid4())

        with pytest.raises(ValidationError, match="Shares sum to"):
            ExpenseSplit(
                id=ExpenseSplitId(uuid4()),
                expense_id=ExpenseId(uuid4()),
                total_amount=self._rub("100.00"),
                shares={person: self._rub("99.99")},
            )
