import app.routers.auth
from httpx import AsyncClient

async def test_callback_endpoint_missing_code(app_client: AsyncClient):
    response = await app_client.get('/callback')
    assert response.status_code == 400
    assert response.json() == {
            'detail': {
                'error': 'missing_code',
            },
        }

async def test_callback_endpoint_with_code(app_client: AsyncClient, monkeypatch):
    async def fake_exchange_token(app, code: str) -> dict:
        return {
            'id_token': 'dummy',
            'access_token': 'dummy',
            'refresh_token': 'dummy',
        }

    monkeypatch.setattr(app.routers.auth, 'exchange_token', fake_exchange_token)

    response = await app_client.get('/callback?code=abc123')
    assert response.status_code == 200
    assert response.json() == {
            'id_token': 'dummy',
            'access_token': 'dummy',
            'refresh_token': 'dummy',
        }

async def test_callback_endpoint_returns_json_response(app_client: AsyncClient, monkeypatch):
    dummy_response_data = {
        'access_token': 'dummy_access_token',
        'id_token': 'dummy_id_token',
        'refresh_token': 'dummy_refresh_token',
        'token_type': 'Bearer',
        'expires_in': 3600
    }

    async def fake_exchange_token(app, code):
        return dummy_response_data

    monkeypatch.setattr(app.routers.auth, 'exchange_token', fake_exchange_token)

    response = await app_client.get('/callback?code=test-code')

    assert response.status_code == 200
    assert response.json() == dummy_response_data
