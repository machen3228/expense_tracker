from pydantic import BaseModel
from pydantic import SecretStr


class JWTConfig(BaseModel):
    algorithm: str
    secret_key: SecretStr
    access_ttl_minutes: int
    refresh_ttl_minutes: int
