import httpx
from fastapi import Request
from fastapi.responses import RedirectResponse

async def redirect_to_cognito_login(request: Request) -> RedirectResponse:
    config = request.app.state.config
    async with httpx.AsyncClient() as client:
        metadata = await fetch_cognito_metadata(client, config.AWS_COGNITO_METADATA_URL)

    login_url = metadata['authorization_endpoint']

    params = {
        'client_id': config.AWS_COGNITO_USER_POOL_CLIENT_ID,
        'response_type': 'code',
        'scope': config.AWS_COGNITO_SCOPE,
        'redirect_uri': config.AWS_COGNITO_REDIRECT_URI,
    }
    from urllib.parse import urlencode
    full_url = f'{login_url}?{urlencode(params)}'
    return RedirectResponse(url=full_url)

async def fetch_cognito_metadata(client: httpx.AsyncClient, metadata_url: str) -> dict:
    response = await client.get(metadata_url)
    response.raise_for_status()
    return response.json()
