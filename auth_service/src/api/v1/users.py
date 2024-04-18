from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import TypeAdapter

from api.v1.schemas.auth import (
    AuthenticationSchema,
    TokenSchema,
    AuthenticationParams,
    TokenParams,
)
from api.v1.schemas.users import UserParams, UserEditParams, UserSchema
from services.user import UserService, get_user_service
from models.entity import User
from db.postgres_db import get_session, AsyncSession
router = APIRouter()


# /api/v1/users/login
@router.post(
    "/login",
    response_model=TokenSchema,
    status_code=status.HTTP_200_OK,
    summary="Авторизация пользователя",
    description="Авторизцаия пользвателя по логину и паролю",
    response_description="Access и Refresh токены",
    tags=["Пользователи"],
)
async def login(
    user_params: Annotated[AuthenticationParams, Depends()],
    user_service: UserService = Depends(get_user_service),
) -> TokenSchema:
    tokens_resp = await user_service.login(user_params.login,
                                           user_params.password)

    return TokenSchema(tokens_resp.access_token, tokens_resp.refresh_token)


# /api/v1/users/user_registration
@router.post(
    "/user_registration",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Регистрация пользователя",
    description="Регистрация пользователя по логину, имени и паролю",
    response_description="Результат регистрации: успешно или нет",
    tags=["Пользователи"],
)
async def user_registration(
    user_params: Annotated[UserParams, Depends()],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> bool:
    user_dto = jsonable_encoder(user_params)
    user = User(**user_dto)
    db.add(user)
    try:
        await db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='This login already exists')
    await db.refresh(user)
    return user

# /api/v1/users/change_user_info/{id_user}


@router.put(
    "/change_user_info/{id_user}",
    # response_model=UserSchema,
    response_model=bool,
    status_code=status.HTTP_200_OK,
    summary="Редактирование данных пользователя",
    description="Редактирование логина, имени и пароля пользователя",
    response_description="Ид, логин, имя, дата регистрации",
    tags=["Пользователи"],
)
async def change_user_info(
    id_user: str,
    user_params: Annotated[UserEditParams, Depends()],
    user_service: UserService = Depends(get_user_service),
) -> bool:
    return await user_service.change_user_info(
        id_user,
        user_params.firstname,
        user_params.lastname,
        user_params.login,
        user_params.password,
    )
    # return UserSchema


# /api/v1/users/logout
@router.post(
    "/logout",
    response_model=bool,
    status_code=status.HTTP_200_OK,
    summary="Выход пользователя",
    description="Выход текущего авторизованного пользователя",
    tags=["Пользователи"],
)
async def logout(token: TokenParams,
                 user_service: UserService = Depends(get_user_service)) -> None:
    return user_service.logout(token.access_token, token.refresh_token)


# /api/v1/users/refresh_token
@router.post(
    "/refresh_token",
    response_model=TokenSchema,
    status_code=status.HTTP_200_OK,
    summary="Запрос access токена",
    description="Запрос access токена",
    response_description="Access токен",
    tags=["Пользователи"],
)
async def refresh_token(
    token: TokenParams,
    user_service: UserService = Depends(get_user_service)
) -> TokenSchema:

    new_tokens = user_service.refresh_access_token(
        token.access_token, token.refresh_token
    )
    return TokenSchema(new_tokens.access_token, new_tokens.refresh_token)


# /api/v1/user/login_history/{id_user}
@router.get(
    "/login_history/{id_user}",
    response_model=list[AuthenticationSchema],
    status_code=status.HTTP_200_OK,
    summary="История авторизаций",
    description="Запрос истории авторизаций пользователя",
    response_description="Ид, ид пользователя, юзер агент, дата аутентификации",
    tags=["Пользователи"],
)
async def get_login_history(
    id_user: str, token: TokenParams,
        user_service: Annotated[UserService, Depends(get_user_service)]
) -> list[AuthenticationSchema]:
    auth_data = user_service.login_history(id_user, token.access_token)
    return TypeAdapter(list[AuthenticationSchema]).validate_python(auth_data)
