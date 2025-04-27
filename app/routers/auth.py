from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.utils.auth_helpers import generate_cognito_logout_url, redirect_to_cognito_login
from app.utils.token_helpers import exchange_token

router = APIRouter()
bearer_schema = HTTPBearer()

@router.get('/login')
async def login(request: Request) -> RedirectResponse:
    return await redirect_to_cognito_login(request)

@router.get('/callback')
async def callback(request: Request) -> dict:
    code = request.query_params.get('code')
    if not code:
        raise HTTPException(status_code=400, detail={'error': 'missing_code'})

    tokens = await exchange_token(request.app, code)

    return tokens

@router.get('/me')
async def get_me(token: HTTPAuthorizationCredentials = Depends(bearer_schema)) -> dict:
    return {'user': 'sub'}

@router.get('/logout')
async def logout(request: Request) -> RedirectResponse:
    logout_url = await generate_cognito_logout_url(request)
    return RedirectResponse(url=logout_url)
