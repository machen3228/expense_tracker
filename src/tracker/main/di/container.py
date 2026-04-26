from typing import TYPE_CHECKING

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from tracker.config.database import DatabaseConfig
from tracker.config.jwt import JWTConfig
from tracker.main.di.providers.database import DatabaseProvider
from tracker.main.di.providers.interactors import InteractorsProvider
from tracker.main.di.providers.password_hasher import SecurityProvider
from tracker.main.di.providers.readers import ReadersProvider
from tracker.main.di.providers.repositories import RepositoriesProvider

if TYPE_CHECKING:
    from dishka import AsyncContainer
    from dishka import Provider

    from tracker.config.config import Config


def create_container(config: Config) -> AsyncContainer:
    providers: list[Provider] = [
        FastapiProvider(),
        DatabaseProvider(),
        InteractorsProvider(),
        ReadersProvider(),
        SecurityProvider(),
        RepositoriesProvider(),
    ]

    context: dict[type, object] = {
        DatabaseConfig: config.database,
        JWTConfig: config.jwt,
    }

    return make_async_container(*providers, context=context)
