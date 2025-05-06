import httpx
from fastapi import HTTPException, Request
from httpx import AsyncClient
from app.utils.auth_helpers import cache_cognito_metadata

async def create_token_request_payload(request: Request, code: str) -> dict:
    metaadata = await cache_cognito_metadata(request)
    url = metaadata['token_endpoint']

    config = request.app.state.config
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

async def exchange_token(request: Request, code: str) -> dict:
    payload = await create_token_request_payload(request, code)
    url = payload['url']
    data = payload['data']
    headers = payload['headers']

    async with AsyncClient() as client:
        try:
            response = await client.post(url, data=data, headers=headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f'[ERROR] Token exchange failed: {e.response.status_code} - {e.response.text}')
            raise HTTPException(status_code=502, detail={'error': 'Token exchange failed'})

    return response.json()
