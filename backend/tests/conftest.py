import pytest
from pathlib import Path
from PIL import Image, ImageDraw
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings


@pytest.fixture(scope="session")
def client():
    """FastAPI TestClient instance."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def sample_test_images(tmp_path_factory) -> list[Path]:
    """Create 5 valid PNG image files for testing layout and PDF generation."""
    temp_dir = tmp_path_factory.mktemp("test_panels")
    image_paths = []
    colors = ["#ff3344", "#2563eb", "#10b981", "#7c3aed", "#ffea00"]

    for i, color in enumerate(colors, start=1):
        img_path = temp_dir / f"test_panel_{i}.png"
        img = Image.new("RGB", (600, 600), color=color)
        draw = ImageDraw.Draw(img)
        draw.text((200, 280), f"TEST PANEL {i}", fill="white" if i != 5 else "black")
        img.save(img_path, format="PNG")
        image_paths.append(img_path)

    return image_paths
