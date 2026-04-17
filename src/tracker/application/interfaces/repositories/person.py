from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Protocol

if TYPE_CHECKING:
    from tracker.domain.entities.person import Person


class IPersonRepository(Protocol):
    @abstractmethod
    async def add(self, entity: Person) -> None: ...

    @abstractmethod
    async def update(self, entity: Person) -> None: ...

    @abstractmethod
    async def delete(self, entity: Person) -> None: ...
