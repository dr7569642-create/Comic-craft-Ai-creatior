import concurrent.futures
import logging
from pathlib import Path
from typing import List
from app.config import settings
from app.schemas import ComicCreateRequest, ComicLayout
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf

logger = logging.getLogger(__name__)


def generate_complete_comic(request: ComicCreateRequest) -> ComicLayout:
    """Execute the end-to-end comic generation pipeline using Gemini AI and fast AI image generation.

    Pipeline Steps:
    1. Input validation (handled by Pydantic)
    2. 5-panel outline generation via Gemini Flash
    3. Full story, dialogue, and prompt scripting via Gemini Pro
    4. Real AI image generation for Panels 1-5 via parallel execution (Pollinations FLUX / Imagen / Comic Engine)
    5. Assembly and image validation in Layout Builder
    6. PDF generation and export
    7. Return completed ComicLayout
    """
    logger.info(f"Starting comic generation for: '{request.prompt[:60]}...'")

    # Step 1: Check environment credentials early
    if not settings.GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is not set. Please provide your Google Gemini API key in the .env file."
        )

    # Step 2: Generate 5-Panel Outline with Gemini Flash (~1.5s)
    logger.info("Step 1/5: Generating 5-panel outline with Gemini Flash...")
    outline = generate_outline(
        prompt=request.prompt,
        main_character=request.main_character,
        setting=request.setting,
        tone=request.tone,
        art_style=request.art_style,
    )

    # Step 3: Generate Detailed Script and Prompts with Gemini Pro (~2s)
    logger.info("Step 2/5: Generating story script and visual prompts with Gemini Pro...")
    story = generate_story(
        outline=outline,
        prompt=request.prompt,
        main_character=request.main_character,
        setting=request.setting,
        tone=request.tone,
        art_style=request.art_style,
    )

    # Step 4: Generate 5 Real AI Images concurrently in parallel
    logger.info("Step 3/5: Generating 5 AI panel illustrations concurrently...")

    def _generate_single_panel(idx_and_panel):
        idx, panel_story = idx_and_panel
        # Gentle stagger to avoid burst rate limits on public image APIs
        if idx > 1:
            import time
            time.sleep(0.7 * (idx - 1))

        logger.info(f"Dispatching artwork generation for Panel {idx}/5...")
        full_image_prompt = (
            f"{panel_story.image_prompt}, "
            f"in {request.art_style} style, "
            f"featuring {outline.character_appearance}, "
            f"cinematic comic panel composition, highly detailed, dramatic lighting"
        )
        img_path = generate_image(
            prompt=full_image_prompt,
            panel_index=idx,
        )
        return idx, img_path

    # Use ThreadPoolExecutor to run panel generations with gentle concurrency
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(_generate_single_panel, (idx, panel_story))
            for idx, panel_story in enumerate(story.panels, start=1)
        ]
        results = [f.result() for f in futures]

    # Ensure panels are ordered 1 to 5
    results.sort(key=lambda x: x[0])
    image_paths: List[Path] = [path for _, path in results]

    # Step 5: Build Comic Layout
    logger.info("Step 4/5: Building and validating comic layout...")
    layout = build_comic_layout(
        story=story,
        outline=outline,
        image_paths=image_paths,
        user_input=request,
    )

    # Step 6: Export to PDF
    logger.info("Step 5/5: Exporting high-resolution comic PDF...")
    pdf_path, download_url = save_pdf(layout)
    layout.pdf_path = str(pdf_path.resolve())
    layout.pdf_url = download_url

    logger.info("ComicCraft generation pipeline successfully completed!")
    return layout
