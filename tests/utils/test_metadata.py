from app.utils.auth_helpers import fetch_cognito_metadata
from app.config import Config

async def test_fetch_cognito_metadata(httpx_mock):
    dummy_metadata = {
        'authorization_endpoint': 'https://example.com/oauth2/authorize',
        'token_endpoint': 'https://example.com/oauth2/token'
    }

    config = Config()
    httpx_mock.add_response(
        url=config.AWS_COGNITO_METADATA_URL,
        json=dummy_metadata
    )

    result = await fetch_cognito_metadata()

    assert result == dummy_metadata
