import app.utils.auth_helpers as auth_helpers
from fastapi import Request
from urllib.parse import urlencode

async def test_generate_cognito_logout_url(request: Request, monkeypatch):
    dummy_metadata = {'logout_endpoint': 'https://dummy.com/logout/'}
    async def fake_cache_cognito_metadata(app):
        return dummy_metadata

    monkeypatch.setattr(auth_helpers, 'cache_cognito_metadata', fake_cache_cognito_metadata)

    endpoint = dummy_metadata['logout_endpoint']
    params = {
        'client_id': 'dummy-id',
        'logout_uri': 'dummy-uri',
    }

    expected_url = f'{endpoint}?{urlencode(params)}'

    logout_url = await auth_helpers.generate_cognito_logout_url(request)

    assert logout_url == expected_url
