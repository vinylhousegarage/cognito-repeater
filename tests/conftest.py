import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
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
