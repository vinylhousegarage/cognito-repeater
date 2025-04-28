from fastapi import HTTPException, Request
from jose import jwt
from jose.utils import base64url_decode
from httpx import AsyncClient
from app.utils.auth_helpers import cache_cognito_metadata

async def fetch_cognito_jwks(request: Request) -> dict:
    metadata = await cache_cognito_metadata(request)
    uri = metadata['jwks_uri']

    async with AsyncClient() as client:
        response = await client.get(url=uri)
        response.raise_for_status()

    return response.json()

def decode_access_token_for_kid(access_token: str) -> str:
    headers = jwt.get_unverified_header(access_token)
    return headers['kid']

async def search_jwk_by_kid(access_token: str, request: Request) -> dict:
    kid = decode_access_token_for_kid(access_token)
    jwks = await fetch_cognito_jwks(request)
    jwk = next((k for k in jwks['keys'] if k['kid'] == kid), None)

    if jwk is None:
        raise HTTPException(status_code=400, detail={'error': 'non_existent'})

    return jwk

def decode_jwk_to_binary(jwk: dict[str, str]) -> tuple[bytes, bytes]:
    try:
        n = base64url_decode(jwk['n'].encode('utf-8'))
        e = base64url_decode(jwk['e'].encode('utf-8'))
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f'Invalid JWK: missing field str{e.args[0]}')
    return n, e
