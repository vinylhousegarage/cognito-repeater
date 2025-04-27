import pytest
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
def dummy_jwks_metadata():
    return {
        'keys': [
            {'kid': 'kid-dummy', 'kty': 'RSA', 'n': 'dummy-n', 'e': 'dummy-e'},
            {'kid': 'kid-fake', 'kty': 'RSA', 'n': 'fake-n', 'e': 'fake-e'},
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
