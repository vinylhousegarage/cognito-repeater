from pytest_httpx import HTTPXMock
from types import SimpleNamespace
from app.utils import jwt_helpers

async def test_fetch_cognito_jwks(httpx_mock: HTTPXMock):
    dummy_metadata = {'jwks_uri': 'https://example.com/jwks'}

    dummy_jwks = {
        'keys': [
            {'kty': 'RSA', 'kid': 'dummy-kid', 'n': 'dummy-n', 'e': 'dummy-e'}
        ]
    }

    httpx_mock.add_response(url=dummy_metadata['jwks_uri'], json=dummy_jwks)

    request = SimpleNamespace()
    request.app =SimpleNamespace()
    request.app.state = SimpleNamespace()
    request.app.state.metadata = SimpleNamespace()
    request.app.state.metadata = dummy_metadata

    result = await jwt_helpers.fetch_cognito_jwks(request)

    assert result == dummy_jwks
