from typing import TYPE_CHECKING

from adaptix import P
from adaptix.conversion import link

from tracker.domain.entities.person import Person
from tracker.domain.entities.person import PersonId
from tracker.domain.values.person_name import PersonName
from tracker.infrastructure.database.mapper import get_mapper
from tracker.infrastructure.database.models.person import PersonORM
from tracker.infrastructure.database.readers.base import SAAbstractReader

if TYPE_CHECKING:
    from collections.abc import Callable


_to_domain: Callable[[PersonORM], Person] = get_mapper(
    PersonORM,
    Person,
    recipe=[
        link(P[PersonORM].username, P[Person].username, coercer=lambda n: PersonName(value=n)),
    ],
)


class SAPersonReader(SAAbstractReader[Person, PersonORM]):
    _model = PersonORM

    def _to_domain(self, orm_obj: PersonORM) -> Person:
        return _to_domain(orm_obj)

    async def get_by_id(self, _id: PersonId) -> Person | None:
        return await self._get(PersonORM.id == _id)

    async def get_by_username(self, username: PersonName) -> Person | None:
        return await self._get(PersonORM.username == username.value)
