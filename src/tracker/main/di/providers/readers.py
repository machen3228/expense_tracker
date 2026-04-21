from dishka import BaseScope
from dishka import Provider
from dishka import Scope
from dishka import provide
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.application.interfaces.readers.person import IPersonReader
from tracker.infrastructure.database.readers.person import SAPersonReader


class ReadersProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    @provide
    def person_reader(self, session: AsyncSession) -> IPersonReader:
        return SAPersonReader(session)
