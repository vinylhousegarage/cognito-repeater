from fastapi.testclient import TestClient
from app import create_app

app = create_app()
client = TestClient(app)

def test_health_status_code():
    response = client.get('/health')
    assert response.status_code == 200
