from pydantic import BaseModel
from pydantic import SecretStr
from sqlalchemy import URL


class DatabaseConfig(BaseModel):
    drivername: str
    name: str
    host: str
    port: int
    username: str
    password: SecretStr

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
