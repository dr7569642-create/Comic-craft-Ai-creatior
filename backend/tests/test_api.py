from unittest.mock import patch
from pathlib import Path


def test_input_validation_empty_fields(client):
    """Test that empty or whitespace-only inputs are properly rejected."""
    # Test completely empty body
    response = client.post("/generate-comic/json", json={})
    assert response.status_code == 422

    # Test whitespace-only fields
    response = client.post(
        "/generate-comic/json",
        json={
            "prompt": "   ",
            "main_character": "Maya",
            "setting": "Neo City",
            "tone": "Adventure",
            "art_style": "Comic Book",
        },
    )
    assert response.status_code == 422


def test_input_validation_short_prompt(client):
    """Prompt must be at least 3 characters."""
    response = client.post(
        "/generate-comic/json",
        json={
            "prompt": "hi",
            "main_character": "Maya",
            "setting": "Neo City",
            "tone": "Adventure",
            "art_style": "Comic Book",
        },
    )
    assert response.status_code == 422


def test_test_image_endpoint_error_handling(client):
    """Verify error response formatting when image generation fails."""
    with patch("app.routes.generate_image", side_effect=RuntimeError("Generation network error")):
        response = client.post("/test-image", json={"prompt": "test prompt"})
        assert response.status_code == 500
        assert "Generation network error" in response.json()["detail"]


def test_test_image_endpoint_mocked_success(client, tmp_path):
    """Verify test-image response formatting on successful generation."""
    dummy_img = tmp_path / "test_gen.png"
    dummy_img.write_bytes(b"\x89PNG\r\n\x1a\nfakecontent")

    with patch("app.routes.generate_image", return_value=dummy_img):
        response = client.post("/test-image", json={"prompt": "Cyberpunk hero"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert f"/static/panels/{dummy_img.name}" == data["image_url"]
