from typing import TYPE_CHECKING

import bcrypt

from tracker.application.interfaces.security.password_hasher import IPasswordHasher

if TYPE_CHECKING:
    from tracker.domain.values.password import Password


class BcryptPasswordHasher(IPasswordHasher):
    def hash_password(self, password: Password) -> bytes:
        salt: bytes = bcrypt.gensalt()
        return bcrypt.hashpw(password.value.encode(), salt)

    def verify_password(self, raw: str, hashed: bytes) -> bool:
        if not raw or not hashed:
            return False
        try:
            return bcrypt.checkpw(raw.encode(), hashed)
        except (ValueError, TypeError):  # fmt: skip
            return False
