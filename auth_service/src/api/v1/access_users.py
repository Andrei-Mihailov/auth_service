from http import HTTPStatus
from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from pydantic import BaseModel, TypeAdapter
from datetime import timedelta

from api.dependencies import PermissionsParams
from api.v1.schemas.roles import PermissionsSchema
from models.models import Permission


from models.value_objects import UserID
from services.permission import PermissionService

router = APIRouter()


# /api/v1/access_users/create
@router.post(
    "/create",
    response_model=PermissionsSchema,
    status_code=status.HTTP_200_OK,
    summary="Создание разрешений",
    description="Создание новых разрешений для пользователей",
    response_description="Ид, название",
    tags=["Разрешения"],
)
async def create(
    permission_params: Annotated[PermissionsParams, Depends()],
    permission_service: Annotated[PermissionService, Depends()],
) -> Permission:
    return Permission


# /api/v1/access_users/{id_permission}
@router.delete(
    "/{id_permission}",
    status_code=status.HTTP_200_OK,
    summary="Удаление разрешения",
    description="Удаление существующего разрешения",
    tags=["Разрешения"],
)
async def delete_permissions(
    id_permission: str, permission_service: Annotated[PermissionService, Depends()]
) -> None:
    return None


# /api/v1/access_users/check/{id_user}
@router.get(
    "/check/{id_user}",
    response_model=list[PermissionsSchema],
    status_code=status.HTTP_200_OK,
    summary="Проверка разрешений роли",
    description="Проверка разрешений данной роли",
    response_description="Ид, название",
    tags=["Разрешения"],
)
async def check(
    id_permission: str, permission_service: Annotated[PermissionService, Depends()]
) -> list[Permission]:
    return list[Permission]
