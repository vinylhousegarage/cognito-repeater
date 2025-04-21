from fastapi import APIRouter

router = APIRouter()

@router.get('/login')
def login():
    return {'url': 'https://login'}

@router.get('/callback')
def callback():
    return {'message': 'callback'}

@router.get('/me')
def get_me():
    return {'user': 'sub'}

@router.get('/logout')
def logout():
    return {'url': 'https://logout'}
