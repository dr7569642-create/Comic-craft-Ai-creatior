from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class ComicCreateRequest(BaseModel):
    prompt: str = Field(..., min_length=3, description="Story prompt or premise")
    main_character: str = Field(..., min_length=1, description="Main character name and brief info")
    setting: str = Field(..., min_length=1, description="Setting or location")
    tone: str = Field(..., min_length=1, description="Story tone (e.g., Adventure, Dark, Humorous)")
    art_style: str = Field(..., min_length=1, description="Visual art style (e.g., Comic Book, Manga, Watercolor)")

    @field_validator("prompt", "main_character", "setting", "tone", "art_style")
    @classmethod
    def not_empty_after_strip(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Field cannot be empty or whitespace only")
        return stripped


class PanelOutline(BaseModel):
    panel_number: int = Field(..., ge=1, le=5)
    scene_description: str
    action: str
    characters: str
    location: str
    visual_direction: str
    emotional_beat: str
    suggested_dialogue: str


class ComicOutline(BaseModel):
    title: str
    character_appearance: str = Field(..., description="Consistent visual description of main character (clothing, hair, facial features)")
    panels: List[PanelOutline] = Field(..., min_length=5, max_length=5)


class PanelStory(BaseModel):
    panel_number: int = Field(..., ge=1, le=5)
    narration: str
    dialogue: str
    visual_description: str
    action: str
    character_info: str
    environment: str
    mood: str
    image_prompt: str


class ComicStory(BaseModel):
    title: str
    panels: List[PanelStory] = Field(..., min_length=5, max_length=5)


class ComicPanel(BaseModel):
    panel_number: int
    image_url: str
    image_path: str
    narration: str
    dialogue: str
    scene_description: str
    art_style: str
    mood: str = ""
    image_prompt: str = ""


class ComicLayout(BaseModel):
    title: str
    prompt: str
    main_character: str
    setting: str
    tone: str
    art_style: str
    panels: List[ComicPanel]
    pdf_url: Optional[str] = None
    pdf_path: Optional[str] = None


class ComicResponse(BaseModel):
    success: bool = True
    title: str
    main_character: str
    setting: str
    tone: str
    art_style: str
    panels: List[ComicPanel]
    pdf_url: str


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "ComicCraft"
    version: Optional[str] = "2.0.0"
    environment: Optional[str] = "production"
    image_provider: Optional[str] = "pollinations"


class ImageTestRequest(BaseModel):
    prompt: Optional[str] = "A brave robotic explorer standing on a neon-lit cyberpunk rooftop at dusk, comic book art style"


class ImageTestResponse(BaseModel):
    success: bool
    image_url: str
    message: str = "Image generated successfully"
