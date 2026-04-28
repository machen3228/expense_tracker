from tracker.application.dto.request.auth.login import LoginRequest
from tracker.application.dto.response.auth.login import LoginResponse
from tracker.application.dto.response.person.base import PersonView
from tracker.application.errors.auth import InvalidCredentialsError
from tracker.application.interfaces.interactor import Interactor
from tracker.application.interfaces.readers.person import IPersonReader
from tracker.application.interfaces.security.jwt_provider import IJWTProvider
from tracker.application.interfaces.security.jwt_provider import TokenPayload
from tracker.application.interfaces.security.password_hasher import IPasswordHasher
from tracker.domain.entities.person import Person
from tracker.domain.errors import ValidationError
from tracker.domain.values.person_name import PersonName


class LoginPerson(Interactor[LoginRequest, LoginResponse]):
    def __init__(
        self,
        person_reader: IPersonReader,
        password_hasher: IPasswordHasher,
        jwt_provider: IJWTProvider,
    ) -> None:
        self._person_reader: IPersonReader = person_reader
        self._password_hasher: IPasswordHasher = password_hasher
        self._jwt_provider: IJWTProvider = jwt_provider

    async def execute(self, request: LoginRequest) -> LoginResponse:
        exception = InvalidCredentialsError("Invalid username or password")

        try:
            username = PersonName(value=request.username)
        except ValidationError:
            raise exception from None

        person: Person | None = await self._person_reader.get_by_username(username)
        if person is None:
            raise exception

        if not self._password_hasher.verify_password(request.password, person.password_hash):
            raise exception

        payload = TokenPayload(sub=person.id)
        access_token = self._jwt_provider.create_access_token(payload)
        refresh_token = self._jwt_provider.create_refresh_token(payload)

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            person=PersonView.from_domain(person),
        )
