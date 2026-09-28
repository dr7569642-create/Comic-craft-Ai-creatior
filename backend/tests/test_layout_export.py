import pytest
from pathlib import Path
from PIL import Image
from app.schemas import (
    ComicCreateRequest,
    ComicOutline,
    ComicStory,
    PanelOutline,
    PanelStory,
)
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf


@pytest.fixture
def mock_story_and_outline():
    outline = ComicOutline(
        title="The Quantum Bot Discovery",
        character_appearance="Maya has messy dark brown hair, brass aviator goggles, and a brown leather flight jacket.",
        panels=[
            PanelOutline(
                panel_number=i,
                scene_description=f"Scene description for panel {i}",
                action=f"Action occurring in panel {i}",
                characters="Maya",
                location="Neo-Aetheria",
                visual_direction=f"Camera angle for panel {i}",
                emotional_beat=f"Beat {i}",
                suggested_dialogue=f"Dialogue line {i}",
            )
            for i in range(1, 6)
        ],
    )

    story = ComicStory(
        title="The Quantum Bot Discovery",
        panels=[
            PanelStory(
                panel_number=i,
                narration=f"Narration text for panel {i} describing the narrative progress.",
                dialogue=f"Maya: 'This is the discovery of panel {i}!'",
                visual_description=f"Vivid visual representation of panel {i}.",
                action=f"Maya moves forward in panel {i}.",
                character_info="Maya looking adventurous and curious.",
                environment="High altitude steampunk sky workshop.",
                mood="Excited and mysterious",
                image_prompt=f"A vibrant comic panel {i} showing Maya in her workshop",
            )
            for i in range(1, 6)
        ],
    )

    req = ComicCreateRequest(
        prompt="A young inventor discovers a mysterious robot in a floating sky workshop.",
        main_character="Maya",
        setting="Neo-Aetheria",
        tone="Adventure",
        art_style="Comic Book",
    )

    return outline, story, req


def test_build_comic_layout_success(mock_story_and_outline, sample_test_images):
    """Test successful construction of ComicLayout with 5 validated panels."""
    outline, story, req = mock_story_and_outline

    layout = build_comic_layout(
        story=story,
        outline=outline,
        image_paths=sample_test_images,
        user_input=req,
    )

    assert layout.title == "The Quantum Bot Discovery"
    assert len(layout.panels) == 5
    assert layout.art_style == "Comic Book"
    assert layout.main_character == "Maya"

    for idx, panel in enumerate(layout.panels, start=1):
        assert panel.panel_number == idx
        assert panel.image_url.startswith("/static/panels/")
        assert Path(panel.image_path).exists()
        assert panel.narration.startswith(f"Narration text for panel {idx}")
        assert "Maya" in panel.dialogue


def test_build_comic_layout_rejects_invalid_image_count(mock_story_and_outline, sample_test_images):
    """Test that fewer than 5 images raises ValueError."""
    outline, story, req = mock_story_and_outline

    with pytest.raises(ValueError, match="Expected exactly 5 panel images"):
        build_comic_layout(
            story=story,
            outline=outline,
            image_paths=sample_test_images[:4],  # Only 4 images
            user_input=req,
        )


def test_pdf_export_generation(mock_story_and_outline, sample_test_images):
    """Verify that save_pdf produces a genuine, non-empty PDF file containing panels."""
    outline, story, req = mock_story_and_outline

    layout = build_comic_layout(
        story=story,
        outline=outline,
        image_paths=sample_test_images,
        user_input=req,
    )

    pdf_path, download_url = save_pdf(layout)

    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 1000  # Genuine PDF with embedded images
    assert download_url.startswith("/static/exports/comic_")
    assert download_url.endswith(".pdf")
