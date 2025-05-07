from fastapi import APIRouter
from app.model import MetadataResponse

router = APIRouter()

@router.get('/health')
def health_check():
    return {'status': 'ok'}

@router.get('/metadata', response_model=MetadataResponse)
def get_metadata():
    return {
        'login_endpoint': '/login',
        'logout_endpoint': '/logout',
        'verify_access_token_endpoint': '/token',
        'verify_userinfo_endpoint': '/user',
        'health_check_endpoint': '/health',
        'simulate_404_endpoint': '/error/404',
        'docs_url': '/docs',
        'redoc_url': '/redoc',
        'openapi_url': '/openapi.json',
    }
