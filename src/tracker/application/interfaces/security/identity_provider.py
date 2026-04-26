from abc import abstractmethod
from typing import Protocol

from tracker.domain.entities.person import Person


class IIdentityProvider(Protocol):
    @abstractmethod
    async def get_person(self) -> Person: ...
