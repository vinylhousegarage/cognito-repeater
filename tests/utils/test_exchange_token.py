from types import SimpleNamespace
import app.utils.token_helpers as token_helpers

async def test_create_token_request_payload(monkeypatch, app, dummy_code):
    dummy_metadata = {'token_endpoint': 'https://example.com/oauth2/token'}

    async def fake_cache_cognito_metadata(_):
        return dummy_metadata

    monkeypatch.setattr(token_helpers, 'cache_cognito_metadata', fake_cache_cognito_metadata)

    request = SimpleNamespace(app=app)

    config = app.state.config
    data = {
        'code': dummy_code,
        'redirect_uri': config.AWS_COGNITO_REDIRECT_URI,
        'grant_type': 'authorization_code',
        'client_id': config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        'client_secret': config.AWS_COGNITO_CLIENT_SECRET,
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'url': dummy_metadata['token_endpoint'], 'data': data, 'headers': headers}

    result = await token_helpers.create_token_request_payload(request, dummy_code)
    assert result == payload


async def test_exchange_token(httpx_mock, monkeypatch, app, dummy_code):
    dummy_claims = {
        'url': 'https://example.com/token',
        'data': {'code': dummy_code},
        'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
    }

    dummy_response_data = {
        'access_token': 'dummy_access',
        'id_token': 'dummy_id',
        'refresh_token': 'dummy_refresh',
        'token_type': 'Bearer',
        'expires_in': 3600,
    }

    async def fake_create_token_request_payload(request, code):
        return dummy_claims

    monkeypatch.setattr(token_helpers, 'create_token_request_payload', fake_create_token_request_payload)

    httpx_mock.add_response(
        url=dummy_claims['url'],
        json=dummy_response_data,
    )

    request = SimpleNamespace(app=app)

    result = await token_helpers.exchange_token(request, dummy_code)
    assert result == dummy_response_data
