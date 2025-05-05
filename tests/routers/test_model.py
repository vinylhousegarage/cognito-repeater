from app.model import MetadataResponse

def test_metadata_response_valid():
    response = MetadataResponse(
        login_endpoint='/login',
        logout_endpoint='/logout',
        verify_access_token_endpoint='/me',
        verify_userinfo_endpoint='/sub',
        health_check_endpoint='/health',
        simulate_404_endpoint='/error/404',
        docs_url='/docs',
        redoc_url='/redoc',
        openapi_url='/openapi.json'
    )
    assert response.login_endpoint == '/login'
