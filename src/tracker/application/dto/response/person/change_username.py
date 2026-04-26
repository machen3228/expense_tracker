from tracker.application.dto.base import dto
from tracker.application.dto.response.person.base import PersonView


@dto
class ChangePersonNameResponse:
    user: PersonView
