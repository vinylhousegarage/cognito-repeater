from httpx import AsyncClient

async def test_me_returns_sub(app_client: AsyncClient, dummy_access_token: str):
    response = await app_client.get(
        '/me',
        headers={'Authorization': f'Bearer {dummy_access_token}'}
    )
    assert response.status_code == 200
    assert response.json() == {'user': 'user-id'}
