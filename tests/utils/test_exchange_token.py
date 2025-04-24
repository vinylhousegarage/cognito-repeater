import app.utils.auth_helpers as auth_helpers

async def test_create_token_request_payload(monkeypatch, app):
    dummy_metadata = {'token_endpoint': 'https://example.com/oauth2/token'}

    async def fake_cache_cognito_metadata(_):
          return dummy_metadata

    monkeypatch.setattr(auth_helpers, 'cache_cognito_metadata', fake_cache_cognito_metadata)

    url = dummy_metadata['token_endpoint']

    code = 'abc1234'
    config = app.state.config
    data = {
        'code': code,
        'redirect_uri': config.AWS_COGNITO_REDIRECT_URI,
        'grant_type': 'authorization_code',
        'client_id': config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        'client_secret': config.AWS_COGNITO_CLIENT_SECRET,
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    payload = {'url': url, 'data': data, 'headers': headers}

    result = await auth_helpers.create_token_request_payload(app, code)
    assert result == payload
