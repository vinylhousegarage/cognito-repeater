import pytest
from fastapi import HTTPException
from jose import jwt
from app.utils import jwt_helpers

async def test_fetch_cognito_jwks(dummy_jwks_request):
    dummy_metadata = dummy_jwks_request.app.state.metadata

    result = await jwt_helpers.fetch_cognito_jwks(dummy_jwks_request)

    assert result['keys'] == dummy_metadata['keys']

def test_decode_access_token_for_kid():
    dummy_kid = 'dummy-key-id'

    dummy_token = jwt.encode(
        {'sub': 'user-id'},
        key='secret',
        algorithm='HS256',
        headers={'kid': dummy_kid},
    )

    result = jwt_helpers.decode_access_token_for_kid(access_token=dummy_token)

    assert result == dummy_kid

async def test_search_jwk_by_kid_found(dummy_jwks_request):
    dummy_kid = 'kid-dummy'
    dummy_token = jwt.encode(
        {'sub': 'user-id'},
        key='secret',
        algorithm='HS256',
        headers={'kid': dummy_kid},
    )

    result = await jwt_helpers.search_jwk_by_kid(dummy_token, dummy_jwks_request)

    assert result['kid'] == dummy_kid
    assert result['kty'] == 'RSA'

async def test_search_jwk_by_kid_not_found(dummy_jwks_request):
    dummy_kid = 'kid-non-existent'
    dummy_token = jwt.encode(
        {'sub': 'user-id'},
        key='secret',
        algorithm='HS256',
        headers={'kid': dummy_kid},
    )

    with pytest.raises(HTTPException):
        await jwt_helpers.search_jwk_by_kid(dummy_token, dummy_jwks_request)
