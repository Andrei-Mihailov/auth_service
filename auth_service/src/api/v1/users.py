from http import HTTPStatus
from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from pydantic import BaseModel, TypeAdapter

from api.v1.schemas.auth import (AuthenticationSchema
                                 ,TokenSchema
                                 ,AuthenticationParams
                                 ,TokenParams)
from api.v1.schemas.users import (UserSchema
                                 ,UserParams
                                 ,UserEditParams)
from services.user import UserService

router = APIRouter()


# /api/v1/users/login
@router.post('/login',
             response_model=TokenSchema,
             status_code=status.HTTP_200_OK,
             summary="Авторизация пользователя",
             description="Авторизцаия пользвателя по логину и паролю",
             response_description="Access и Refresh токены",
             tags=['Пользователи'])
async def login(user_params: Annotated[AuthenticationParams, Depends()],
                user_service: UserService = Depends()) -> TokenSchema:
    tokens_resp = await user_service.login(user_params.login, user_params.password)
   
    return TokenSchema(tokens_resp.access_token, tokens_resp.refresh_token)


# /api/v1/users/user_registration
@router.post('/user_registration',
             #response_model=UserSchema,
             status_code=status.HTTP_200_OK,
             summary="Регистрация пользователя",
             description="Регистрация пользователя по логину, имени и паролю",
             response_description="Результат регистрации: успешно или нет",
             tags=['Пользователи'])
async def user_registration(user_params: Annotated[UserParams, Depends()],
                            user_service: Annotated[UserService, Depends()]) -> bool:
    
    return await user_service.create_user(user_params.firstname,
                                  user_params.lastname,
                                  user_params.login,
                                  user_params.password)
    #return UserSchema

# /api/v1/users/change_user_info/{id_user}
@router.put('/change_user_info/{id_user}',
            #response_model=UserSchema,
            status_code=status.HTTP_200_OK,
            summary="Редактирование данных пользователя",
            description="Редактирование логина, имени и пароля пользователя",
            response_description="Ид, логин, имя, дата регистрации",
            tags=['Пользователи'])
async def change_user_info(id_user: str,
                           user_params: Annotated[UserEditParams, Depends()],
                           user_service: UserService = Depends()) -> bool:
    return await user_service.change_user_info(id_user, 
                                  user_params.firstname,
                                  user_params.lastname,
                                  user_params.login,
                                  user_params.password)
    #return UserSchema


# /api/v1/users/logout/{id_user}
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
async def refresh_token(id_user: str, token: TokenParams) -> TokenSchema:
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
    return TokenSchema


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
                            user_service: Annotated[UserService, Depends()]) -> list[AuthenticationSchema]:
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
    return list[AuthenticationSchema]
