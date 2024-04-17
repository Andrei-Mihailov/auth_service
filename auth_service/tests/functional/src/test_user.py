from http import HTTPStatus

import pytest

@pytest.mark.asyncio
async def test_login_success(client_fixture, user_fixture):
    response = await client_fixture.post('/login', json={
        'username': user_fixture.username,
        'password': 'testpassword'
    })

    assert response.status_code == HTTPStatus.OK
    assert 'detail' in response.json()
    assert response.json()['detail'] == 'Successfully login'

