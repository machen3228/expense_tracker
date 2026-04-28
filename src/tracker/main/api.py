from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from tracker.config.config import Config
from tracker.config.config import config
from tracker.main.di.container import create_container
from tracker.presentation.api.error_handler import app_error_handler
from tracker.presentation.api.routers.auth import router as auth_router
from tracker.presentation.api.routers.person import router as person_router

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from dishka import AsyncContainer


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()


def create_app(config: Config) -> FastAPI:
    app = FastAPI(
        title=config.api.title,
        version=config.api.version,
        docs_url=config.api.docs_url,
        redoc_url=config.api.redoc_url,
        openapi_url=config.api.openapi_url,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.api.cors.allow_origins,
        allow_credentials=config.api.cors.allow_credentials,
        allow_methods=config.api.cors.allow_methods,
        allow_headers=config.api.cors.allow_headers,
        max_age=config.api.cors.max_age,
    )

    container: AsyncContainer = create_container(config)
    setup_dishka(container, app)

    _include_routers(app)
    app.add_exception_handler(Exception, app_error_handler)

    return app


def _include_routers(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(person_router)


def main() -> None:
    app: FastAPI = create_app(config)

    uvicorn.run(
        app,
        host=config.api.host,
        port=config.api.port,
        reload=config.api.reload,
    )


if __name__ == "__main__":
    main()
