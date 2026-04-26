from abc import abstractmethod
from enum import StrEnum
from typing import Protocol

from tracker.application.dto.base import dto
from tracker.domain.entities.person import PersonId


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


@dto
class TokenPayload:
    sub: PersonId


@dto
class TokenMeta:
    type: TokenType
    iat: int
    exp: int


@dto
class TokenData:
    payload: TokenPayload
    meta: TokenMeta


class IJWTProvider(Protocol):
    @abstractmethod
    def create_access_token(self, payload: TokenPayload) -> str: ...

    @abstractmethod
    def create_refresh_token(self, payload: TokenPayload) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> TokenData: ...
