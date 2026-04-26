from tracker.application.dto.base import dto
from tracker.domain.entities.person import PersonId


@dto
class ChangePersonNameData:
    username: str


@dto
class ChangePersonNameRequest:
    id: PersonId
    data: ChangePersonNameData
