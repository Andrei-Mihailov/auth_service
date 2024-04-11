from http import HTTPStatus
from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from pydantic import BaseModel, TypeAdapter
from datetime import timedelta

from api.dependencies import UserParams, UserEditParams, AuthenticationParams, TokenParams
from api.v1.schemas.p_area import UserSchema, AuthenticationSchema, TokenSchema
from models.user import User
from models.auth import Authentication, Token


from models.value_objects import UserID
from services.user import UserService, get_current_user
router = APIRouter()


# /api/v1/p_area/user_registration
@router.post('/user_registration',
             response_model=UserSchema,
             status_code=status.HTTP_200_OK,
             summary="Регистрация пользователя",
             description="Регистрация пользователя по логину, имени и паролю",
             response_description="Ид, логин, имя, дата регистрации",
             tags=['Пользователи'])
async def user_registration(user_params: Annotated[UserParams, Depends()],
                            user_service: Annotated[UserService, Depends()]) -> User:
    return User


# /api/v1/p_area/change_user_info/{id_user}
@router.put('/change_user_info/{id_user}',
            response_model=UserSchema,
            status_code=status.HTTP_200_OK,
            summary="Редактирование данных пользователя",
            description="Редактирование логина, имени и пароля пользователя",
            response_description="Ид, логин, имя, дата регистрации",
            tags=['Пользователи'])
async def change_user_info(id_user: str,
                           user_params: Annotated[UserEditParams, Depends()],
                           user_service: UserService = Depends()) -> User:
    return User


# /api/v1/p_area/login
@router.post('/login',
             response_model=AuthenticationSchema,
             status_code=status.HTTP_200_OK,
             summary="Авторизация пользователя",
             description="Авторизцаия пользвателя по логину и паролю",
             response_description="Ид, логин, имя, дата регистрации",
             tags=['Пользователи'])
async def login(user_params: Annotated[AuthenticationParams, Depends()],
                user_service: UserService = Depends()) -> Authentication:
    return Authentication


# /api/v1/p_area/logout/{id_user}
@router.post('/logout/{id_user}',
             response_model=None,
             status_code=status.HTTP_200_OK,
             summary="Выход пользователя",
             description="Выход текущего авторизованного пользователя",
             tags=['Пользователи'])
async def logout(id_user: str,
                 token: TokenParams,
                 user_service: Annotated[UserService, Depends()]) -> None:
    return None


# /api/v1/p_area/refresh_token/{id_user}
@router.post('/refresh_token/{id_user}',
             response_model=TokenSchema,
             status_code=status.HTTP_200_OK,
             summary="Запрос refresh токена",
             description="Запрос refresh токена",
             response_description="Токены access и refresh",
             tags=['Пользователи'])
async def refresh_token(id_user: str, token: TokenParams) -> Token:
    # try:
    #     current_user: UserService = await get_current_user(token.access_token)
    #     access_token_expires = timedelta(minutes=UserService.ACCESS_TOKEN_EXPIRE_MINUTES)
    #     new_access_token = current_user.create_access_token(
    #         data={"sub": token.refresh_token},
    #         expires_delta=access_token_expires
    #     )

    #     # Возвращаем новый access token
    #     return {"access_token": new_access_token, "token_type": "bearer"}

    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Failed to refresh token"
    #     )
    return Token


# /api/v1/p_area/get_login_history/{id_user}
@router.get('/get_login_history/{id_user}',
            response_model=list[AuthenticationSchema],
            status_code=status.HTTP_200_OK,
            summary="История авторизаций",
            description="Запрос истории авторизаций пользователя",
            response_description="Ид, ид пользователя, юзер агент, дата аутентификации",
            tags=['Пользователи'])
async def get_login_history(id_user: str,
                            token: TokenParams,
                            user_service: Annotated[UserService, Depends()]) -> list[Authentication]:
    # try:
    #     current_user: UserService = await get_current_user(token.access_token)
    #     access_token_expires = timedelta(minutes=UserService.ACCESS_TOKEN_EXPIRE_MINUTES)
    #     new_access_token = current_user.create_access_token(
    #         data={"sub": token.refresh_token},
    #         expires_delta=access_token_expires
    #     )

    #     # Возвращаем новый access token
    #     return {"access_token": new_access_token, "token_type": "bearer"}

    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Failed to refresh token"
    #     )
    return list[Authentication]
