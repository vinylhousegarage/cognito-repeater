import pytest
from httpx import AsyncClient
from app import create_app

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
