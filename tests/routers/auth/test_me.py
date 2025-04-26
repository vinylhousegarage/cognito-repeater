async def test_get_access_token(app_client):
    dummy_access_token = 'dummy-access-token'

    response = await app_client.get(
        '/me',
        headers={'Authorization': f'Bearer {dummy_access_token}'}
    )

    assert response.status_code == 200
    assert 'user' in response.json()
