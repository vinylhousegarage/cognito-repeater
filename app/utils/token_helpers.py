from httpx import AsyncClient
from app.utils.auth_helpers import cache_cognito_metadata

async def create_token_request_payload(app, code):
    metaadata = await cache_cognito_metadata(app)
    url = metaadata['token_endpoint']

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

    return payload

async def exchange_token(app, code: str) -> dict:
    payload = await create_token_request_payload(app, code)
    url = payload['url']
    data = payload['data']
    headers = payload['headers']

    async with AsyncClient() as client:
        response = await client.post(url, data=data, headers=headers)
        response.raise_for_status()

    return response.json()
