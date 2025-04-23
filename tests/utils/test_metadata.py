import app.utils.auth_helpers as auth_helpers
from httpx import AsyncClient
from pytest_httpx import HTTPXMock
from types import SimpleNamespace

async def test_fetch_cognito_metadata(httpx_mock: HTTPXMock, async_client: AsyncClient) -> None:
    dummy_metadata = {
        'authorization_endpoint': 'https://example.com/oauth2/authorize',
        'token_endpoint': 'https://example.com/oauth2/token'
    }

    dummy_url = 'https://example.com/.well-known/openid-configuration'

    httpx_mock.add_response(url=dummy_url, json=dummy_metadata)

    result = await auth_helpers.fetch_cognito_metadata(async_client, dummy_url)

    assert result == dummy_metadata

async def test_cache_cognito_metadata(monkeypatch):
    dummy_metadata = {
        'authorization_endpoint': 'https://example.com/login',
        'token_endpoint': 'https://example.com/token'
    }

    async def fake_fetch_cognito_metadata(_, __) -> None:
        return dummy_metadata

    monkeypatch.setattr(auth_helpers, 'fetch_cognito_metadata', fake_fetch_cognito_metadata)

    app = SimpleNamespace()
    app.state = SimpleNamespace()
    app.state.config = SimpleNamespace()
    app.state.config.AWS_COGNITO_METADATA_URL = 'https://fake-url'

    metadata = await auth_helpers.cache_cognito_metadata(app)
    assert metadata == dummy_metadata
    assert app.state.metadata == dummy_metadata

    second_metadata = await auth_helpers.cache_cognito_metadata(app)
    assert second_metadata is metadata
