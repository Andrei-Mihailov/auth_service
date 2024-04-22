from http import HTTPStatus
import uuid

import pytest

from ..settings import test_settings

SERVICE_URL = test_settings.SERVICE_URL

new_permission_name = str(uuid.uuid4())


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"name": new_permission_name}, {"status": HTTPStatus.OK}),
        ({"name": new_permission_name}, {"status": HTTPStatus.BAD_REQUEST}),
    ],
)
@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_create_permission(make_post_request, query_data, expected_answer):
    url = SERVICE_URL + "/api/v1/permissions/create"
    response = await make_post_request(url, query_data)
    status = response.status
    assert status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"name": new_permission_name}, {"status": HTTPStatus.OK}),
        ({"name": new_permission_name}, {"status": HTTPStatus.BAD_REQUEST}),
    ],
)
@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_delete_permission(make_delete_request, query_data, expected_answer):
    permission_id = str(uuid.uuid4())
    url = SERVICE_URL + f"/api/v1/permissions/{permission_id}"
    response = await make_delete_request(url, query_data)
    status = response.status
    assert status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"name": new_permission_name}, {"status": HTTPStatus.OK}),
        ({"name": new_permission_name}, {"status": HTTPStatus.BAD_REQUEST}),
    ],
)
@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_change_permission(make_put_request, query_data, expected_answer):
    permission_id = str(uuid.uuid4())
    url = SERVICE_URL + f"/api/v1/permissions/change/{permission_id}"
    response = await make_put_request(url, query_data)
    status = response.status
    assert status == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"name": new_permission_name}, {"status": HTTPStatus.OK}),
        ({"name": new_permission_name}, {"status": HTTPStatus.BAD_REQUEST}),
    ],
)
@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_list_permissions(make_get_request, query_data, expected_answer):
    url = SERVICE_URL + "/api/v1/permissions/list"
    response = await make_get_request(url)
    status = response.status
    assert status == expected_answer["status"]
