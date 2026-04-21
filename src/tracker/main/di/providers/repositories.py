from typing import TYPE_CHECKING

from dishka import Provider
from dishka import Scope
from dishka import provide

from tracker.infrastructure.database.repositories.person import SAPersonRepository

if TYPE_CHECKING:
    from dishka import BaseScope
    from sqlalchemy.ext.asyncio import AsyncSession

    from tracker.application.interfaces.repositories.person import IPersonRepository


class RepositoriesProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    @provide
    def person_repository(self, session: AsyncSession) -> IPersonRepository:
        return SAPersonRepository(session)
