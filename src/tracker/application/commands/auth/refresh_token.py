from tracker.application.dto.request.auth.refresh_token import RefreshTokenRequest
from tracker.application.dto.response.auth.refresh_token import RefreshTokenResponse
from tracker.application.dto.response.person.base import PersonView
from tracker.application.errors.auth import AuthenticationError
from tracker.application.errors.auth import InvalidTokenError
from tracker.application.interfaces.interactor import Interactor
from tracker.application.interfaces.readers.person import IPersonReader
from tracker.application.interfaces.security.jwt_provider import IJWTProvider
from tracker.application.interfaces.security.jwt_provider import TokenData
from tracker.application.interfaces.security.jwt_provider import TokenPayload
from tracker.application.interfaces.security.jwt_provider import TokenType
from tracker.domain.entities.person import Person


class RefreshToken(Interactor[RefreshTokenRequest, RefreshTokenResponse]):
    def __init__(
        self,
        person_reader: IPersonReader,
        jwt_provider: IJWTProvider,
    ) -> None:
        self._person_reader: IPersonReader = person_reader
        self._jwt_provider: IJWTProvider = jwt_provider

    async def execute(self, request: RefreshTokenRequest) -> RefreshTokenResponse:
        decoded: TokenData = self._jwt_provider.decode_token(request.refresh_token)

        if decoded.meta.type != TokenType.REFRESH:
            raise InvalidTokenError(f"Token type must be '{TokenType.REFRESH}'")

        person: Person | None = await self._person_reader.get_by_id(decoded.payload.sub)
        if person is None:
            raise AuthenticationError("User no longer exists")

        payload = TokenPayload(sub=person.id)
        access_token = self._jwt_provider.create_access_token(payload)
        refresh_token = self._jwt_provider.create_refresh_token(payload)

        return RefreshTokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            person=PersonView.from_domain(person),
        )
