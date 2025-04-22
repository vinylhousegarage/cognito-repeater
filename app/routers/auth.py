from fastapi import APIRouter, Request
from app.utils.auth_helpers import redirect_to_cognito_login

router = APIRouter()

@router.get('/login')
async def login(request: Request):
    return await redirect_to_cognito_login(request)

@router.get('/callback')
def callback():
    return {'message': 'callback'}

@router.get('/me')
def get_me():
    return {'user': 'sub'}

@router.get('/logout')
def logout():
    return {'url': 'https://logout'}
