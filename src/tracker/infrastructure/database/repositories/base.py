from abc import ABC
from abc import abstractmethod
from collections.abc import Hashable
from typing import TYPE_CHECKING

from tracker.domain.entities.base import Entity
from tracker.infrastructure.database.models.base import BaseORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SAAbstractRepository[EntityType: Entity[Hashable], ORMType: BaseORM](ABC):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    @abstractmethod
    def _to_orm(self, entity: EntityType) -> ORMType:
        raise NotImplementedError

    async def add(self, entity: EntityType) -> None:
        orm_obj: ORMType = self._to_orm(entity)
        self._session.add(orm_obj)

    async def update(self, entity: EntityType) -> None:
        orm_obj: ORMType = self._to_orm(entity)
        await self._session.merge(orm_obj)

    async def delete(self, entity: EntityType) -> None:
        orm_obj: ORMType = self._to_orm(entity)
        merged: ORMType = await self._session.merge(orm_obj)
        await self._session.delete(merged)
