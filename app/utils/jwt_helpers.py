from cryprography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
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

def decode_jwk_to_bytes(jwk: dict[str, str]) -> tuple[bytes, bytes]:
    try:
        bytes_n = base64url_decode(jwk['n'].encode('utf-8'))
        bytes_e = base64url_decode(jwk['e'].encode('utf-8'))
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f'Invalid JWK: missing field str{e.args[0]}')
    return bytes_n, bytes_e

def convert_bytes_to_int(bytes_n: bytes, bytes_e: bytes) -> tuple[int, int]:
    int_n = int.from_bytes(bytes_n, 'big')
    int_e = int.from_bytes(bytes_e, 'big')
    return int_n, int_e

def generate_public_key(int_e: int, int_n: int) -> RSAPublicKey:
    public_key = rsa.RSAPublicNumbers(int_e, int_n).public_key()
    return public_key

def convert_public_key_to_pem(public_key: RSAPublicKey) -> bytes:
    pem = public_key.public_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem
