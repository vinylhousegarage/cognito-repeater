from app.utils.auth_helpers import cache_cognito_metadata
from urllib.parse import urlencode

async def create_token_request_url(app):
    meatadata = await cache_cognito_metadata(app)
    config = app.state.config

    endpoint = meatadata['token_endpoint']
    params = {
        'grant_type': 'authorization_code',
        'client_id': config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        'client_secret': config.AWS_COGNITO_CLIENT_SECRET,
    }

    return f'{endpoint}?{urlencode(params)}'

async def exchange_token(app, code: str) -> dict:

    return {
        'id_token': 'dummy',
        'access_token': 'dummy',
        'refresh_token': 'dummy'
    }
