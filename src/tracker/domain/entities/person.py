from typing import TYPE_CHECKING
from typing import NewType
from uuid import UUID

from tracker.domain.entities.base import Entity
from tracker.domain.entities.base import entity

if TYPE_CHECKING:
    from tracker.domain.values.person_name import PersonName

PersonId = NewType("PersonId", UUID)


@entity
class Person(Entity[PersonId]):
    username: PersonName
    password_hash: bytes
