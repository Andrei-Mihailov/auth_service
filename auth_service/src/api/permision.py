from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.v1.schemas.permission import PermissionParams
from services.permission import PermissionService

router = APIRouter()


@router.post(
    "/create_permission",
    response_model=bool,
    status_code=status.HTTP_200_OK,
    summary="Создание разрешения",
    description="Создание нового разрешения в системе",
    response_description="Результат операции: успешно или нет",
    tags=["Разрешения"],
)
async def create_permission(
    permission_params: Annotated[PermissionParams, Depends()],
    permission_service: PermissionService = Depends(),
) -> bool:
    return await permission_service.create_permission(permission_params.name)


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
    permission_params: Annotated[PermissionParams, Depends()],
    permission_service: PermissionService = Depends(),
) -> bool:
    return await permission_service.assign_permission_to_role(
        permission_params.role_name, permission_params.permission_name
    )


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
    permission_params: Annotated[PermissionParams, Depends()],
    permission_service: PermissionService = Depends(),
) -> bool:
    return await permission_service.remove_permission_from_role(
        permission_params.role_name, permission_params.permission_name
    )