from typing import TYPE_CHECKING
from uuid import uuid4

from tracker.application.dto.request.person.create import CreatePersonRequest
from tracker.application.dto.response.person.base import PersonView
from tracker.application.dto.response.person.create import CreatePersonResponse
from tracker.application.interfaces.interactor import Interactor
from tracker.domain.entities.person import Person
from tracker.domain.entities.person import PersonId
from tracker.domain.errors.base import AlreadyExistsError
from tracker.domain.values.password import Password
from tracker.domain.values.person_name import PersonName

if TYPE_CHECKING:
    from tracker.application.interfaces.readers.person import IPersonReader
    from tracker.application.interfaces.repositories.person import IPersonRepository
    from tracker.application.interfaces.security.password_hasher import IPasswordHasher
    from tracker.application.interfaces.transaction_manager import ITransactionManager


class CreatePerson(Interactor[CreatePersonRequest, CreatePersonResponse]):
    def __init__(
        self,
        person_repository: IPersonRepository,
        person_reader: IPersonReader,
        password_hasher: IPasswordHasher,
        transaction_manager: ITransactionManager,
    ) -> None:
        self._person_repository = person_repository
        self._person_reader = person_reader
        self._password_hasher = password_hasher
        self._uow = transaction_manager

    async def execute(self, request: CreatePersonRequest) -> CreatePersonResponse:
        password = Password(value=request.password)
        password_hash: bytes = self._password_hasher.hash_password(password)

        person = Person(
            id=PersonId(uuid4()),
            username=PersonName(value=request.username),
            password_hash=password_hash,
        )

        await self._check_unique(person)
        await self._person_repository.add(person)
        await self._uow.commit()

        return CreatePersonResponse(person=PersonView.from_domain(person))

    async def _check_unique(self, person: Person) -> None:
        existing: Person | None = await self._person_reader.get_by_username(person.username)
        if existing is not None:
            raise AlreadyExistsError(f"Person with username '{person.username.value}' already exists")
