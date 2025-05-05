from fastapi import Request
from httpx import AsyncClient
from pytest_httpx import HTTPXMock
from types import SimpleNamespace
from app.utils import auth_helpers

async def test_fetch_cognito_metadata(httpx_mock: HTTPXMock, async_client: AsyncClient) -> None:
    dummy_metadata = {
        'authorization_endpoint': 'https://example.com/oauth2/authorize',
        'token_endpoint': 'https://example.com/oauth2/token'
    }

    dummy_url = 'https://example.com/.well-known/openid-configuration'

    httpx_mock.add_response(url=dummy_url, json=dummy_metadata)

    result = await auth_helpers.fetch_cognito_metadata(async_client, dummy_url)

    assert result == dummy_metadata

async def test_cache_cognito_metadata(request: Request, monkeypatch):
    dummy_metadata = {
        'authorization_endpoint': 'https://example.com/login',
        'token_endpoint': 'https://example.com/token'
    }

    async def fake_fetch_cognito_metadata(client, metadata_url) -> None:
        return dummy_metadata

    monkeypatch.setattr(auth_helpers, 'fetch_cognito_metadata', fake_fetch_cognito_metadata)

    request = SimpleNamespace()
    request.app =SimpleNamespace()
    request.app.state = SimpleNamespace()
    request.app.state.config = SimpleNamespace()
    request.app.state.config.AWS_COGNITO_METADATA_URL = 'https://fake-url'

    metadata = await auth_helpers.cache_cognito_metadata(request)
    assert metadata == dummy_metadata
    assert request.app.state.metadata == dummy_metadata

    second_metadata = await auth_helpers.cache_cognito_metadata(request)
    assert second_metadata is metadata
