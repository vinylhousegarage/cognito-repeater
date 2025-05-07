async def test_root_endpoint_redirects_to_login(app_client):
    response = await app_client.get('/')
    assert response.status_code == 307
    assert response.headers['location'] == '/login'
