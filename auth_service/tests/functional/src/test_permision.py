import pytest
from httpx import AsyncClient

from ..settings import test_settings


SERVICE_URL = test_settings.SERVISE_URL


@pytest.mark.asyncio
async def test_create_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post("/api/v1/roles/create", json={"type": "Admin"})
        assert response.status_code == 200
        assert response.json()["type"] == "Admin"


@pytest.mark.asyncio
async def test_delete_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.delete("/api/v1/roles/1")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.put(
            "/api/v1/roles/change/1", json={"type": "Moderator"}
        )
        assert response.status_code == 200
        assert response.json()["type"] == "Moderator"


@pytest.mark.asyncio
async def test_list_roles():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.get("/api/v1/roles/list")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_add_permissions():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post("/api/v1/roles/add_permissions/1/1")
        assert response.status_code == 200
        assert response.json()["type"] == "Permission"


@pytest.mark.asyncio
async def test_add_user_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post("/api/v1/roles/set/1/1")
        assert response.status_code == 200
        assert response.json()["type"] == "UserRole"


@pytest.mark.asyncio
async def test_delete_permissions():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.delete("/api/v1/roles/1/1")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_role_duplicate_name():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post("/api/v1/roles/create", json={"type": "Admin"})
        assert response.status_code == 409  # Conflict


@pytest.mark.asyncio
async def test_create_role_missing_name():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post("/api/v1/roles/create", json={})
        assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.asyncio
async def test_delete_role_nonexistent():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.delete("/api/v1/roles/999")
        assert response.status_code == 404  # Not Found


@pytest.mark.asyncio
async def test_change_role_nonexistent():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.put(
            "/api/v1/roles/change/999", json={"type": "Moderator"}
        )
        assert response.status_code == 404  # Not Found


@pytest.mark.asyncio
async def test_change_role_missing_name():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.put("/api/v1/roles/change/1", json={})
        assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.asyncio
async def test_change_role_invalid_name_type():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.put("/api/v1/roles/change/1", json={"type": 123})
        assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.asyncio
async def test_list_roles_empty():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.get("/api/v1/roles/list")
        assert response.status_code == 200
        assert response.json() == []


@pytest.mark.asyncio
async def test_add_permissions_nonexistent_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post("/api/v1/roles/add_permissions/999/1")
        assert response.status_code == 404  # Not Found


@pytest.mark.asyncio
async def test_add_permissions_nonexistent_permission():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post("/api/v1/roles/add_permissions/1/999")
        assert response.status_code == 404  # Not Found


@pytest.mark.asyncio
async def test_add_user_role_nonexistent_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post("/api/v1/roles/set/999/1")
        assert response.status_code == 404  # Not Found


@pytest.mark.asyncio
async def test_add_user_role_nonexistent_user():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.post("/api/v1/roles/set/1/999")
        assert response.status_code == 404  # Not Found


@pytest.mark.asyncio
async def test_delete_permissions_nonexistent_role():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.delete("/api/v1/roles/999/1")
        assert response.status_code == 404  # Not Found


@pytest.mark.asyncio
async def test_delete_permissions_nonexistent_permission():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        response = await client.delete("/api/v1/roles/1/999")
        assert response.status_code == 404  # Not Found
