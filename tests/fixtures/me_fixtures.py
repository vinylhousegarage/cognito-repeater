import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta, timezone
from jose import jwt
from jose.utils import base64url_encode
from types import SimpleNamespace

@pytest.fixture
def test_kid():
    return 'test-kid'

@pytest.fixture
def test_private_key():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

@pytest.fixture
def test_private_key_pem(test_private_key):
    return test_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

@pytest.fixture
def test_claims():
    return {
        'sub': 'user-id',
        'iss': 'https://example.com',
        'aud': 'user-pool-client-id',
        'exp': int((datetime.now(timezone.utc) + timedelta(minutes=5)).timestamp()),
    }

@pytest.fixture
def test_access_token(test_claims, test_private_key_pem, test_kid):
        return jwt.encode(
            test_claims,
            key=test_private_key_pem,
            algorithm='RS256',
            headers={'kid': test_kid},
        )

@pytest.fixture
def cache_cognito_metadata_httpx_mock(app, httpx_mock, test_private_key, test_kid):
    public_numbers = test_private_key.public_key().public_numbers()
    e = base64url_encode(public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, 'big')).decode()
    n = base64url_encode(public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, 'big')).decode()

    app.state.config = SimpleNamespace()
    app.state.config.AWS_COGNITO_METADATA_URL = 'https://example.com/.well-known/openid-configuration'
    app.state.config.AWS_COGNITO_USER_POOL_CLIENT_ID = 'user-pool-client-id'

    httpx_mock.add_response(
        url='https://example.com/.well-known/openid-configuration',
        json={'issuer': 'https://example.com', 'jwks_uri': 'https://example.com/jwks'}
    )

    httpx_mock.add_response(
        url='https://example.com/jwks',
        json={'keys': [{'kid': test_kid, 'kty': 'RSA', 'n': n, 'e': e}]}
    )
