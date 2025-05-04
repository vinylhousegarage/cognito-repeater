from fastapi import APIRouter, Depends, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.jwt_helpers import verify_access_token_only

router = APIRouter()
bearer_scheme = HTTPBearer()

@router.get('/docs')
async def protected_docs(
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    access_token = token.credentials

    await verify_access_token_only(request, access_token)

    return get_swagger_ui_html(
        openapi_url='/openapi.json',
        title='Protected Swagger UI'
    )
