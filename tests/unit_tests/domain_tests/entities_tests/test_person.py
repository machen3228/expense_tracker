from uuid import uuid4

from hamcrest import assert_that
from hamcrest import has_properties
import pytest

from tracker.domain.entities.person import Person
from tracker.domain.entities.person import PersonId
from tracker.domain.values.person_name import PersonName


@pytest.mark.unit
class TestPerson:
    @staticmethod
    def _make_person(person_id: PersonId | None = None, username: str = "alice") -> Person:
        return Person(
            id=person_id or PersonId(uuid4()),
            username=PersonName(value=username),
            password_hash=b"hashed",
        )

    def test_creates_person_with_all_fields(self) -> None:
        person_id = PersonId(uuid4())
        name = PersonName(value="alice")

        person = Person(id=person_id, username=name, password_hash=b"secret_hash")

        assert_that(person, has_properties(id=person_id, username=name, password_hash=b"secret_hash"))

    def test_password_hash_accepts_arbitrary_bytes(self) -> None:
        person = self._make_person()
        person.password_hash = b"\x00\xff\xab" * 32

        assert person.password_hash == b"\x00\xff\xab" * 32

    def test_username_can_be_replaced(self) -> None:
        person = self._make_person(username="alice")
        person.username = PersonName(value="bob123")

        assert person.username == PersonName(value="bob123")

    def test_password_hash_can_be_replaced(self) -> None:
        person = self._make_person()
        person.password_hash = b"new_hash"

        assert person.password_hash == b"new_hash"
