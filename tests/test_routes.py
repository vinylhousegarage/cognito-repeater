import pytest
from fastapi.testclient import TestClient
from app import create_app

app = create_app()
client = TestClient(app)

@pytest.mark.parametrize('path,expected_status', [
    ('/login', 307),
    ('/logout', 200),
    ('/callback', 200),
    ('/me', 200),
    ('/health', 200),
    ('/not-exist', 404),
])
def test_routes_status_code(path, expected_status):
    response = client.get(path)
    assert response.status_code == expected_status
