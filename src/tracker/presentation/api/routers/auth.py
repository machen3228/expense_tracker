from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi import Form
from fastapi import status

from tracker.application.commands.auth.login import LoginPerson
from tracker.application.dto.request.auth.login import LoginRequest
from tracker.application.dto.response.auth.login import LoginResponse

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    request: Annotated[LoginRequest, Form()],
    interactor: FromDishka[LoginPerson],
) -> LoginResponse:
    return await interactor.execute(request)
