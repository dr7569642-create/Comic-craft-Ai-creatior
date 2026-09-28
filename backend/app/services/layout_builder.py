import logging
from pathlib import Path
from typing import List
from app.config import settings
from app.schemas import ComicCreateRequest, ComicLayout, ComicOutline, ComicPanel, ComicStory
from app.services.image_generator import validate_image_file

logger = logging.getLogger(__name__)


def build_comic_layout(
    story: ComicStory,
    outline: ComicOutline,
    image_paths: List[Path],
    user_input: ComicCreateRequest,
) -> ComicLayout:
    """Build the structured comic layout combining story elements, outlines, and validated AI images."""
    if len(image_paths) != 5:
        raise ValueError(f"Expected exactly 5 panel images, received {len(image_paths)}.")

    if len(story.panels) != 5:
        raise ValueError(f"Expected exactly 5 story panels, received {len(story.panels)}.")

    panels: List[ComicPanel] = []

    # Map outline by panel number for fast lookup
    outline_map = {p.panel_number: p for p in outline.panels}

    for idx, (panel_story, img_path) in enumerate(zip(story.panels, image_paths), start=1):
        # Strict validation of every panel image
        validate_image_file(img_path)

        outline_item = outline_map.get(idx)
        scene_desc = outline_item.scene_description if outline_item else panel_story.visual_description

        # Construct relative web-accessible URL
        rel_url = f"/static/panels/{img_path.name}"

        panel = ComicPanel(
            panel_number=idx,
            image_url=rel_url,
            image_path=str(img_path.resolve()),
            narration=panel_story.narration.strip(),
            dialogue=panel_story.dialogue.strip(),
            scene_description=scene_desc.strip(),
            art_style=user_input.art_style,
            mood=panel_story.mood.strip(),
            image_prompt=panel_story.image_prompt.strip(),
        )
        panels.append(panel)

    layout = ComicLayout(
        title=story.title or outline.title or f"{user_input.main_character}'s Adventure",
        prompt=user_input.prompt,
        main_character=user_input.main_character,
        setting=user_input.setting,
        tone=user_input.tone,
        art_style=user_input.art_style,
        panels=panels,
    )

    logger.info(f"Successfully constructed ComicLayout for '{layout.title}' with 5 panels.")
    return layout
