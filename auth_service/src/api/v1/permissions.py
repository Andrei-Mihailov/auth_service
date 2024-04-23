from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Request

from api.v1.schemas.roles import (
    PermissionsParams,
    PermissionsSchema,
    RolePermissionsParams,
)
from services.permission import PermissionService, get_permission_service
from service import get_tokens_from_cookie


router = APIRouter()


# /api/v1/permissions/create_permission
@router.post(
    "/create_permission",
    response_model=PermissionsSchema,
    status_code=status.HTTP_200_OK,
    summary="Создание разрешения",
    description="Создание нового разрешения в системе",
    response_description="Результат операции: успешно или нет",
    tags=["Разрешения"],
)
async def create_permission(
    request: Request,
    permission_params: Annotated[PermissionsParams, Depends()],
    permission_service: PermissionService = Depends(get_permission_service),
) -> PermissionsSchema:
    token = get_tokens_from_cookie(request)
    perm = await permission_service.create_permission(permission_params, token.access_token)
    if perm is not None:
        return PermissionsSchema(uuid=perm.id, name=perm.name)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This permission already exists",
        )


# /api/v1/permissions/assign_permission_to_role
@router.post(
    "/assign_permission_to_role",
    response_model=bool,
    status_code=status.HTTP_200_OK,
    summary="Назначение разрешения роли",
    description="Назначение разрешения определенной роли в системе",
    response_description="Результат операции: успешно или нет",
    tags=["Разрешения"],
)
async def assign_permission_to_role(
    request: Request,
    permission_params: Annotated[RolePermissionsParams, Depends()],
    permission_service: PermissionService = Depends(get_permission_service),
) -> bool:
    token = get_tokens_from_cookie(request)
    result = await permission_service.assign_permission_to_role(
        permission_params, token.access_token
    )
    if result:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# /api/v1/permissions/remove_permission_from_role
@router.post(
    "/remove_permission_from_role",
    response_model=bool,
    status_code=status.HTTP_200_OK,
    summary="Удаление разрешения из роли",
    description="Удаление разрешения из определенной роли в системе",
    response_description="Результат операции: успешно или нет",
    tags=["Разрешения"],
)
async def remove_permission_from_role(
    request: Request,
    permission_params: Annotated[RolePermissionsParams, Depends()],
    permission_service: PermissionService = Depends(get_permission_service),
) -> bool:
    token = get_tokens_from_cookie(request)
    result = await permission_service.remove_permission_from_role(
        permission_params, token.access_token
    )
    if result:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
