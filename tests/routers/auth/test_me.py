from app.utils import auth_helpers

async def test_get_access_token(monkeypatch):
    dummy_access_token = {'key': 'value'}

    async def fake_get_access_token(*args, **kwargs):
        return dummy_access_token

    monkeypatch.setattr(auth_helpers, 'get_access_token', fake_get_access_token)

    access_token = await auth_helpers.get_access_token()

    assert access_token == dummy_access_token
