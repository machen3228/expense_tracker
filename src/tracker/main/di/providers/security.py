from dishka import BaseScope
from dishka import Provider
from dishka import Scope
from dishka import provide
from fastapi import Request

from tracker.application.interfaces.readers.person import IPersonReader
from tracker.application.interfaces.security.identity_provider import IIdentityProvider
from tracker.application.interfaces.security.jwt_provider import IJWTProvider
from tracker.application.interfaces.security.password_hasher import IPasswordHasher
from tracker.config.jwt import JWTConfig
from tracker.infrastructure.security.identity_provider import IdentityProvider
from tracker.infrastructure.security.jwy_provider import PyJWTProvider
from tracker.infrastructure.security.password_hasher import BcryptPasswordHasher


class SecurityProvider(Provider):
    scope: BaseScope | None = Scope.APP

    @provide
    def password_hasher(self) -> IPasswordHasher:
        return BcryptPasswordHasher()

    @provide
    def jwt_provider(self, config: JWTConfig) -> IJWTProvider:
        return PyJWTProvider(
            secret_key=config.secret_key.get_secret_value(),
            algorithm=config.algorithm,
            access_ttl=config.access_ttl_minutes,
            refresh_ttl=config.refresh_ttl_minutes,
        )

    @provide(scope=Scope.REQUEST)
    def identity_provider(
        self,
        request: Request,
        jwt_provider: IJWTProvider,
        person_reader: IPersonReader,
    ) -> IIdentityProvider:
        token: str = request.headers.get("Authorization", "").removeprefix("Bearer ")
        return IdentityProvider(
            token=token,
            jwt_provider=jwt_provider,
            person_reader=person_reader,
        )
