import pytest
from fastapi.testclient import TestClient
from app import create_app

app = create_app()
client = TestClient(app)

@pytest.mark.parametrize('path,expected_status', [
    ('/error/404', 404),
])
def test_errors_endpoint_status_code(path, expected_status):
    response = client.get(path, follow_redirects=False)
    assert response.status_code == expected_status
