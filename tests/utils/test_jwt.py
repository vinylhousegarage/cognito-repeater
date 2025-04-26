import jwt
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

async def test_decode_access_token_for_kid():
    dummy_kid = 'dummy-key-id'

    dummy_token = jwt.encode(
        payload={'sub': 'user-id'},
        key='secret',
        algorithm='HS256',
        headers={'kid': dummy_kid},
    )

    result = await jwt_helpers.decode_access_token_for_kid(dummy_token)

    assert result == dummy_kid
