import base64
import pytest
from fastapi import HTTPException
from jose import jwt
from app.utils import jwt_helpers

async def test_fetch_cognito_jwks(dummy_jwks_request, fetch_cognito_jwks_httpx_mock):
    dummy_metadata = dummy_jwks_request.app.state.metadata

    result = await jwt_helpers.fetch_cognito_jwks(dummy_jwks_request)

    assert result['keys'] == dummy_metadata['keys']

def test_decode_access_token_for_kid(dummy_kid):
    dummy_token = jwt.encode(
        {'sub': 'user-id'},
        key='secret',
        algorithm='HS256',
        headers={'kid': dummy_kid},
    )

    result = jwt_helpers.decode_access_token_for_kid(access_token=dummy_token)

    assert result == dummy_kid

async def test_search_jwk_by_kid_found(dummy_kid, dummy_jwks_request, fetch_cognito_jwks_httpx_mock):
    dummy_token = jwt.encode(
        {'sub': 'user-id'},
        key='secret',
        algorithm='HS256',
        headers={'kid': dummy_kid},
    )

    result = await jwt_helpers.search_jwk_by_kid(dummy_token, dummy_jwks_request)

    assert result['kid'] == dummy_kid
    assert result['kty'] == 'RSA'

async def test_search_jwk_by_kid_not_found(dummy_jwks_request, fetch_cognito_jwks_httpx_mock):
    dummy_non_existent_kid = 'dummy-non-existent-kid'
    dummy_token = jwt.encode(
        {'sub': 'user-id'},
        key='secret',
        algorithm='HS256',
        headers={'kid': dummy_non_existent_kid},
    )

    with pytest.raises(HTTPException):
        await jwt_helpers.search_jwk_by_kid(dummy_token, dummy_jwks_request)

def test_decode_jwk_to_bytes():
    dummy_jwk = {
        'n': base64.urlsafe_b64encode(b'\x01\x02\x03').rstrip(b'=').decode('utf-8'),
        'e': base64.urlsafe_b64encode(b'\x01\x00\x01').rstrip(b'=').decode('utf-8'),
    }

    n_bytes, e_bytes = jwt_helpers.decode_jwk_to_bytes(dummy_jwk)

    assert n_bytes == b'\x01\x02\x03'
    assert e_bytes == b'\x01\x00\x01'

def test_decode_jwk_to_bytes_missing_n():
    dummy_jwk = {
        'e': base64.urlsafe_b64encode(b'\x01\x00\x01').rstrip(b'=').decode('utf-8'),
    }

    with pytest.raises(HTTPException):
        jwt_helpers.decode_jwk_to_bytes(dummy_jwk)

def test_decode_jwk_to_bytes_missing_e():
    dummy_jwk = {
        'n': base64.urlsafe_b64encode(b'\x01\x02\x03').rstrip(b'=').decode('utf-8'),
    }

    with pytest.raises(HTTPException):
        jwt_helpers.decode_jwk_to_bytes(dummy_jwk)

def test_convert_bytes_to_int():
    n_bytes = b'\x01\x02\x03'
    e_bytes = b'\x01\x00\x01'
    dummy_n = int.from_bytes(n_bytes, 'big')
    dummy_e = int.from_bytes(e_bytes, 'big')

    n_int, e_int = jwt_helpers.convert_bytes_to_int(n_bytes, e_bytes)

    assert n_int == dummy_n
    assert e_int == dummy_e

def test_generate_public_key(dummy_e_int, dummy_n_int, dummy_public_key):
    public_key = jwt_helpers.generate_public_key(dummy_e_int, dummy_n_int)
    assert public_key.public_numbers() == dummy_public_key.public_numbers()

def test_cache_public_key_by_kid(dummy_request, dummy_kid, dummy_public_key):
    jwt_helpers.cache_public_key_by_kid(dummy_request, dummy_kid, dummy_public_key)
    assert dummy_request.app.state.public_keys[dummy_kid] == dummy_public_key

def test_cache_public_key_by_kid_creates_keys_dict_when_missing(dummy_request, dummy_kid, dummy_public_key):
    if hasattr(dummy_request.app.state, 'public_keys'):
        delattr(dummy_request.app.state, 'public_keys')

    jwt_helpers.cache_public_key_by_kid(dummy_request, dummy_kid, dummy_public_key)

    assert dummy_request.app.state.public_keys[dummy_kid] == dummy_public_key

def test_cache_public_key_by_kid_overwrites_existing_key(dummy_request, dummy_kid, dummy_public_key, dummy_second_public_key):
    jwt_helpers.cache_public_key_by_kid(dummy_request, dummy_kid, dummy_public_key)
    jwt_helpers.cache_public_key_by_kid(dummy_request, dummy_kid, dummy_second_public_key)
    assert dummy_request.app.state.public_keys[dummy_kid] == dummy_second_public_key
