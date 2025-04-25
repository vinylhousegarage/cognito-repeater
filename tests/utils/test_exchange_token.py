import app.utils.token_helpers as token_helpers

async def test_create_token_request_payload(monkeypatch, app, dummy_code):
    dummy_metadata = {'token_endpoint': 'https://example.com/oauth2/token'}

    async def fake_cache_cognito_metadata(_):
          return dummy_metadata

    monkeypatch.setattr(token_helpers, 'cache_cognito_metadata', fake_cache_cognito_metadata)

    url = dummy_metadata['token_endpoint']

    config = app.state.config
    data = {
        'code': dummy_code,
        'redirect_uri': config.AWS_COGNITO_REDIRECT_URI,
        'grant_type': 'authorization_code',
        'client_id': config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        'client_secret': config.AWS_COGNITO_CLIENT_SECRET,
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    payload = {'url': url, 'data': data, 'headers': headers}

    result = await token_helpers.create_token_request_payload(app, dummy_code)
    assert result == payload

async def test_exchange_token(httpx_mock, monkeypatch, app, dummy_code):
    dummy_payload = {
        'url': 'https://example.com/token',
        'data': {'code': 'abc1234'},
        'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
    }

    dummy_response_data = {
        'access_token': 'dummy_access',
        'id_token': 'dummy_id',
        'refresh_token': 'dummy_refresh',
        'token_type': 'Bearer',
        'expires_in': 3600,
    }

    async def fake_create_token_request_payload(app, code):
        return dummy_payload

    monkeypatch.setattr(token_helpers, 'create_token_request_payload', fake_create_token_request_payload)

    httpx_mock.add_response(
        url=dummy_payload['url'],
        json=dummy_response_data,
    )

    result = await token_helpers.exchange_token(app, dummy_code)
    assert result == dummy_response_data
