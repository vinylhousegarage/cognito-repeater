import pytest
from httpx import AsyncClient
from pytest_httpx import HTTPXMock

@pytest.mark.asyncio
async def test_sub_returns_sub_when_userinfo_valid(app_client: AsyncClient, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url='https://example.com/userinfo',
        json={'sub': 'user-1234'},
        status_code=200
    )

    response = await app_client.get(
        '/sub',
        headers={'Authorization': 'Bearer dummy-access-token'}
    )

    assert response.status_code == 200
    assert response.json() == {'sub': 'user-1234'}
