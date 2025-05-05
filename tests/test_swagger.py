async def test_docs_is_disabled(app_client):
    response = await app_client.get('/docs')
    assert response.status_code == 403

async def test_docs_with_valid_token(app_client, test_access_token, cache_cognito_metadata_httpx_mock):
    response = await app_client.get(
        '/docs',
        headers={'Authorization': f'Bearer {test_access_token}'}
    )
    assert response.status_code == 200
    assert 'Swagger UI' in response.text

async def test_redoc_is_disabled(app_client):
    response = await app_client.get('/redoc')
    assert response.status_code == 403

async def test_redoc_with_valid_token(app_client, test_access_token, cache_cognito_metadata_httpx_mock):
    response = await app_client.get(
        '/redoc',
        headers={'Authorization': f'Bearer {test_access_token}'}
    )
    assert response.status_code == 200
    assert 'ReDoc' in response.text

async def test_openapi_is_disabled(app_client):
    response = await app_client.get('/openapi.json')
    assert response.status_code == 403

async def test_openapi_with_valid_token(app_client, test_access_token, cache_cognito_metadata_httpx_mock):
    response = await app_client.get(
        '/openapi.json',
        headers={'Authorization': f'Bearer {test_access_token}'}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['openapi'].startswith('3.')
    assert data['info']['title'] == 'FastAPI'
    assert data['info']['license']['name'] == 'MIT License'
    assert data['info']['license']['url'] == 'https://opensource.org/licenses/MIT'
