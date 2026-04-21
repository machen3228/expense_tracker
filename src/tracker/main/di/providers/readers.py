from typing import TYPE_CHECKING

from dishka import Provider
from dishka import Scope
from dishka import provide

from tracker.infrastructure.database.readers.person import SAPersonReader

if TYPE_CHECKING:
    from dishka import BaseScope
    from sqlalchemy.ext.asyncio import AsyncSession

    from tracker.application.interfaces.readers.person import IPersonReader


class ReadersProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    @provide
    def person_reader(self, session: AsyncSession) -> IPersonReader:
        return SAPersonReader(session)
