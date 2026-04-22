from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi import status

from tracker.application.commands.person.create import CreatePerson
from tracker.application.dto.request.person.create import CreatePersonRequest
from tracker.application.dto.response.person.create import CreatePersonResponse

router = APIRouter(prefix="/person", tags=["Person"], route_class=DishkaRoute)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    request: CreatePersonRequest,
    interactor: FromDishka[CreatePerson],
) -> CreatePersonResponse:
    return await interactor.execute(request)
