from httpx import AsyncClient

async def test_token_endpoint_returns_sub(app_client: AsyncClient, test_access_token: str, cache_cognito_metadata_httpx_mock):
    response = await app_client.get(
        '/token',
        headers={'Authorization': f'Bearer {test_access_token}'}
    )
    assert response.status_code == 200
    assert response.json() == {'sub': 'user-id'}
