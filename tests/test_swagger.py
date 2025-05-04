async def test_docs_is_disabled(app_client):
    response = await app_client.get('/docs')
    assert response.status_code == 403

async def test_docs_with_valid_token(app_client, dummy_access_token):
    response = await app_client.get(
        '/docs',
        headers={'Authorization': f'Bearer {dummy_access_token}'}
    )
    assert response.status_code == 200
    assert 'Swagger UI' in response.text
