from typing import TYPE_CHECKING

from dishka import make_async_container

from tracker.config.database import DatabaseConfig
from tracker.main.di.providers.database import DatabaseProvider
from tracker.main.di.providers.interactors import InteractorsProvider
from tracker.main.di.providers.password_hasher import PasswordHasherProvider
from tracker.main.di.providers.readers import ReadersProvider
from tracker.main.di.providers.repositories import RepositoriesProvider

if TYPE_CHECKING:
    from dishka import AsyncContainer
    from dishka import Provider

    from tracker.config.config import Config


def create_container(config: Config) -> AsyncContainer:
    providers: list[Provider] = [
        DatabaseProvider(),
        InteractorsProvider(),
        PasswordHasherProvider(),
        ReadersProvider(),
        RepositoriesProvider(),
    ]

    context: dict[type, object] = {
        DatabaseConfig: config.database,
    }

    return make_async_container(*providers, context=context)
