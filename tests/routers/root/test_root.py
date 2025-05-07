from fastapi.testclient import TestClient
from app import create_app

app = create_app()
client = TestClient(app)

def test_root_endpoint_redirects_to_login():
    response = client.get('/', allow_redirects=False)
    assert response.status_code == 307
    assert response.headers['location'] == '/login'
