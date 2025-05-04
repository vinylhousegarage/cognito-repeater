def test_docs_is_disabled(app_client):
    response = app_client.get('/docs')
    assert response.status_code == 404
