from http import HTTPStatus
import uuid

import pytest

from ..settings import test_settings

SERVICE_URL = test_settings.SERVISE_URL

new_role_name = str(uuid.uuid4())
new_permission_name = str(uuid.uuid4())


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"name": new_role_name},
            {"status": HTTPStatus.OK}
        ),
        (
            {"name": new_role_name},
            {"status": HTTPStatus.BAD_REQUEST}
        )
    ]
)
@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_create_role(make_post_request, query_data, expected_answer):
    url = SERVICE_URL + "/api/v1/roles/create"
    response = await make_post_request(url, query_data)
    status = response.status
    assert status == expected_answer['status']


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"name": new_role_name},
            {"status": HTTPStatus.OK}
        ),
        (
            {"name": new_role_name},
            {"status": HTTPStatus.BAD_REQUEST}
        )
    ]
)
@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_delete_role(make_delete_request, query_data, expected_answer):
    role_id = str(uuid.uuid4())
    url = SERVICE_URL + f"/api/v1/roles/{role_id}"
    response = await make_delete_request(url, query_data)
    status = response.status
    assert status == expected_answer['status']


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"name": new_role_name},
            {"status": HTTPStatus.OK}
        ),
        (
            {"name": new_role_name},
            {"status": HTTPStatus.BAD_REQUEST}
        )
    ]
)
@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_change_role(make_put_request, query_data, expected_answer):
    role_id = str(uuid.uuid4())
    url = SERVICE_URL + f"/api/v1/roles/change/{role_id}"
    response = await make_put_request(url, query_data)
    status = response.status
    assert status == expected_answer['status']


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"name": new_role_name},
            {"status": HTTPStatus.OK}
        ),
        (
            {"name": new_role_name},
            {"status": HTTPStatus.BAD_REQUEST}
        )
    ]
)
@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_list_roles(make_get_request, query_data, expected_answer):
    url = SERVICE_URL + "/api/v1/roles/list"
    response = await make_get_request(url)
    status = response.status
    assert status == expected_answer['status']


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"role_id": str(uuid.uuid4()), "permission_id": str(uuid.uuid4())},
            {"status": HTTPStatus.OK}
        ),
        (
            {"role_id": str(uuid.uuid4()), "permission_id": str(uuid.uuid4())},
            {"status": HTTPStatus.BAD_REQUEST}
        ),
        (
            {"role_id": "", "permission_id": ""},
            {"status": HTTPStatus.BAD_REQUEST}
        )
    ]
)
@pytest.mark.order(5)
@pytest.mark.asyncio
async def test_add_permissions(make_post_request, query_data, expected_answer):
    url = SERVICE_URL + "/api/v1/roles/add_permissions/{role_id}/{permission_id}"
    response = await make_post_request(url, query_data)
    status = response.status
    assert status == expected_answer['status']