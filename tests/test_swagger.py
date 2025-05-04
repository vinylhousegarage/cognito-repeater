async def test_docs_is_disabled(app_client):
    response = await app_client.get('/docs')
    assert response.status_code == 403

async def test_docs_with_valid_token(app, httpx_mock, app_client, dummy_access_token):
    metadata_url = 'https://example.com/metadata_url'
    jwks_url = 'https://example.com/jwks'

    app.state.config = type('Config', (), {})()
    app.state.config.AWS_COGNITO_METADATA_URL = metadata_url

    httpx_mock.add_response(
        url=metadata_url,
        json={'jwks_uri': jwks_url}
    )

    response = await app_client.get(
        '/docs',
        headers={'Authorization': f'Bearer {dummy_access_token}'}
    )
    assert response.status_code == 200
    assert 'Swagger UI' in response.text
