from fastapi import Request
from httpx import AsyncClient
from app.utils.auth_helpers import cache_cognito_metadata

async def fetch_cognito_jwks(request: Request) -> dict:
    metadata = await cache_cognito_metadata(request)
    uri = metadata['jwks_uri']

    async with AsyncClient() as client:
        response = await client.get(url=uri)
        response.raise_for_status()

    return response.json()
