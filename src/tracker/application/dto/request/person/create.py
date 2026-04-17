from tracker.application.dto.base import dto


@dto
class CreatePersonRequest:
    username: str
    password: str
