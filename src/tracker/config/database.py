from pydantic import BaseModel
from pydantic import Field
from pydantic import SecretStr
from sqlalchemy import URL


class EngineConfig(BaseModel):
    echo: bool


class DatabaseConfig(BaseModel):
    drivername: str
    name: str
    host: str
    port: int
    username: str
    password: SecretStr

    engine: EngineConfig = Field(default_factory=EngineConfig)

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.drivername,
            database=self.name,
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password.get_secret_value(),
        )
