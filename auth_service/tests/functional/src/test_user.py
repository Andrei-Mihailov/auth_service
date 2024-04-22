from http import HTTPStatus
import uuid

import pytest

from ..settings import test_settings

SERVICE_URL = test_settings.SERVISE_URL

new_login = str(uuid.uuid4())
new_user_pass = "test"


def pytest_namespace():
    return {"access_token": None, "refresh_token": None, "new_user_id": None}


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"login": new_login, "password": new_user_pass}, {"status": HTTPStatus.OK}),
        ({"login": new_login, "password": "test"}, {"status": HTTPStatus.BAD_REQUEST}),
    ],
)
@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_registration_user(make_post_request, query_data, expected_answer):
    url = SERVICE_URL + "/api/v1/users/user_registration"
    query_data = {"login": query_data["login"], "password": query_data["password"]}

    response = await make_post_request(url, query_data)

    status = response.status
    assert status == expected_answer["status"]
    if status == HTTPStatus.OK:
        body = await response.json()
        pytest.new_user_id = body["uuid"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"login": new_login, "password": "testtest"},
            {"status": HTTPStatus.FORBIDDEN},
        ),
        ({"login": new_login, "password": new_user_pass}, {"status": HTTPStatus.OK}),
        (
            {"login": str(uuid.uuid4()), "password": "user"},
            {"status": HTTPStatus.NOT_FOUND},
        ),
    ],
)
@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_login_user(make_post_request, query_data, expected_answer):
    url = SERVICE_URL + "/api/v1/users/login"
    query_data = {"login": query_data["login"], "password": query_data["password"]}

    response = await make_post_request(url, query_data)

    status = response.status
    assert status == expected_answer["status"]

    if expected_answer["status"] == HTTPStatus.OK:
        access_token = response.cookies.get("access_token")
        refresh_token = response.cookies.get("refresh_token")

        pytest.access_token = access_token
        pytest.refresh_token = refresh_token

        assert access_token is not None
        assert refresh_token is not None

    if expected_answer["status"] == HTTPStatus.NOT_FOUND:
        assert response.cookies.get("access_token") is None
        assert response.cookies.get("refresh_token") is None


@pytest.mark.parametrize(
    "query_data",
    [
        (
            {
                "first_name": "ivan",
                "last_name": "petrov",
                "login": str(uuid.uuid4()),
                "password": "user55",
            }
        ),
    ],
)
@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_change_user(make_put_request, query_data):
    url = SERVICE_URL + "/api/v1/users/change_user_info"
    query_data = {"login": query_data["login"], "password": query_data["password"]}

    response = await make_put_request(url, query_data)
    assert response.status == HTTPStatus.NOT_FOUND

    cookies = {
        "access_token": pytest.access_token,
        "refresh_token": pytest.refresh_token,
    }
    response = await make_put_request(url, query_data, cookies)

    assert response.status == HTTPStatus.OK


@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_refresh_token(make_post_request):
    url = SERVICE_URL + "/api/v1/users/refresh_token"
    # проверяем запрос без куки
    response = await make_post_request(url)
    assert response.status == HTTPStatus.NOT_FOUND
    # проверяем с куками автризованного пользователя
    cookies = {
        "access_token": pytest.access_token,
        "refresh_token": pytest.refresh_token,
    }
    response = await make_post_request(url, cookie=cookies)
    access_token = response.cookies.get("access_token")
    refresh_token = response.cookies.get("refresh_token")
    pytest.access_token = access_token
    pytest.refresh_token = refresh_token
    assert access_token is not None
    assert refresh_token is not None
    assert response.status == HTTPStatus.OK
    # проверяем со старыми токенами
    response = await make_post_request(url, cookie=cookies)
    assert response.status == HTTPStatus.FORBIDDEN


@pytest.mark.order(5)
@pytest.mark.asyncio
async def test_login_history(make_post_request):
    url = SERVICE_URL + "/api/v1/users/login_history"
    # проверяем запрос без куки
    response = await make_post_request(url)
    assert response.status == HTTPStatus.NOT_FOUND
    # проверяем с куками автризованного пользователя
    cookies = {
        "access_token": pytest.access_token,
        "refresh_token": pytest.refresh_token,
    }
    response = await make_post_request(url, cookie=cookies)
    body = await response.json()

    assert response.status == HTTPStatus.OK
    assert len(body) == 1


@pytest.mark.order(6)
@pytest.mark.asyncio
async def test_logout(make_post_request):
    url = SERVICE_URL + "/api/v1/users/check_permission"
    # проверяем запрос без куки
    response = await make_post_request(url)
    assert response.status == HTTPStatus.NOT_FOUND
    # проверяем с куками автризованного пользователя
    cookies = {
        "access_token": pytest.access_token,
        "refresh_token": pytest.refresh_token,
    }
    # проверяем новое разрешение
    permission_name = str(uuid.uuid4())
    query_data = {"name": permission_name}
    response = await make_post_request(url, query_data, cookie=cookies)
    body = await response.json()
    assert body == "false"

    # создаем новое разрешение
    query_data = {"type": str(uuid.uuid4())}
    url_role = SERVICE_URL + "/api/v1/roles/create"
    response_role = await make_post_request(url_role, query_data, cookie=cookies)
    url_permission = SERVICE_URL + "/api/v1/permissions/create_permission"
    query_data = {"name": permission_name}
    response_permission = await make_post_request(
        url_permission, query_data, cookie=cookies
    )
    query_data = {
        "role_id": response_role["uuid"],
        "permissions_id": response_permission["uuid"],
    }
    url_role_permission = SERVICE_URL + "/api/v1/permissions/assign_permission_to_role"
    response_role_permission = await make_post_request(
        url_role_permission, query_data, cookie=cookies
    )
    url = (
        SERVICE_URL + f"/api/v1/roles/set/{pytest.new_user_id}/{response_role['uuid']}"
    )
    response = await make_post_request(url_role_permission, query_data, cookie=cookies)

    # проверяем только что выданное разрешение
    query_data = {"name": permission_name}
    response = await make_post_request(url, query_data, cookie=cookies)
    body = await response.json()
    assert body == "true"


@pytest.mark.order(7)
@pytest.mark.asyncio
async def test_logout(make_post_request):
    url = SERVICE_URL + "/api/v1/users/logout"
    # проверяем запрос без куки
    response = await make_post_request(url)
    assert response.status == HTTPStatus.NOT_FOUND
    # проверяем с куками автризованного пользователя
    cookies = {
        "access_token": pytest.access_token,
        "refresh_token": pytest.refresh_token,
    }
    response = await make_post_request(url, cookie=cookies)
    assert response.status == HTTPStatus.OK

    url = SERVICE_URL + f"/api/v1/users/login_history"
    response = await make_post_request(url, cookie=cookies)
    assert response.status == HTTPStatus.FORBIDDEN
