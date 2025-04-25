import pytest
from httpx import AsyncClient, ASGITransport
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

