from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Protocol

if TYPE_CHECKING:
    from tracker.domain.entities.person import Person
    from tracker.domain.entities.person import PersonId
    from tracker.domain.values.person_name import PersonName


class IPersonReader(Protocol):
    @abstractmethod
    async def get_by_id(self, _id: PersonId) -> Person | None: ...

    @abstractmethod
    async def get_by_username(self, username: PersonName) -> Person | None: ...
