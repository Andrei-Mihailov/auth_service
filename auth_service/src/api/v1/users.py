from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Request, Response
from pydantic import TypeAdapter

from api.v1.schemas.auth import (
    AuthenticationSchema,
    TokenSchema,
    AuthenticationParams,
    AuthenticationData,
    TokenParams,
)
from api.v1.schemas.users import UserParams, UserEditParams
from services.user import UserService, get_user_service
from services.auth import AuthService, get_auth_service

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
    request: Request,
    user_params: Annotated[AuthenticationParams, Depends()],
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenSchema:
    user_agent = request.headers.get("user-agent")
    tokens_resp, user = await user_service.login(
        user_params.login, user_params.password
    )
    user_agent_data = AuthenticationData(user_agent=user_agent, user_id=user.id)
    await auth_service.new_auth(user_agent_data)
    response = Response()
    response.set_cookie("access_token", tokens_resp.access_token)
    response.set_cookie("refresh_token", tokens_resp.refresh_token)
    return response


# /api/v1/users/user_registration
@router.post(
    "/user_registration",
    response_model=bool,
    status_code=status.HTTP_200_OK,
    summary="Регистрация пользователя",
    description="Регистрация пользователя по логину, имени и паролю",
    response_description="Результат регистрации: успешно или нет",
    tags=["Пользователи"],
)
async def user_registration(
    user_params: Annotated[UserParams, Depends()],
    user_service: UserService = Depends(get_user_service),
) -> bool:
    try:
        res = await user_service.create_user(user_params)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="This login already exists"
        )
    return res


# /api/v1/users/change_user_info
@router.put(
    "/change_user_info",
    # response_model=UserSchema,
    response_model=bool,
    status_code=status.HTTP_200_OK,
    summary="Редактирование данных пользователя",
    description="Редактирование логина, имени и пароля пользователя",
    response_description="Ид, логин, имя, дата регистрации",
    tags=["Пользователи"],
)
async def change_user_info(
    request: Request,
    user_params: Annotated[UserEditParams, Depends()],
    user_service: UserService = Depends(get_user_service),
) -> bool:
    tokens = TokenParams(
        access_token=request.cookies.get("access_token"),
        refresh_token=request.cookies.get("refresh_token"),
    )
    return await user_service.change_user_info(tokens.access_token, user_params)
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
async def logout(
    request: Request, user_service: UserService = Depends(get_user_service)
) -> None:
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
    request: Request, user_service: UserService = Depends(get_user_service)
) -> TokenSchema:
    tokens = TokenParams(
        access_token=request.cookies.get("access_token"),
        refresh_token=request.cookies.get("refresh_token"),
    )
    new_tokens = await user_service.refresh_access_token(
        tokens.access_token, tokens.refresh_token
    )
    response = Response()
    response.set_cookie("access_token", new_tokens.access_token)
    response.set_cookie("refresh_token", new_tokens.refresh_token)
    return response


# /api/v1/user/login_history


@router.get(
    "/login_history",
    response_model=list[AuthenticationSchema],
    status_code=status.HTTP_200_OK,
    summary="История авторизаций",
    description="Запрос истории авторизаций пользователя",
    response_description="Ид, ид пользователя, юзер агент, дата аутентификации",
    tags=["Пользователи"],
)
async def get_login_history(
    request: Request, auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> list[AuthenticationSchema]:
    tokens = TokenParams(
        access_token=request.cookies.get("access_token"),
        refresh_token=request.cookies.get("refresh_token"),
    )
    auth_data = await auth_service.login_history(tokens.access_token)
    return TypeAdapter(list[AuthenticationSchema]).validate_python(auth_data)
