import pytest
import uuid
from httpx import AsyncClient
from http import HTTPStatus

from ..settings import test_settings


SERVICE_URL = test_settings.SERVISE_URL

login = str(uuid.uuid4())
user_pass = "test"


@pytest.mark.order("first")
@pytest.mark.asyncio
async def test_list_roles_empty():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.get("/api/v1/roles/list")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_create_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        pytest.role_type = str(uuid.uuid4())
        response = await client.post(
            "/api/v1/roles/create", params={"type": pytest.role_type}
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()["type"] == pytest.role_type
        pytest.role_id = response.json()["uuid"]


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_create_role_duplicate_name():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post(
            "/api/v1/roles/create", params={"type": pytest.role_type}
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_change_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        pytest.role_type = str(uuid.uuid4())
        response = await client.put(
            f"/api/v1/roles/change/{pytest.role_id}", params={"type": pytest.role_type}
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()["type"] == pytest.role_type


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_list_roles():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.get("/api/v1/roles/list")
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(), list)


@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_create_permission():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        pytest.permissions_name = str(uuid.uuid4())
        response = await client.post(
            "/api/v1/permissions/create_permission",
            params={"name": pytest.permissions_name},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()["name"] == pytest.permissions_name
        pytest.permissions_id = response.json()["uuid"]


@pytest.mark.order(5)
@pytest.mark.asyncio
async def test_add_user_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post(
            "/api/v1/users/user_registration",
            params={"login": login, "password": user_pass},
        )
        pytest.user_id = response.json()["uuid"]
        response_set_role = await client.post(
            f"/api/v1/roles/set/{pytest.user_id}/{pytest.role_id}"
        )
        assert response_set_role.status_code == HTTPStatus.OK
        assert response_set_role.json()["id_role"] == pytest.role_id


@pytest.mark.asyncio
async def test_create_role_missing_name():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post("/api/v1/roles/create", params={})
        assert (
            response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        )  # Unprocessable Entity


@pytest.mark.asyncio
async def test_change_role_nonexistent():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.put(
            "/api/v1/roles/change/999", params={"type": "Moderator"}
        )
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_change_role_missing_name():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.put(f"/api/v1/roles/change/{pytest.role_id}", params={})
        assert (
            response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        )  # Unprocessable Entity


@pytest.mark.asyncio
async def test_add_permissions_nonexistent_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post(
            f"/api/v1/permissions/assign_permission_to_role",
            params={
                "role_id": str(uuid.uuid4()),
                "permissions_id": pytest.permissions_id,
            },
        )
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_add_permissions_nonexistent_permission():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post(
            f"/api/v1/permissions/assign_permission_to_role",
            params={"role_id": pytest.role_id, "permissions_id": str(uuid.uuid4())},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_add_permissions():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post(
            f"/api/v1/permissions/assign_permission_to_role",
            params={"role_id": pytest.role_id, "permissions_id": pytest.permissions_id},
        )
        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_add_user_role_nonexistent_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post(
            f"/api/v1/roles/set/{pytest.user_id}/{str(uuid.uuid4())}"
        )
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_add_user_role_nonexistent_user():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post(
            f"/api/v1/roles/set/{str(uuid.uuid4())}/{pytest.role_id}"
        )
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_permissions_nonexistent_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post(
            f"/api/v1/permissions/remove_permission_from_role",
            params={
                "role_id": str(uuid.uuid4()),
                "permissions_id": pytest.permissions_id,
            },
        )
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_permissions_nonexistent_permission():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post(
            f"/api/v1/permissions/remove_permission_from_role",
            params={"role_id": pytest.role_id, "permissions_id": str(uuid.uuid4())},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.order("fourth_to_last")
@pytest.mark.asyncio
async def test_delete_permissions():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post(
            f"/api/v1/permissions/remove_permission_from_role",
            params={"role_id": pytest.role_id, "permissions_id": pytest.permissions_id},
        )
        assert response.status_code == HTTPStatus.OK


@pytest.mark.order("third_to_last")
@pytest.mark.asyncio
async def test_delete_role_from_user():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        # назначенная пользователю роль
        response = await client.post(f"/api/v1/roles/delete/{pytest.user_id}")
        assert response.status_code == HTTPStatus.OK


@pytest.mark.order("second_to_last")
@pytest.mark.asyncio
async def test_delete_role_nonexistent():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.delete(f"/api/v1/roles/{str(uuid.uuid4())}")
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.order("last")
@pytest.mark.asyncio
async def test_delete_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.delete(f"/api/v1/roles/{pytest.role_id}")
        assert response.status_code == HTTPStatus.OK
