from fastapi import APIRouter, Depends, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.jwt_helpers import verify_access_token_only

router = APIRouter()
bearer_scheme = HTTPBearer()

@router.get('/docs')
async def protected_docs(request: Request, token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    access_token = token.credentials
    await verify_access_token_only(request, access_token)
    return get_swagger_ui_html(openapi_url='/openapi.json', title='Protected Swagger UI')

@router.get('/redoc')
async def protected_redoc(request: Request, token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    access_token = token.credentials
    await verify_access_token_only(request, access_token)
    return get_redoc_html(openapi_url='/openapi.json', title='Protected ReDoc')

@router.get('/openapi.json')
async def protected_openapi(request: Request, token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    access_token = token.credentials
    await verify_access_token_only(request, access_token)
    app = request.app
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    openapi_schema['info']['license'] = {
        'name': 'MIT License',
        'url': 'https://opensource.org/licenses/MIT'
    }
    return JSONResponse(openapi_schema)
