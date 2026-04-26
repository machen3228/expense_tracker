from tracker.application.dto.request.person.change_username import ChangePersonNameRequest
from tracker.application.dto.response.person.base import PersonView
from tracker.application.dto.response.person.change_username import ChangePersonNameResponse
from tracker.application.errors.auth import AccessDeniedError
from tracker.application.interfaces.interactor import Interactor
from tracker.application.interfaces.readers.person import IPersonReader
from tracker.application.interfaces.repositories.person import IPersonRepository
from tracker.application.interfaces.security.identity_provider import IIdentityProvider
from tracker.application.interfaces.transaction_manager import ITransactionManager
from tracker.domain.entities.person import Person
from tracker.domain.entities.person import PersonId
from tracker.domain.errors.base import AlreadyExistsError
from tracker.domain.errors.base import NotFoundError
from tracker.domain.values.person_name import PersonName


class ChangePersonName(Interactor[ChangePersonNameRequest, ChangePersonNameResponse]):
    def __init__(
        self,
        person_repository: IPersonRepository,
        person_reader: IPersonReader,
        transaction_manager: ITransactionManager,
        identity_provider: IIdentityProvider,
    ) -> None:
        self._person_repository: IPersonRepository = person_repository
        self._person_reader: IPersonReader = person_reader
        self._uow: ITransactionManager = transaction_manager
        self._idp: IIdentityProvider = identity_provider

    async def execute(self, request: ChangePersonNameRequest) -> ChangePersonNameResponse:
        current_person: Person = await self._idp.get_person()
        self._check_access(current_person, request.id)

        person: Person | None = await self._person_reader.get_by_id(request.id)
        if person is None:
            raise NotFoundError(f"User with id '{request.id}' not found")

        person.username = PersonName(value=request.data.username)

        await self._check_unique(person)
        await self._person_repository.update(person)
        await self._uow.commit()

        return ChangePersonNameResponse(person=PersonView.from_domain(person))

    async def _check_unique(self, person: Person) -> None:
        existing: Person | None = await self._person_reader.get_by_username(person.username)
        if existing is not None and existing.id != person.id:
            raise AlreadyExistsError(f"Person with username '{person.username.value}' already exists")

    @staticmethod
    def _check_access(current_person: Person, target_person_id: PersonId) -> None:
        if current_person.id != target_person_id:
            raise AccessDeniedError("You don't have permission to change another person's username")
