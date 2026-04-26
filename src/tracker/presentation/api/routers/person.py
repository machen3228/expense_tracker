from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from tracker.application.commands.person.change_username import ChangePersonName
from tracker.application.commands.person.create import CreatePerson
from tracker.application.dto.request.person.change_username import ChangePersonNameData
from tracker.application.dto.request.person.change_username import ChangePersonNameRequest
from tracker.application.dto.request.person.create import CreatePersonRequest
from tracker.application.dto.response.person.change_username import ChangePersonNameResponse
from tracker.application.dto.response.person.create import CreatePersonResponse
from tracker.domain.entities.person import PersonId
from tracker.presentation.api.dependencies import get_current_user_token

router = APIRouter(prefix="/person", tags=["Person"], route_class=DishkaRoute)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    request: CreatePersonRequest,
    interactor: FromDishka[CreatePerson],
) -> CreatePersonResponse:
    return await interactor.execute(request)


@router.patch("/{person_id}/username", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user_token)])
async def change_username(
    person_id: PersonId,
    data: ChangePersonNameData,
    interactor: FromDishka[ChangePersonName],
) -> ChangePersonNameResponse:
    return await interactor.execute(ChangePersonNameRequest(id=person_id, data=data))
