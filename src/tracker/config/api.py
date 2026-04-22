from pydantic import BaseModel


class CORSConfig(BaseModel):
    allow_origins: list[str]
    allow_credentials: bool
    allow_methods: list[str]
    allow_headers: list[str]
    max_age: int = 600


class APIConfig(BaseModel):
    title: str
    version: str
    docs_url: str
    redoc_url: str
    openapi_url: str
    host: str
    port: int
    reload: bool

    cors: CORSConfig
