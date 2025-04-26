from app.utils import jwt_helpers

async def test_fetch_cognito_jwks(async_client, monkeypatch):
    dummy_response = {
        'keys': [
            {
                'kid': 'dummy-kid',
                'kty': 'RSA',
                'alg': 'RS256',
                'use': 'sig',
                'n': 'dummy-n',
                'e': 'AQAB',
            }
        ]
    }

    async def fake_get(url, *args, **kwargs):
        class DummyResponse:
            def raise_for_status(self): pass
            def json(self): return dummy_response
        return DummyResponse()

    monkeypatch.setattr(async_client, 'get', fake_get)

    jwks_uri = 'https://dummy-endpoint/.well-known/jwks.json'
    response = await jwt_helpers.fetch_cognito_jwks(jwks_uri)

    assert response == dummy_response
