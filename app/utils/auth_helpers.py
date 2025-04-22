import httpx
from fastapi.responses import RedirectResponse
from app.config import Config

def redirect_to_cognito_login() -> RedirectResponse:
    return RedirectResponse(url='https://example.com/login')

async def fetch_cognito_metadata(client: httpx.AsyncClient) -> dict:
    response = await client.get(Config.AWS_COGNITO_METADATA_URL)
    response.raise_for_status()
    return response.json()
