from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from tracker.application.errors.base import OperationFailedError
from tracker.domain.entities.base import Entity
from tracker.infrastructure.database.models.base import BaseORM

if TYPE_CHECKING:
    from sqlalchemy import ColumnElement
    from sqlalchemy import Result
    from sqlalchemy import Select
    from sqlalchemy.ext.asyncio import AsyncSession


class SAAbstractReader[EntityType: Entity[Any], ORMType: BaseORM](ABC):
    _model: ClassVar[type[BaseORM]]

    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    @abstractmethod
    def _to_domain(self, orm_obj: ORMType) -> EntityType:
        raise NotImplementedError

    async def _execute[T](self, query: Select[tuple[T]]) -> Result[tuple[T]]:
        try:
            return await self._session.execute(query)
        except SQLAlchemyError as e:
            raise OperationFailedError from e

    async def _get(
        self,
        *where_clause: ColumnElement[bool],
    ) -> EntityType | None:
        query: Select[tuple[ORMType]] = select(self._model)

        if where_clause:
            query = query.where(*where_clause)

        result = await self._execute(query)
        orm_obj: ORMType | None = result.scalars().first()

        if orm_obj is None:
            return None

        return self._to_domain(orm_obj)
