async def test_root_endpoint_redirects_to_login(app_client):
    response = app_client.get('/', allow_redirects=False)
    assert response.status_code == 307
    assert response.headers['location'] == '/login'
