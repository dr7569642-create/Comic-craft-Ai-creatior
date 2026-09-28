import json
import logging
import re
from google import genai
from google.genai import types
from app.config import settings
from app.schemas import ComicOutline

logger = logging.getLogger(__name__)


def generate_outline(prompt: str, main_character: str, setting: str, tone: str, art_style: str) -> ComicOutline:
    """Generate a structured 5-panel comic outline using Google Gemini."""
    if not settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY.strip():
        raise ValueError(
            "GEMINI_API_KEY is missing. Please set your Google Gemini API key in the .env file."
        )

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    system_instruction = (
        "You are a master comic book writer and visual director. "
        "Create a coherent, compelling 5-panel comic outline based on the user's premise. "
        "The outline must have EXACTLY 5 panels following this classical narrative arc:\n"
        "- Panel 1: Introduction and setup (establish the main character and world)\n"
        "- Panel 2: Development or sudden discovery (catalyst for action)\n"
        "- Panel 3: Conflict, rising tension or obstacle\n"
        "- Panel 4: Climax or peak dramatic/action moment\n"
        "- Panel 5: Resolution and aftermath\n\n"
        "Crucial Requirement: Define a detailed 'character_appearance' that describes the main character's "
        "physical traits, distinctive clothing, hair, colors, and accessories so they can be drawn consistently "
        "across all five panels."
    )

    user_content = (
        f"Story Premise: {prompt}\n"
        f"Main Character: {main_character}\n"
        f"Setting / Environment: {setting}\n"
        f"Tone: {tone}\n"
        f"Art Style: {art_style}\n\n"
        "Generate a complete 5-panel outline formatted strictly as the requested JSON schema."
    )

    # Candidate models in order of preference, with active fallback
    candidate_models = [settings.GEMINI_OUTLINE_MODEL, "gemini-3.1-flash-lite", "gemini-3.5-flash", "gemini-3.6-flash"]
    unique_candidates = list(dict.fromkeys([m for m in candidate_models if m]))

    last_error = None
    for model_name in unique_candidates:
        try:
            logger.info(f"Attempting outline generation with model: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=user_content,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=ComicOutline,
                    temperature=0.7,
                ),
            )

            if hasattr(response, "parsed") and response.parsed:
                if isinstance(response.parsed, ComicOutline):
                    return response.parsed
                return ComicOutline.model_validate(response.parsed)

            raw_text = response.text or ""
            cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text.strip(), flags=re.MULTILINE)
            cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)
            data = json.loads(cleaned)
            return ComicOutline.model_validate(data)

        except Exception as exc:
            logger.warning(f"Model '{model_name}' failed: {exc}. Trying fallback...")
            last_error = exc

    raise RuntimeError(f"Gemini Outline Generation Error: {str(last_error)}")
