from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from app.utils.auth_helpers import redirect_to_cognito_login
from app.utils.token_helpers import create_token_request_payload

router = APIRouter()

@router.get('/login')
async def login(request: Request) -> RedirectResponse:
    return await redirect_to_cognito_login(request)

@router.get('/callback')
async def callback(request: Request):
    code = request.query_params.get('code')
    if not code:
        raise HTTPException(
            status_code=400,
            detail={
                'error': 'missing_code',
                'detail': 'Authorization code is required.'
            }
        )

    tokens = await create_token_request_payload(request.app, code)

    return JSONResponse(
        status_code=200,
        content={'message': 'Login successful', 'tokens': tokens},
    )

@router.get('/me')
def get_me():
    return {'user': 'sub'}

@router.get('/logout')
def logout():
    return {'url': 'https://logout'}
