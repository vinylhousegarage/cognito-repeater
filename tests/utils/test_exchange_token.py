import app.utils.token_helpers as token_helpers

async def test_create_token_request_url(monkeypatch):
    dummy_url = 'https://example.com/oauth2/token/params'

    async def fake_exchange_token(app, code):
      return {'url': dummy_url}

    monkeypatch.setattr(token_helpers, 'exchange_token', fake_exchange_token)

    result = await token_helpers.exchange_token(app=None, code='dummy-code')
    assert result['url'] == dummy_url
