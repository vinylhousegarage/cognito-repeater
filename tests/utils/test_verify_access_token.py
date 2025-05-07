import pytest
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError, JWSSignatureError
from app.utils import jwt_helpers

def test_verify_access_token(dummy_access_token, dummy_payload_factory, dummy_leeway, dummy_claims, dummy_public_key_for_verify, dummy_request_for_verify):
    dummy_payload = dummy_payload_factory(dummy_claims)
    result = jwt_helpers.verify_access_token(dummy_request_for_verify, dummy_access_token, dummy_public_key_for_verify, dummy_leeway)
    assert result == dummy_payload

@pytest.mark.parametrize('mocked_exception, expected_detail', [
    (ExpiredSignatureError('Signature has expired'), 'Signature has expired'),
    (JWSSignatureError('Signature verification failed'), 'Signature verification failed'),
    (JWTClaimsError('Invalid claim: aud'), 'Invalid claim: aud'),
    (JWTError('Invalid audience'), 'Invalid audience'),
])
def test_verify_access_token_exceptions(mocked_exception, expected_detail, monkeypatch, dummy_access_token, dummy_request_for_verify, dummy_public_key_for_verify):
    def fake_decode(*args, **kwargs):
        raise mocked_exception

    monkeypatch.setattr('app.utils.jwt_helpers.jwt.decode', fake_decode)

    with pytest.raises(HTTPException) as exc_info:
        jwt_helpers.verify_access_token(dummy_request_for_verify, dummy_access_token, dummy_public_key_for_verify)

    assert exc_info.value.status_code == 401
    assert expected_detail in exc_info.value.detail['error']

def test_verify_access_token_expired(dummy_claims, dummy_access_token_factory, dummy_request_for_verify, dummy_public_key_for_verify):
    expired_payload = dummy_claims.copy()
    expired_payload['exp'] = datetime.now(timezone.utc) - timedelta(minutes=6) # Original token valid for 5 minutes; exp set 6 minutes ago
    dummy_access_token = dummy_access_token_factory(expired_payload)

    with pytest.raises(HTTPException) as exc:
        jwt_helpers.verify_access_token(dummy_request_for_verify, dummy_access_token, dummy_public_key_for_verify)

    assert exc.value.status_code == 401
    assert exc.value.detail['error'] == 'Signature has expired.'

def test_verify_access_token_signature(dummy_access_token, dummy_request_for_verify, dummy_second_public_key_for_verify):
    with pytest.raises(HTTPException) as exc:
        jwt_helpers.verify_access_token(dummy_request_for_verify, dummy_access_token, dummy_second_public_key_for_verify)

    assert exc.value.status_code == 401
    assert exc.value.detail['error'] == 'Signature verification failed.'

@pytest.mark.parametrize('broken_payload, expected_error', [
    ({'iss': 'wrong-audience'}, 'Invalid issuer'),
    ({'aud': 'wrong-audience'}, 'Invalid audience'),
    ({'iss': None}, 'Invalid issuer'),
])
def test_verify_access_token_claims_errors(broken_payload, expected_error, dummy_access_token_factory, dummy_request_for_verify, dummy_claims, dummy_public_key_for_verify):
    payload = dummy_claims.copy()
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
    ('client_id', 'Missing client_id claim'),
    ('exp', 'Missing exp claim'),
])
def test_verify_access_token_missing_required_claims(missing_claim, expected_error, dummy_claims, dummy_access_token_factory, dummy_request_for_verify, dummy_public_key_for_verify):
    payload = dummy_claims.copy()
    del payload[missing_claim]
    dummy_access_token = dummy_access_token_factory(payload)

    with pytest.raises(HTTPException) as exc:
        jwt_helpers.verify_access_token(dummy_request_for_verify, dummy_access_token, dummy_public_key_for_verify)

    assert exc.value.status_code == 401
    assert exc.value.detail['error'] == expected_error

def test_verify_access_token_fails_without_public_key(dummy_access_token, dummy_request_for_verify):
    public_key = None # simulate missing public_key

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

@pytest.mark.parametrize('invalid_sub', [None, '', 123, {}, []])
def test_extract_sub_raises_for_invalid_sub(invalid_sub):
    payload = {'sub': invalid_sub}

    with pytest.raises(HTTPException) as exc:
        jwt_helpers.extract_sub(payload)

    assert exc.value.status_code == 401
    assert exc.value.detail == {'error': 'Invalid sub claim'}
