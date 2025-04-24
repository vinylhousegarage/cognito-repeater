from app.utils.token_helpers import create_token_request_url
from urllib.parse import urlencode

async def test_create_token_request_url(app):
    metadata = app.state.metadata
    config = app.state.config

    endpoint = metadata['token_endpoint']
    params = {
        'grant_type': 'authorization_code',
        'client_id': config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        'client_secret': config.AWS_COGNITO_CLIENT_SECRET,
    }

    expected = f'{endpoint}?{urlencode(params)}'

    result = await create_token_request_url(app)
    assert result == expected
