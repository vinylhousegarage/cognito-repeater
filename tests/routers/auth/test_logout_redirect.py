from fastapi.testclient import TestClient
from app import create_app

app = create_app()
client = TestClient(app)

def test_logout_redirect_returns_200_and_success_message():
    response = client.get('/logout/redirect')
    assert response.status_code == 200, f'Expected 200 OK, but got {response.status_code}. Response body: {response.text}'
    assert response.json() == {'message': 'Logout successful'}
