import httpx
from fastapi import Request
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode

async def fetch_cognito_metadata(client: httpx.AsyncClient, metadata_url: str) -> dict:
    response = await client.get(metadata_url)
    response.raise_for_status()
    return response.json()

async def cache_cognito_metadata(request: Request) -> dict:
    if not hasattr(request.app.state, 'metadata'):
        async with httpx.AsyncClient() as client:
            request.app.state.metadata = await fetch_cognito_metadata(
              client, request.app.state.config.AWS_COGNITO_METADATA_URL
            )
    return request.app.state.metadata

async def redirect_to_cognito_login(request: Request) -> RedirectResponse:
    config = request.app.state.config
    metadata = await cache_cognito_metadata(request)
    login_url = metadata['authorization_endpoint']
    params = {
        'client_id': config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        'response_type': 'code',
        'scope': config.AWS_COGNITO_SCOPE,
        'redirect_uri': config.AWS_COGNITO_REDIRECT_URI,
    }
    full_url = f'{login_url}?{urlencode(params)}'
    return RedirectResponse(url=full_url)

async def generate_cognito_logout_url(request: Request) -> str:
    app = request.app
    config = app.state.config
    metadata = await cache_cognito_metadata(request)
    endpoint = metadata['end_session_endpoint']
    params = {
        'client_id': config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        'logout_uri': config.AWS_COGNITO_LOGOUT_URI,
    }
    return f'{endpoint}?{urlencode(params)}'
