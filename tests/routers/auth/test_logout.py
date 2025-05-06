import app.routers.auth
from httpx import AsyncClient

async def test_logout_endpoint_returns_redirect(app_client: AsyncClient, monkeypatch):
    dummy_url = 'https://example.com/cognito/logout/?cleint_id=abc'

    async def fake_generate_cognito_logout_url(*args, **kwargs):
        return dummy_url

    monkeypatch.setattr(app.routers.auth, 'generate_cognito_logout_url', fake_generate_cognito_logout_url)

    response = await app_client.get('/logout', follow_redirects=False)
    assert response.status_code == 307
    assert response.headers['location'] == dummy_url
