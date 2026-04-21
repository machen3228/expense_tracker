from collections.abc import AsyncIterator

from dishka import BaseScope
from dishka import Provider
from dishka import Scope
from dishka import provide
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from tracker.application.interfaces.transaction_manager import ITransactionManager
from tracker.config.database import DatabaseConfig
from tracker.infrastructure.database.transaction_manager import SATransactionManager


class DatabaseProvider(Provider):
    scope: BaseScope | None = Scope.APP

    @provide
    async def engine(self, config: DatabaseConfig) -> AsyncIterator[AsyncEngine]:
        engine: AsyncEngine = create_async_engine(config.url, echo=config.engine.echo)
        yield engine
        await engine.dispose()

    @provide
    def session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    @provide(scope=Scope.REQUEST)
    async def session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def transaction_manager(self, session: AsyncSession) -> ITransactionManager:
        return SATransactionManager(session)
