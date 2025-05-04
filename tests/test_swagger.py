def test_docs_is_disabled(client):
    response = client.get('/docs')
    assert response.status_code == 404
