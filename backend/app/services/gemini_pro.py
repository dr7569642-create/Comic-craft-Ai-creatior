import json
import logging
import re
from google import genai
from google.genai import types
from app.config import settings
from app.schemas import ComicOutline, ComicStory

logger = logging.getLogger(__name__)


def generate_story(
    outline: ComicOutline,
    prompt: str,
    main_character: str,
    setting: str,
    tone: str,
    art_style: str,
) -> ComicStory:
    """Generate detailed 5-panel comic story script and image prompts using Gemini."""
    if not settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY.strip():
        raise ValueError(
            "GEMINI_API_KEY is missing. Please set your Google Gemini API key in the .env file."
        )

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    system_instruction = (
        "You are an acclaimed comic book author, letterer, and storyboard artist. "
        "Expand the given 5-panel comic outline into full, immersive panel scripts and precise image generation prompts. "
        "Every panel must contain:\n"
        "- narration: punchy comic box narration text (1-3 sentences)\n"
        "- dialogue: character dialogue lines with speaker tags (e.g. Maya: 'Look out!') or inner thoughts\n"
        "- visual_description: vivid scene details for this specific frame\n"
        "- action: physical motion occurring in this frame\n"
        "- character_info: emotional state and physical posture of characters present\n"
        "- environment: background scenery, props, atmosphere\n"
        "- mood: emotional tone of this panel (e.g. tense, awe-inspired, triumphant)\n"
        "- image_prompt: an exceptionally high quality, detailed prompt for a text-to-image AI model. "
        "The image prompt MUST integrate:\n"
        "  1. The specified Art Style prominently\n"
        "  2. Consistent character appearance features (hair, outfit, distinctive traits)\n"
        "  3. Specific dynamic composition, camera angle, and dramatic comic book lighting\n"
        "  4. Environment and scenery details\n"
        "  5. Note: Avoid requesting text, speech bubbles, or watermark in the image itself."
    )

    outline_json = outline.model_dump_json(indent=2)
    user_content = (
        f"Original Prompt: {prompt}\n"
        f"Main Character: {main_character}\n"
        f"Setting: {setting}\n"
        f"Tone: {tone}\n"
        f"Art Style: {art_style}\n\n"
        f"Approved 5-Panel Outline & Character Appearance:\n{outline_json}\n\n"
        "Generate the complete 5-panel comic story and image prompts formatted strictly as the requested JSON schema."
    )

    candidate_models = [settings.GEMINI_STORY_MODEL, "gemini-3.1-flash-lite", "gemini-3.5-flash", "gemini-3.6-flash"]
    unique_candidates = list(dict.fromkeys([m for m in candidate_models if m]))

    last_error = None
    for model_name in unique_candidates:
        try:
            logger.info(f"Attempting story generation with model: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=user_content,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=ComicStory,
                    temperature=0.7,
                ),
            )

            if hasattr(response, "parsed") and response.parsed:
                if isinstance(response.parsed, ComicStory):
                    return response.parsed
                return ComicStory.model_validate(response.parsed)

            raw_text = response.text or ""
            cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text.strip(), flags=re.MULTILINE)
            cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)
            data = json.loads(cleaned)
            return ComicStory.model_validate(data)

        except Exception as exc:
            logger.warning(f"Model '{model_name}' failed: {exc}. Trying fallback...")
            last_error = exc

    raise RuntimeError(f"Gemini Story Generation Error: {str(last_error)}")
