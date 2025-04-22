async def test_redirect_cognito_login(client):
    response = await client.get('/login', follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['location'].startswith('https://')
