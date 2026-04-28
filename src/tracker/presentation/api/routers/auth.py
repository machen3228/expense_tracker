from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi import Form
from fastapi import status

from tracker.application.commands.auth.login import LoginPerson
from tracker.application.commands.auth.refresh_token import RefreshToken
from tracker.application.dto.request.auth.login import LoginRequest
from tracker.application.dto.request.auth.refresh_token import RefreshTokenRequest
from tracker.application.dto.response.auth.login import LoginResponse
from tracker.application.dto.response.auth.refresh_token import RefreshTokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    request: Annotated[LoginRequest, Form()],
    interactor: FromDishka[LoginPerson],
) -> LoginResponse:
    return await interactor.execute(request)


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(
    request: Annotated[RefreshTokenRequest, Form()],
    interactor: FromDishka[RefreshToken],
) -> RefreshTokenResponse:
    return await interactor.execute(request)
