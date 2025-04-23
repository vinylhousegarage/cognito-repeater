from httpx import AsyncClient

async def test_callback_missing_code(app_client: AsyncClient) -> None:
    response = await app_client.get('/callback')
    assert response.status_code == 400
    assert response.json() == {
        'error': 'missing_code',
        'detail': 'Authorization code is required.'
    }
