import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Environment & Server configuration (Any Cloud / Container / Localhost)
    ENVIRONMENT: str = "production"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    CORS_ORIGINS: list[str] = ["*"]

    # Google Gemini Models (for Outline & Story Scripting)
    GEMINI_API_KEY: str = ""
    GEMINI_OUTLINE_MODEL: str = "gemini-3.1-flash-lite"
    GEMINI_STORY_MODEL: str = "gemini-3.1-flash-lite"

    # Image Generation (No Hugging Face required!)
    # Options: "pollinations" (Free, FLUX/SDXL, no key needed), "imagen" (Google GenAI), "procedural" (Pillow Comic Engine)
    IMAGE_PROVIDER: str = "pollinations"
    IMAGE_MODEL: str = "flux"
    POLLINATIONS_BASE_URL: str = "https://image.pollinations.ai/prompt"

    # Directory Paths - Environment Agnostic
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    BACKEND_DIR: Path = Path(__file__).resolve().parent.parent

    # Storage paths (can be overridden via STORAGE_DIR env var for Docker volumes / persistent disks)
    STORAGE_DIR: Path = (
        Path(os.getenv("STORAGE_DIR"))
        if os.getenv("STORAGE_DIR")
        else (BACKEND_DIR / "storage")
    )
    PANELS_DIR: Path = STORAGE_DIR / "panels"
    EXPORTS_DIR: Path = STORAGE_DIR / "exports"

    # Frontend paths (supports unified deployment or decoupled static assets)
    FRONTEND_DIR: Path = (
        (BASE_DIR / "frontend")
        if (BASE_DIR / "frontend").exists()
        else (BACKEND_DIR / "frontend")
    )
    TEMPLATES_DIR: Path = (
        (FRONTEND_DIR / "templates")
        if (FRONTEND_DIR / "templates").exists()
        else FRONTEND_DIR
    )

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

# Ensure directories exist across all environments
settings.PANELS_DIR.mkdir(parents=True, exist_ok=True)
settings.EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
