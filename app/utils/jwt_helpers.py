from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from fastapi import HTTPException, Request
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError, JWSSignatureError
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

def cache_public_key_by_kid(request: Request, kid: str, public_key: RSAPublicKey) -> None:
    if not hasattr(request.app.state, 'public_keys'):
        request.app.state.public_keys = {}
    request.app.state.public_keys[kid] = public_key

def log_jwt_error(e: Exception) -> None:
    print(f'debug-{type(e).__name__}-str(e): {str(e)}')
    print(f'debug-{type(e).__name__}-type(e): {type(e)}')

def verify_access_token(request: Request, access_token: str, public_key: RSAPublicKey, leeway = 10):
    if public_key is None:
        raise HTTPException(status_code=401, detail={'error': 'Public key not found', 'type': 'MissingPublicKeyError'})
    if not access_token:
        raise HTTPException(status_code=401, detail={'error': 'Missing token', 'type': 'JWTError'})
    try:
        payload = jwt.decode(
            access_token,
            public_key,
            algorithms = ['RS256'],
            audience = request.app.state.config.AWS_COGNITO_USER_POOL_CLIENT_ID,
            issuer = request.app.state.metadata['issuer'],
            options = {
                'verify_exp': True,
                'leeway': leeway,
            }
        )
    except ExpiredSignatureError as e:
        log_jwt_error(e)
        raise HTTPException(status_code=401, detail={'error': str(e), 'type': type(e).__name__})
    except JWSSignatureError as e:
        log_jwt_error(e)
        raise HTTPException(status_code=401, detail={'error': str(e), 'type': type(e).__name__})
    except JWTClaimsError as e:
        log_jwt_error(e)
        raise HTTPException(status_code=401, detail={'error': str(e), 'type': type(e).__name__})
    except JWTError as e:
        log_jwt_error(e)
        raise HTTPException(status_code=401, detail={'error': str(e), 'type': type(e).__name__})

    required_claims = ['sub', 'iss', 'aud', 'exp']
    for claim in required_claims:
        if claim not in payload:
            raise HTTPException(
                status_code=401,
                detail={
                    'error': f'Missing {claim} claim',
                    'type': 'MissingClaimError'
                }
            )

    return payload

def extract_sub(payload: dict) -> str:
    sub = payload.get('sub')
    if not sub or not isinstance(sub, str):
        raise HTTPException(status_code=401, detail={'error': 'Invalid sub claim'})
    return sub

async def verify_and_extract_sub(request: Request, access_token: str) -> str:
    jwk = await search_jwk_by_kid(access_token, request)
    bytes_n, bytes_e = decode_jwk_to_bytes(jwk)
    int_n, int_e = convert_bytes_to_int(bytes_n, bytes_e)
    public_key = generate_public_key(int_e, int_n)
    cache_public_key_by_kid(request, jwk['kid'], public_key)
    payload = verify_access_token(request, access_token, public_key)
    return extract_sub(payload)

async def verify_access_token_only(request: Request, access_token: str) -> None:
    jwk = await search_jwk_by_kid(access_token, request)
    bytes_n, bytes_e = decode_jwk_to_bytes(jwk)
    int_n, int_e = convert_bytes_to_int(bytes_n, bytes_e)
    public_key = generate_public_key(int_e, int_n)
    cache_public_key_by_kid(request, jwk['kid'], public_key)
    verify_access_token(request, access_token, public_key)
