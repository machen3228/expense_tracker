from typing import TYPE_CHECKING

from tracker.application.dto.base import dto

if TYPE_CHECKING:
    from tracker.application.dto.response.person.base import PersonView


@dto
class CreatePersonResponse:
    person: PersonView
