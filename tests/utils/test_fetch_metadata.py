from httpx import AsyncClient
from pytest_httpx import HTTPXMock
from app.utils.auth_helpers import fetch_cognito_metadata

async def test_fetch_cognito_metadata(httpx_mock: HTTPXMock, async_client: AsyncClient) -> None:
    dummy_metadata = {
        'authorization_endpoint': 'https://example.com/oauth2/authorize',
        'token_endpoint': 'https://example.com/oauth2/token'
    }

    dummy_url = 'https://example.com/.well-known/openid-configuration'

    httpx_mock.add_response(url=dummy_url, json=dummy_metadata)

    result = await fetch_cognito_metadata(async_client, dummy_url)

    assert result == dummy_metadata
