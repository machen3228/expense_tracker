from typing import NewType
from uuid import UUID
from uuid import uuid4

import pytest

from tracker.domain.entities.base import Entity
from tracker.domain.entities.base import entity

_ConcreteId = NewType("_ConcreteId", UUID)
_OtherId = NewType("_OtherId", UUID)


@entity
class _ConcreteEntity(Entity[_ConcreteId]):
    name: str


@entity
class _OtherEntity(Entity[_OtherId]):
    name: str


@pytest.mark.unit
class TestEntity:
    @staticmethod
    def _make_entity(entity_id: _ConcreteId | None = None, name: str = "x") -> _ConcreteEntity:
        return _ConcreteEntity(id=entity_id or _ConcreteId(uuid4()), name=name)

    def test_base_entity_cannot_be_instantiated_directly(self) -> None:
        with pytest.raises(TypeError):
            Entity(id=uuid4())

    def test_id_cannot_be_changed_after_construction(self) -> None:
        e = self._make_entity()

        with pytest.raises(AttributeError, match="Changing entity ID is not permitted"):
            e.id = _ConcreteId(uuid4())

    def test_other_fields_are_mutable(self) -> None:
        e = self._make_entity(name="original")
        e.name = "updated"

        assert e.name == "updated"

    def test_entities_with_same_id_and_type_are_equal(self) -> None:
        shared_id = _ConcreteId(uuid4())
        e1 = _ConcreteEntity(id=shared_id, name="alice")
        e2 = _ConcreteEntity(id=shared_id, name="bob")

        assert e1 == e2

    def test_entities_with_different_ids_are_not_equal(self) -> None:
        e1 = self._make_entity()
        e2 = self._make_entity()

        assert e1 != e2

    def test_entities_of_different_types_are_not_equal_even_with_same_raw_id(self) -> None:
        raw = uuid4()
        e1 = _ConcreteEntity(id=_ConcreteId(raw), name="x")
        e2 = _OtherEntity(id=_OtherId(raw), name="x")

        assert e1 != e2

    def test_entity_is_not_equal_to_non_entity(self) -> None:
        e = self._make_entity()
        non_entity_int = 42

        assert e != "not an entity"
        assert e != non_entity_int

    def test_equal_entities_produce_same_hash(self) -> None:
        shared_id = _ConcreteId(uuid4())
        e1 = _ConcreteEntity(id=shared_id, name="foo")
        e2 = _ConcreteEntity(id=shared_id, name="bar")

        assert hash(e1) == hash(e2)

    def test_entities_can_be_used_as_dict_keys(self) -> None:
        e = self._make_entity()
        d = {e: "value"}

        assert d[e] == "value"

    def test_entities_can_be_stored_in_sets(self) -> None:
        shared_id = _ConcreteId(uuid4())
        e1 = _ConcreteEntity(id=shared_id, name="first")
        e2 = _ConcreteEntity(id=shared_id, name="second")

        assert len({e1, e2}) == 1

    def test_different_types_same_raw_id_produce_different_hashes(self) -> None:
        raw = uuid4()
        e1 = _ConcreteEntity(id=_ConcreteId(raw), name="x")
        e2 = _OtherEntity(id=_OtherId(raw), name="x")

        assert hash(e1) != hash(e2)
