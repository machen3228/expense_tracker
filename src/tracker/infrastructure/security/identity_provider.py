from tracker.application.errors.auth import AuthenticationError
from tracker.application.errors.auth import InvalidTokenError
from tracker.application.interfaces.readers.person import IPersonReader
from tracker.application.interfaces.security.identity_provider import IIdentityProvider
from tracker.application.interfaces.security.jwt_provider import IJWTProvider
from tracker.application.interfaces.security.jwt_provider import TokenData
from tracker.application.interfaces.security.jwt_provider import TokenType
from tracker.domain.entities.person import Person


class IdentityProvider(IIdentityProvider):
    def __init__(
        self,
        token: str,
        jwt_provider: IJWTProvider,
        person_reader: IPersonReader,
    ) -> None:
        self._token: str = token
        self._jwt_provider: IJWTProvider = jwt_provider
        self._person_reader: IPersonReader = person_reader
        self._cached_person: Person | None = None

    async def get_person(self) -> Person:
        if self._cached_person is not None:
            return self._cached_person

        person: Person = await self._get_person_from_token()
        self._cached_person = person
        return person

    async def _get_person_from_token(self) -> Person:
        token_data: TokenData = self._jwt_provider.decode_token(self._token)

        if token_data.meta.type != TokenType.ACCESS:
            raise InvalidTokenError(f"Token type must be '{TokenType.ACCESS}'")

        person: Person | None = await self._person_reader.get_by_id(token_data.payload.sub)
        if person is None:
            raise AuthenticationError("Person no longer exists")

        return person
