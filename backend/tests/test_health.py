def test_health_check(client):
    """Verify /health endpoint returns correct JSON structure and status code."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "ComicCraft"
    assert "environment" in data


def test_api_health_check(client):
    """Verify /api/health endpoint alias."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "ComicCraft"
