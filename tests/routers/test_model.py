import pytest
from pydantic import ValidationError
from app.model import MetadataResponse

def test_metadata_response_valid():
    response = MetadataResponse(
        login_endpoint='/login',
        logout_endpoint='/logout',
        verify_access_token_endpoint='/token',
        verify_userinfo_endpoint='/user',
        health_check_endpoint='/health',
        simulate_404_endpoint='/error/404',
        docs_url='/docs',
        redoc_url='/redoc',
        openapi_url='/openapi.json'
    )
    assert response.login_endpoint == '/login'

def test_metadata_response_invalid_path():
    with pytest.raises(ValidationError) as exc:
        MetadataResponse(
            login_endpoint='login',
            logout_endpoint='/logout',
            verify_access_token_endpoint='/token',
            verify_userinfo_endpoint='/user',
            health_check_endpoint='/health',
            simulate_404_endpoint='/error/404',
            docs_url='/docs',
            redoc_url='/redoc',
            openapi_url='/openapi.json'
        )
    assert "must start with '/'" in str(exc.value)
