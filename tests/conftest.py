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
