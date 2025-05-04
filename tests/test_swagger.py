async def test_docs_is_disabled(app_client):
    response = await app_client.get('/docs')
    assert response.status_code == 403
