from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Protocol

if TYPE_CHECKING:
    from tracker.domain.values.password import Password


class IPasswordHasher(Protocol):
    @abstractmethod
    def hash_password(self, password: Password) -> bytes: ...

    @abstractmethod
    def verify_password(self, raw: str, hashed: bytes) -> bool: ...
