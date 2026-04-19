from typing import TYPE_CHECKING

from adaptix import P
from adaptix.conversion import link

from tracker.domain.entities.person import Person
from tracker.infrastructure.database.mapper import get_mapper
from tracker.infrastructure.database.models.person import PersonORM
from tracker.infrastructure.database.repositories.base import SAAbstractRepository

if TYPE_CHECKING:
    from collections.abc import Callable

_to_orm: Callable[[Person], PersonORM] = get_mapper(
    Person,
    PersonORM,
    recipe=[
        link(P[Person].username, P[PersonORM].username, coercer=lambda u: u.value),
    ],
)


class SAPersonRepository(SAAbstractRepository[Person, PersonORM]):
    def _to_orm(self, entity: Person) -> PersonORM:
        return _to_orm(entity)
