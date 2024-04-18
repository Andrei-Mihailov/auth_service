from typing import Annotated
from fastapi import APIRouter, Depends, status


from api.v1.schemas.roles import (RolesSchema, PermissionsSchema, UserRoleSchema,
                                  RoleParams, RoleEditParams, PermissionsParams)
from models.roles import Role, Permission, User_Role


from services.role import RoleService, get_role_service
from services.permission import PermissionService, get_permission_service

router = APIRouter()


# /api/v1/roles/create
@router.post(
    "/create",
    response_model=RolesSchema,
    status_code=status.HTTP_200_OK,
    summary="Создание роли",
    description="Создание новой роли",
    response_description="Ид, тип, разрешения",
    tags=["Роли"],
)
async def create(
    role_params: Annotated[RoleParams, Depends()],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> Role:
    return Role


# /api/v1/roles/{id_role}
@router.delete(
    "/{id_role}",
    status_code=status.HTTP_200_OK,
    summary="Удаление роли",
    description="Удаление существующей роли",
    tags=["Роли"],
)
async def delete(id_role: str,
                 role_service: Annotated[RoleService, Depends(get_role_service)]) -> None:
    return None


# /api/v1/roles/create/{id_role}
@router.put(
    "/change/{id_role}",
    # response_model=RolesSchema,
    status_code=status.HTTP_200_OK,
    summary="Редактирование роли",
    description="Редактирование существующей роли",
    response_description="Ид, тип, разрешения",
    tags=["Роли"],
)
async def change(
    id_role: str,
    role_params: Annotated[RoleEditParams, Depends()],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> Role:
    return Role


# /api/v1/roles/list
@router.get(
    "/list",
    # response_model=list[RolesSchema],
    status_code=status.HTTP_200_OK,
    summary="Список ролей",
    description="Список существующих ролей",
    response_description="Ид, тип, разрешения",
    tags=["Роли"],
)
async def list_roles(
        role_service: Annotated[RoleService, Depends(get_role_service)]
) -> list[Role]:
    return list[Role]


# /api/v1/roles/add_permissions/{id_role}/{id_permission}
@router.post(
    "/add_permissions/{id_role}/{id_permission}",
    # response_model=PermissionsSchema,
    status_code=status.HTTP_200_OK,
    summary="Добавление разрешений",
    description="Добавление разрешений для роли по их ИД",
    response_description="Ид, название",
    tags=["Роли"],
)
async def add_permissions(
    id_role: str,
    id_permission: str,
    prmission_params: Annotated[PermissionsParams, Depends()],
    permission_service: Annotated[PermissionService, Depends(get_permission_service)],
) -> Permission:
    return Permission


# /api/v1/roles/set/{id_role}/{user_id}
@router.post(
    "/set/{user_id}/{id_role}",
    # response_model=UserRoleSchema,
    status_code=status.HTTP_200_OK,
    summary="Назначение ролей",
    description="Назначение выбранной роли конкретному пользователю",
    response_description="Ид роли, Ид пользователя",
    tags=["Роли"],
)
async def add_user_role(user_id: str, id_role: str) -> User_Role:
    return Permission


# /api/v1/roles/{id_role}/{id_permission}
@router.delete(
    "/{id_role}/{id_permission}",
    status_code=status.HTTP_200_OK,
    summary="Удаление разрешения у роли",
    description="Удаление существующего разрешения у роли по их ИД",
    tags=["Роли"],
)
async def delete_permissions(
    id_role: str,
    id_permission: str,
    permission_service: Annotated[PermissionService, Depends(get_permission_service)],
) -> None:
    return None
