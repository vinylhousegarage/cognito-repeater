import app.utils.token_helpers
from httpx import AsyncClient

async def test_callback_missing_code(app_client: AsyncClient):
    response = await app_client.get('/callback')
    assert response.status_code == 400
    assert response.json() == {
        'detail': {
            'error': 'missing_code',
            'detail': 'Authorization code is required.'
        }
    }

async def test_callback_with_code(app_client: AsyncClient, monkeypatch):
    async def fake_create_token_request_payload(app, code: str) -> dict:
        return {
            'id_token': 'dummy',
            'access_token': 'dummy',
            'refresh_token': 'dummy',
        }

    monkeypatch.setattr(app.utils.token_helpers, 'create_token_request_payload', fake_create_token_request_payload)

    response = await app_client.get('/callback?code=abc123')
    assert response.status_code == 200
    assert response.json() == {
        'message': 'Login successful',
        'tokens': {
            'id_token': 'dummy',
            'access_token': 'dummy',
            'refresh_token': 'dummy',
        }
    }
