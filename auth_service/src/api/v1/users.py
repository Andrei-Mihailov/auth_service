from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Request, Response


from api.v1.schemas.auth import (
    AuthenticationSchema,
    TokenSchema,
    AuthenticationParams,
    AuthenticationData
)
from api.v1.schemas.users import UserParams, UserSchema, UserEditParams
from api.v1.schemas.roles import PermissionsParams
from services.user import UserService, get_user_service
from services.auth import AuthService, get_auth_service
from .service import get_tokens_from_cookie, PaginationParams

router = APIRouter()


# /api/v1/users/login
@router.post(
    "/login",
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
) -> None:
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
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Регистрация пользователя",
    description="Регистрация пользователя по логину, имени и паролю",
    response_description="Результат регистрации: успешно или нет",
    tags=["Пользователи"],
)
async def user_registration(
    user_params: Annotated[UserParams, Depends()],
    user_service: UserService = Depends(get_user_service),
) -> UserSchema:
    user = await user_service.create_user(user_params)
    if user is not None:
        return UserSchema(
            uuid=user.id,
            login=user.login,
            first_name=user.first_name,
            last_name=user.last_name,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="This login already exists"
        )


# /api/v1/users/change_user_info
@router.put(
    "/change_user_info",
    response_model=UserSchema,
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
) -> UserSchema:

    tokens = get_tokens_from_cookie(request)
    change_user = await user_service.change_user_info(tokens.access_token, user_params)
    return UserSchema(
        uuid=change_user.id,
        login=change_user.login,
        first_name=change_user.first_name,
        last_name=change_user.last_name,
    )


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
) -> bool:
    tokens = get_tokens_from_cookie(request)
    return await user_service.logout(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )


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
    tokens = get_tokens_from_cookie(request)

    new_tokens = await user_service.refresh_access_token(
        tokens.access_token, tokens.refresh_token
    )
    response = Response()
    response.set_cookie("access_token", new_tokens.access_token)
    response.set_cookie("refresh_token", new_tokens.refresh_token)
    return response


# /api/v1/users/login_history
@router.post(
    "/login_history",
    response_model=list[AuthenticationSchema],
    status_code=status.HTTP_200_OK,
    summary="История авторизаций",
    description="Запрос истории авторизаций пользователя",
    response_description="Ид, ид пользователя, юзер агент, дата аутентификации",
    tags=["Пользователи"],
)
async def get_login_history(
    request: Request, auth_service: Annotated[AuthService, Depends(get_auth_service)],
    pagination_params: Annotated[PaginationParams, Depends()]
) -> list[AuthenticationSchema]:

    tokens = get_tokens_from_cookie(request)
    auth_data = await auth_service.login_history(tokens.access_token, pagination_params.page_number, pagination_params.page_size)

    list_auth_scheme = []
    for item in auth_data:
        auth_scheme = AuthenticationSchema(
            uuid=item.id,
            user_id=item.user_id,
            user_agent=item.user_agent,
            date_auth=item.date_auth,
        )
        list_auth_scheme.append(auth_scheme)
    return list_auth_scheme


# /api/v1/users/check_permission
@router.post(
    "/check_permission",
    response_model=bool,
    status_code=status.HTTP_200_OK,
    summary="Проверка разрешений пользователя",
    description="Проверка разрешения опредленных действий пользователя",
    response_description="Результат проверки: успешно или нет",
    tags=["Пользователи"],
)
async def check_permission(
    request: Request,
    permission_params: Annotated[PermissionsParams, Depends()],
    user_service: UserService = Depends(get_user_service),
) -> bool:
    tokens = get_tokens_from_cookie(request)
    return await user_service.check_permissions(
        tokens.access_token, permission_params.name
    )
