import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from jose import jwt
from types import SimpleNamespace
from app import create_app

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
async def app_client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as app_client:
        yield app_client

@pytest.fixture
async def async_client():
    async with AsyncClient() as async_client:
        yield async_client

@pytest.fixture
def dummy_code():
    return 'abc1234'

@pytest.fixture
def test_client(app):
    return TestClient(app)

@pytest.fixture
def dummy_kid():
    return 'dummy-kid'

@pytest.fixture
def dummy_jwks_metadata():
    return {
        'jwks_uri': 'https://example.com/jwks',
        'keys': [
            {'kid': 'dummy-kid', 'kty': 'RSA', 'n': 'dummy-n', 'e': 'dummy-e'},
            {'kid': 'fake-kid', 'kty': 'RSA', 'n': 'fake-n', 'e': 'fake-e'},
        ]
    }

@pytest.fixture
def dummy_app_attr_state():
    app = SimpleNamespace()
    app.state = SimpleNamespace()
    return app

@pytest.fixture
def dummy_request(dummy_app_attr_state):
    request = SimpleNamespace()
    request.app = dummy_app_attr_state
    return request

@pytest.fixture
def dummy_jwks_request(dummy_request, dummy_jwks_metadata):
    dummy_request.app.state.metadata = dummy_jwks_metadata
    return dummy_request

@pytest.fixture
def fetch_cognito_jwks_httpx_mock(dummy_jwks_request, httpx_mock):
    dummy_metadata = dummy_jwks_request.app.state.metadata
    return httpx_mock.add_response(
        url=dummy_metadata['jwks_uri'],
        json={'keys': dummy_metadata['keys']},
    )

@pytest.fixture
def dummy_e_int():
    return 65537

@pytest.fixture
def dummy_p_int():
    return 257

@pytest.fixture
def dummy_q_int():
    return 263

@pytest.fixture
def dummy_n_int(dummy_p_int, dummy_q_int):
    return dummy_p_int * dummy_q_int

@pytest.fixture
def dummy_public_key(dummy_e_int, dummy_n_int):
    return rsa.RSAPublicNumbers(dummy_e_int, dummy_n_int).public_key()

@pytest.fixture
def dummy_second_q_int():
    return 269

@pytest.fixture
def dummy_second_n_int(dummy_p_int, dummy_second_q_int):
    return dummy_p_int * dummy_second_q_int

@pytest.fixture
def dummy_second_public_key(dummy_e_int, dummy_second_n_int):
    return rsa.RSAPublicNumbers(dummy_e_int, dummy_second_n_int).public_key()

@pytest.fixture
def dummy_private_key_for_verify():
    return rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048,
    )

@pytest.fixture
def dummy_public_key_for_verify(dummy_private_key_for_verify):
    return dummy_private_key_for_verify.public_key()

@pytest.fixture
def dummy_private_key_for_verify_to_pem(dummy_private_key_for_verify):
    private_pem = dummy_private_key_for_verify.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return private_pem.decode('utf-8')

@pytest.fixture
def dummy_second_private_key_for_verify():
    return rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048,
    )

@pytest.fixture
def dummy_second_public_key_for_verify(dummy_second_private_key_for_verify):
    return dummy_second_private_key_for_verify.public_key()

@pytest.fixture
def dummy_leeway():
    return 10

@pytest.fixture
def dummy_request_for_verify(dummy_request):
    dummy_request.app.state.metadata = {'issuer': 'https://example.com'}
    dummy_request.app.state.config = SimpleNamespace()
    dummy_request.app.state.config.AWS_COGNITO_USER_POOL_CLIENT_ID = 'test-client-id'
    return dummy_request

@pytest.fixture
def dummy_claims(dummy_request_for_verify):
    return {
        'sub': 'user-id',
        'iss': dummy_request_for_verify.app.state.metadata['issuer'],
        'aud': dummy_request_for_verify.app.state.config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=5)
    }

@pytest.fixture
def dummy_access_token_factory(dummy_private_key_for_verify_to_pem, dummy_kid):
    def _create_dummy_access_token(dummy_claims: dict) -> str:
        dummy_access_token = jwt.encode(
            dummy_claims,
            key = dummy_private_key_for_verify_to_pem,
            algorithm = 'RS256',
            headers = {'kid': dummy_kid},
        )
        return dummy_access_token
    return _create_dummy_access_token

@pytest.fixture
def dummy_payload_factory(
    dummy_access_token_factory,
    dummy_public_key_for_verify,
    dummy_leeway,
):
    def _create_dummy_payload(dummy_claims: dict) -> dict:
        dummy_access_token = dummy_access_token_factory(dummy_claims)
        dummy_payload = jwt.decode(
            dummy_access_token,
            dummy_public_key_for_verify,
            algorithms = ['RS256'],
            audience = dummy_claims['aud'],
            issuer = dummy_claims['iss'],
            options={'verify_exp': True, 'leeway': dummy_leeway},
        )
        return dummy_payload
    return _create_dummy_payload
