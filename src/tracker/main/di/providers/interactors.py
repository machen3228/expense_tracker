from dishka import BaseScope
from dishka import Provider
from dishka import Scope
from dishka import provide

from tracker.application.commands.person.change_username import ChangePersonName
from tracker.application.commands.person.create import CreatePerson
from tracker.application.interfaces.readers.person import IPersonReader
from tracker.application.interfaces.repositories.person import IPersonRepository
from tracker.application.interfaces.security.identity_provider import IIdentityProvider
from tracker.application.interfaces.security.password_hasher import IPasswordHasher
from tracker.application.interfaces.transaction_manager import ITransactionManager


class InteractorsProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    @provide
    def create_person(
        self,
        person_repository: IPersonRepository,
        person_reader: IPersonReader,
        password_hasher: IPasswordHasher,
        transaction_manager: ITransactionManager,
    ) -> CreatePerson:
        return CreatePerson(
            person_repository,
            person_reader,
            password_hasher,
            transaction_manager,
        )

    @provide
    def change_username(
        self,
        person_repository: IPersonRepository,
        person_reader: IPersonReader,
        transaction_manager: ITransactionManager,
        identity_provider: IIdentityProvider,
    ) -> ChangePersonName:
        return ChangePersonName(
            person_repository,
            person_reader,
            transaction_manager,
            identity_provider,
        )
