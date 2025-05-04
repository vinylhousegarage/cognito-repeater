from httpx import AsyncClient
from pytest_httpx import HTTPXMock

async def test_sub_returns_sub_when_userinfo_valid(app_client: AsyncClient, httpx_mock: HTTPXMock):
    metadata_url = 'https://example.com/metadata_url'
    userinfo_url = 'https://example.com/userinfo'

    app_client.app.state.config = type('Config', (), {})()
    app_client.app.state.config.AWS_COGNITO_METADATA_URL = metadata_url

    httpx_mock.add_response(
        url=metadata_url,
        json={'userinfo': userinfo_url}
    )
    httpx_mock.add_response(
        url=userinfo_url,
        json={'sub': 'user-1234'},
        status_code=200
    )

    response = await app_client.get(
        '/sub',
        headers={'Authorization': 'Bearer dummy-access-token'}
    )

    assert response.status_code == 200
    assert response.json() == {'sub': 'user-1234'}
