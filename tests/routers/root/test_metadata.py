from httpx import AsyncClient
from app.model import MetadataResponse

async def test_metadata_endpoint_response(app_client: AsyncClient):
    response = await app_client.get('/metadata')
    assert response.status_code == 200
    data = response.json()

    _ = MetadataResponse(**data)  # Validate response structure

    for field_name, value in data.items():
        assert value.startswith('/'), f"{field_name} does not start with '/'"
