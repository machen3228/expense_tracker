from typing import TYPE_CHECKING

from dishka import Provider
from dishka import Scope
from dishka import provide

from tracker.infrastructure.password_hasher import BcryptPasswordHasher

if TYPE_CHECKING:
    from dishka import BaseScope

    from tracker.application.interfaces.security.password_hasher import IPasswordHasher


class PasswordHasherProvider(Provider):
    scope: BaseScope | None = Scope.APP

    @provide
    def password_hasher(self) -> IPasswordHasher:
        return BcryptPasswordHasher()
