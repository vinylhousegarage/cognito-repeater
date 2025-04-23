import app.utils.auth_helpers as auth_helpers
from types import SimpleNamespace
from app.utils.auth_helpers import cache_cognito_metadata

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

    metadata = await cache_cognito_metadata(app)
    assert metadata == dummy_metadata
    assert app.state.metadata == dummy_metadata

    second_metadata = await cache_cognito_metadata(app)
    assert second_metadata is metadata
