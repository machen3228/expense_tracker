from pydantic import BaseModel

from tracker.application.dto.response.person.base import PersonView


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"  # noqa: S105
    person: PersonView
