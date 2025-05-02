import base64
import pytest
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError, JWSSignatureError

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

def test_verify_access_token(dummy_access_token_factory, dummy_claims_factory, dummy_leeway, dummy_payload, dummy_public_key_for_verify, dummy_request_for_verify):
    dummy_claims = dummy_claims_factory(dummy_payload)
    dummy_access_token = dummy_access_token_factory(dummy_payload)
    result = jwt_helpers.verify_access_token(dummy_request_for_verify, dummy_access_token, dummy_public_key_for_verify, dummy_leeway)
    assert result == dummy_claims

@pytest.mark.parametrize('mocked_exception, expected_detail', [
    (ExpiredSignatureError('Signature has expired'), 'Signature has expired'),
    (JWSSignatureError('Signature verification failed'), 'Signature verification failed'),
    (JWTClaimsError('Invalid claim: aud'), 'Invalid claim: aud'),
    (JWTError('Invalid audience'), 'Invalid audience'),
])
def test_verify_access_token_exceptions(mocked_exception, expected_detail, monkeypatch, dummy_access_token_factory, dummy_payload, dummy_request_for_verify, dummy_public_key_for_verify):
    dummy_access_token = dummy_access_token_factory(dummy_payload)

    def fake_decode(*args, **kwargs):
        raise mocked_exception

    monkeypatch.setattr('app.utils.jwt_helpers.jwt.decode', fake_decode)

    with pytest.raises(HTTPException) as exc_info:
        jwt_helpers.verify_access_token(dummy_request_for_verify, dummy_access_token, dummy_public_key_for_verify)

    assert exc_info.value.status_code == 401
    assert expected_detail in exc_info.value.detail['error']

def test_verify_access_token_expired(dummy_payload, dummy_access_token_factory, dummy_request_for_verify, dummy_public_key_for_verify):
    expired_payload = dummy_payload.copy()
    expired_payload['exp'] = datetime.now(timezone.utc) - timedelta(minutes=6) # Original token valid for 5 minutes; exp set 6 minutes ago
    dummy_access_token = dummy_access_token_factory(expired_payload)

    with pytest.raises(HTTPException) as exc:
        jwt_helpers.verify_access_token(dummy_request_for_verify, dummy_access_token, dummy_public_key_for_verify)

    assert exc.value.status_code == 401
    assert exc.value.detail['error'] == 'Signature has expired.'

def test_verify_access_token_signature(dummy_access_token_factory, dummy_payload, dummy_request_for_verify, dummy_second_public_key_for_verify):
    dummy_access_token = dummy_access_token_factory(dummy_payload)

    with pytest.raises(HTTPException) as exc:
        jwt_helpers.verify_access_token(dummy_request_for_verify, dummy_access_token, dummy_second_public_key_for_verify)

    assert exc.value.status_code == 401
    assert exc.value.detail['error'] == 'Signature verification failed.'

@pytest.mark.parametrize('broken_payload, expected_error', [
    ({'iss': 'wrong-audience'}, 'Invalid issuer'),
    ({'aud': 'wrong-audience'}, 'Invalid audience'),
    ({'iss': None}, 'Invalid issuer'),
])
def test_verify_access_token_claims_errors(broken_payload, expected_error, dummy_access_token_factory, dummy_request_for_verify, dummy_payload, dummy_public_key_for_verify):
    payload = dummy_payload.copy()
    payload.update(broken_payload)

    for key, value in broken_payload.items():
        if value is None:
            del payload[key]

    dummy_access_token = dummy_access_token_factory(payload)

    with pytest.raises(HTTPException) as exc:
        jwt_helpers.verify_access_token(dummy_request_for_verify, dummy_access_token, dummy_public_key_for_verify)

    assert exc.value.status_code == 401
    assert exc.value.detail['error'] == expected_error

@pytest.mark.parametrize('missing_claim, expected_error', [
    ('sub', 'Missing sub claim'),
    ('aud', 'Missing aud claim'),
    ('exp', 'Missing exp claim'),
])
def test_verify_access_token_missing_required_claims(missing_claim, expected_error, dummy_payload, dummy_access_token_factory, dummy_request_for_verify, dummy_public_key_for_verify):
    payload = dummy_payload.copy()
    del payload[missing_claim]
    dummy_access_token = dummy_access_token_factory(payload)

    with pytest.raises(HTTPException) as exc:
        jwt_helpers.verify_access_token(dummy_request_for_verify, dummy_access_token, dummy_public_key_for_verify)

    assert exc.value.status_code == 401
    assert exc.value.detail['error'] == expected_error

def test_verify_access_token_fails_without_public_key(dummy_request_for_verify, dummy_access_token_factory, dummy_payload):
    public_key = None # simulate missing public_key
    dummy_access_token = dummy_access_token_factory(dummy_payload)

    with pytest.raises(HTTPException) as exc:
        jwt_helpers.verify_access_token(dummy_request_for_verify, dummy_access_token, public_key)

    assert exc.value.status_code == 401
    assert exc.value.detail['error'] == 'Public key not found'

@pytest.mark.parametrize('invalid_token', [
    '',   # empty string
    None, # None value
])
def test_verify_access_token_missing_token(invalid_token, dummy_request_for_verify, dummy_public_key_for_verify):
    with pytest.raises(HTTPException) as exc:
        jwt_helpers.verify_access_token(dummy_request_for_verify, invalid_token, dummy_public_key_for_verify)

    assert exc.value.status_code == 401
    assert exc.value.detail['error'] == 'Missing token'

@pytest.mark.parametrize('invalid_token', [
    'abc.def.ghi.jkl',  # simulate a 4-part token (too many parts)
    'abc.def.@@@',  # invalid base64 format
])
def test_verify_access_token_invalid_format(invalid_token, dummy_request_for_verify, dummy_public_key_for_verify):
    with pytest.raises(HTTPException) as exc:
        jwt_helpers.verify_access_token(dummy_request_for_verify, invalid_token, dummy_public_key_for_verify)
    assert exc.value.status_code == 401
    assert 'Invalid header string' in exc.value.detail['error']

def test_verify_access_token_with_two_part_token(dummy_request_for_verify, dummy_public_key_for_verify):
    invalid_token = 'abc.def'  # 2-part token (should be 3)
    with pytest.raises(HTTPException) as exc:
        jwt_helpers.verify_access_token(dummy_request_for_verify, invalid_token, dummy_public_key_for_verify)

    assert exc.value.status_code == 401
    assert 'Not enough segments' in exc.value.detail['error']
