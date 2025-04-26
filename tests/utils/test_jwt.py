from types import SimpleNamespace
from app.utils import jwt_helpers

async def test_fetch_cognito_jwks(async_client, monkeypatch):
    dummy_response = {
        'authorization_endpoint': 'https://example.com/oauth2/authorize',
        'token_endpoint': 'https://example.com/oauth2/token',
        'jwks_uri': 'https://example.com/.well-known/jwks.json'
    }

    async def fake_get(url, *args, **kwargs):
        class DummyResponse:
            def raise_for_status(self): pass
            def json(self): return dummy_response
        return DummyResponse()

    monkeypatch.setattr(async_client, 'get', fake_get)

    request = SimpleNamespace()
    request.app =SimpleNamespace()
    request.app.state = SimpleNamespace()
    request.app.state.config = SimpleNamespace()
    request.app.state.config.AWS_COGNITO_METADATA_URL = 'https://example.com/metadata'

    metadata = await jwt_helpers.fetch_cognito_jwks(request)
    uri = metadata['jwks_uri']

    assert uri == dummy_response['jwks_uri']
