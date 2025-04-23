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
