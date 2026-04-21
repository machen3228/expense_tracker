from dishka import BaseScope
from dishka import Provider
from dishka import Scope
from dishka import provide

from tracker.application.interfaces.security.password_hasher import IPasswordHasher
from tracker.infrastructure.password_hasher import BcryptPasswordHasher


class PasswordHasherProvider(Provider):
    scope: BaseScope | None = Scope.APP

    @provide
    def password_hasher(self) -> IPasswordHasher:
        return BcryptPasswordHasher()
