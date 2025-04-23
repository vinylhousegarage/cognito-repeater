import app.routers.auth
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
    async def fake_exchange_token(app, code):
        return {'id_token': 'dummy', 'access_token': 'dummy', 'refresh_token': 'dummy'}

    monkeypatch.setattr(app.routers.auth, 'exchange_token', fake_exchange_token)

    response = await app_client.get('/callback?code=abc123')
    assert response.status_code == 200
    assert response.json() == {'message': 'Login successful'}
