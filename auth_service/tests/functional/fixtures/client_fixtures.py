import pytest_asyncio
import sys
from os import path
from httpx import AsyncClient

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from settings import test_settings


SERVICE_URL = test_settings.SERVISE_URL


@pytest_asyncio.fixture(name='client_fixture')
async def client_fixture():
    async with AsyncClient(base_url=SERVICE_URL) as client:
        yield client


@pytest_asyncio.fixture(name='user_fixture')
def user_fixture():
    class User:
        def __init__(self, username, password):
            self.username = username
            self.password = password

    test_user = User(username="test", password="test")

    return test_user


@pytest_asyncio.fixture(name='superuser_fixture')
def superuser_fixture():
    class User:
        def __init__(self, username, password):
            self.username = username
            self.password = password

    test_user = User(username=test_settings.SU_login,
                     password=test_settings.SU_password)

    return test_user


@pytest_asyncio.fixture(name='authenticated_client')
async def authenticated_client(client_fixture, user_fixture):
    login_data = {"login": user_fixture.username, "password": user_fixture.password}
    response = await client_fixture.post("/api/v1/users/login", params=login_data)
    assert response.status_code == 200
    cookies = response.cookies
    client_fixture.cookies = cookies
    yield client_fixture


@pytest_asyncio.fixture(name='superuser_authenticated_client')
async def superuser_authenticated_client(client_fixture, superuser_fixture):
    login_data = {"login": superuser_fixture.username, "password": superuser_fixture.password}
    response = await client_fixture.post("/api/v1/users/login", params=login_data)
    assert response.status_code == 200
    cookies = response.cookies
    client_fixture.supercookies = cookies
    yield client_fixture


@pytest_asyncio.fixture(name='client_factory')
def client_factory(client_fixture, user_fixture, superuser_fixture):
    async def inner(user):
        if user == "user":
            login_data = {
                "login": user_fixture.username,
                "password": user_fixture.password
            }
        elif user == "superuser":
            login_data = {
                "login": superuser_fixture.username,
                "password": superuser_fixture.password,
            }
        else:
            raise ValueError("Invalid user type")

        response = await client_fixture.post(
            "/api/v1/users/login",
            params=login_data
        )
        assert response.status_code == 200
        cookies = response.cookies
        client_fixture.cookies = cookies
        yield client_fixture
    return inner
