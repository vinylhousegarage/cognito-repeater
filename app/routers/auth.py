from fastapi import APIRouter
from app.utils.auth_helpers import redirect_to_cognito_login

router = APIRouter()

@router.get('/login')
def login():
    return redirect_to_cognito_login()

@router.get('/callback')
def callback():
    return {'message': 'callback'}

@router.get('/me')
def get_me():
    return {'user': 'sub'}

@router.get('/logout')
def logout():
    return {'url': 'https://logout'}
