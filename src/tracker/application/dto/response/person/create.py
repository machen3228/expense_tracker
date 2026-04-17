from typing import TYPE_CHECKING
from typing import Self

from tracker.application.dto.base import dto

if TYPE_CHECKING:
    from tracker.domain.entities.person import Person
    from tracker.domain.entities.person import PersonId


@dto
class CreatePersonResponse:
    id: PersonId
    username: str

    @classmethod
    def from_domain(cls, entity: Person) -> Self:
        return cls(
            id=entity.id,
            username=entity.username.value,
        )
