import app.routers.auth
from fastapi.responses import RedirectResponse
from httpx import AsyncClient

async def test_login_redirect(client: AsyncClient, monkeypatch) -> None:
    def fake_redirect() -> RedirectResponse:
        return RedirectResponse(url='https://example.com/login')

    monkeypatch.setattr(app.routers.auth, 'redirect_to_cognito_login', fake_redirect)

    response = await client.get('/login', follow_redirects=False)
    assert response.status_code == 307
    assert response.headers['location'].startswith('https://')
