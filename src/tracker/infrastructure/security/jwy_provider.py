from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import Any

import jwt
from pydantic import TypeAdapter

from tracker.application.errors.auth import InvalidTokenError
from tracker.application.errors.auth import TokenExpiredError
from tracker.application.errors.base import OperationFailedError
from tracker.application.interfaces.security.jwt_provider import IJWTProvider
from tracker.application.interfaces.security.jwt_provider import TokenData
from tracker.application.interfaces.security.jwt_provider import TokenMeta
from tracker.application.interfaces.security.jwt_provider import TokenPayload
from tracker.application.interfaces.security.jwt_provider import TokenType
from tracker.infrastructure.database.errors.base import DataMapperError

_adapter: TypeAdapter[TokenData] = TypeAdapter(TokenData)


class PyJWTProvider(IJWTProvider):
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_ttl: int,
        refresh_ttl: int,
    ) -> None:
        self._secret_key: str = secret_key
        self._algorithm: str = algorithm
        self._ttl_map = {
            TokenType.ACCESS: access_ttl,
            TokenType.REFRESH: refresh_ttl,
        }

    def create_access_token(self, payload: TokenPayload) -> str:
        return self._create_token(payload, TokenType.ACCESS)

    def create_refresh_token(self, payload: TokenPayload) -> str:
        return self._create_token(payload, TokenType.REFRESH)

    def decode_token(self, token: str) -> TokenData:
        try:
            token_data: dict[str, Any] = jwt.decode(
                token,
                key=self._secret_key,
                algorithms=[self._algorithm],
            )
        except jwt.ExpiredSignatureError as e:
            raise TokenExpiredError("Token has expired") from e
        except jwt.InvalidTokenError as e:
            raise InvalidTokenError("Token is invalid") from e

        try:
            return _adapter.validate_python(token_data)
        except Exception as e:
            raise DataMapperError from e

    def _create_token(self, payload: TokenPayload, token_type: TokenType) -> str:
        now = datetime.now(UTC)
        ttl_minutes = self._ttl_map[token_type]
        iat = int(now.timestamp())
        exp = int((now + timedelta(minutes=ttl_minutes)).timestamp())

        token_data = TokenData(
            payload=payload,
            meta=TokenMeta(
                type=token_type,
                iat=iat,
                exp=exp,
            ),
        )

        try:
            data = _adapter.dump_python(token_data, mode="json")
        except Exception as e:
            raise DataMapperError from e

        try:
            return jwt.encode(
                data,
                key=self._secret_key,
                algorithm=self._algorithm,
            )
        except jwt.PyJWTError as e:
            raise OperationFailedError from e
