from fastapi import APIRouter, Depends
from dependencies import get_user_service
from services import UserService
from schema import UserLoginSchema, UserCreateSchema
from typing import Annotated

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserLoginSchema)
async def create_user(body: UserCreateSchema,
                      user_service: Annotated[UserService, Depends(get_user_service)]):
    return await user_service.create_user(body.username, body.password)
