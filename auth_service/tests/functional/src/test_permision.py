import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_role():
    response = await client.post("/api/v1/roles/create", json={"name": "Admin"})
    assert response.status_code == 200
    assert response.json()["name"] == "Admin"


@pytest.mark.asyncio
async def test_delete_role():
    response = await client.delete("/api/v1/roles/1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_role():
    response = await client.put("/api/v1/roles/change/1", json={"name": "Moderator"})
    assert response.status_code == 200
    assert response.json()["name"] == "Moderator"


@pytest.mark.asyncio
async def test_list_roles():
    response = await client.get("/api/v1/roles/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_add_permissions():
    response = await client.post("/api/v1/roles/add_permissions/1/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Permission"


@pytest.mark.asyncio
async def test_add_user_role():
    response = await client.post("/api/v1/roles/set/1/1")
    assert response.status_code == 200
    assert response.json()["name"] == "UserRole"


@pytest.mark.asyncio
async def test_delete_permissions():
    response = await client.delete("/api/v1/roles/1/1")
    assert response.status_code == 200