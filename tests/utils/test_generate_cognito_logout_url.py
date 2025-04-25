import app.utils.auth_helpers as auth_helpers
from types import SimpleNamespace
from urllib.parse import urlencode

async def test_generate_cognito_logout_url(monkeypatch):
    dummy_metadata = {'end_session_endpoint': 'https://dummy.com/logout/'}

    async def fake_cache_cognito_metadata(app):
        return dummy_metadata

    monkeypatch.setattr(auth_helpers, 'cache_cognito_metadata', fake_cache_cognito_metadata)

    endpoint = dummy_metadata['end_session_endpoint']
    params = {
        'client_id': 'dummy-id',
        'logout_uri': 'dummy-uri',
    }
    expected_url = f'{endpoint}?{urlencode(params)}'

    dummy_config = SimpleNamespace(
        AWS_COGNITO_USER_POOL_CLIENT_ID='dummy-id',
        AWS_COGNITO_LOGOUT_URI='dummy-uri',
    )
    dummy_app = SimpleNamespace(state=SimpleNamespace(config=dummy_config))
    dummy_request = SimpleNamespace(app=dummy_app)
    logout_url = await auth_helpers.generate_cognito_logout_url(dummy_request)

    assert logout_url == expected_url
