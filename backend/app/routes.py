import logging
from pathlib import Path
from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.schemas import (
    ComicCreateRequest,
    ComicResponse,
    HealthResponse,
    ImageTestRequest,
    ImageTestResponse,
)
from app.services.comic_pipeline import generate_complete_comic
from app.services.image_generator import generate_image

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


@router.get("/health", response_model=HealthResponse, tags=["System"])
@router.get("/api/health", response_model=HealthResponse, tags=["System"])
def get_health():
    """Health check endpoint confirming ComicCraft service status across any environment."""
    return HealthResponse(
        status="ok",
        service="ComicCraft",
        version="2.0.0",
        environment=settings.ENVIRONMENT,
        image_provider=settings.IMAGE_PROVIDER,
    )


@router.get("/", response_class=HTMLResponse, tags=["Web Pages"])
def get_homepage(request: Request):
    """Render the ComicCraft creator studio homepage."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "has_gemini_key": bool(settings.GEMINI_API_KEY.strip()),
            "image_provider": settings.IMAGE_PROVIDER,
        },
    )


@router.post("/generate", response_class=HTMLResponse, tags=["Web Pages"])
def generate_comic_form(
    request: Request,
    prompt: str = Form(...),
    main_character: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    """Process web form submission and render comic_preview.html with real generated AI images."""
    try:
        req = ComicCreateRequest(
            prompt=prompt,
            main_character=main_character,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
    except Exception as validation_err:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": f"Validation Error: {validation_err}",
                "form_data": {
                    "prompt": prompt,
                    "main_character": main_character,
                    "setting": setting,
                    "tone": tone,
                    "art_style": art_style,
                },
                "has_gemini_key": bool(settings.GEMINI_API_KEY.strip()),
                "image_provider": settings.IMAGE_PROVIDER,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:
        layout = generate_complete_comic(req)
        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "comic": layout,
            },
        )
    except Exception as exc:
        logger.error(f"Error during comic generation: {exc}", exc_info=True)
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(exc),
                "form_data": {
                    "prompt": prompt,
                    "main_character": main_character,
                    "setting": setting,
                    "tone": tone,
                    "art_style": art_style,
                },
                "has_gemini_key": bool(settings.GEMINI_API_KEY.strip()),
                "image_provider": settings.IMAGE_PROVIDER,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/generate-comic/json", response_model=ComicResponse, tags=["API"])
def generate_comic_json(req: ComicCreateRequest):
    """Generate complete 5-panel comic with real AI images and return JSON representation."""
    try:
        layout = generate_complete_comic(req)
        return ComicResponse(
            success=True,
            title=layout.title,
            main_character=layout.main_character,
            setting=layout.setting,
            tone=layout.tone,
            art_style=layout.art_style,
            panels=layout.panels,
            pdf_url=layout.pdf_url or "",
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as exc:
        logger.error(f"API Comic Generation Error: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comic Generation Failed: {str(exc)}",
        )


@router.post("/test-image", response_model=ImageTestResponse, tags=["Testing & Diagnostics"])
def test_image_generation(req: ImageTestRequest = ImageTestRequest()):
    """Generate a single test AI image via Pollinations/Imagen/Pillow to verify image generation."""
    prompt = req.prompt or "A bold comic book hero in dynamic action pose, vivid colors, graphic novel style"
    try:
        img_path = generate_image(prompt=prompt)
        rel_url = f"/static/panels/{img_path.name}"
        return ImageTestResponse(
            success=True,
            image_url=rel_url,
            message="Test image successfully generated and verified via AI image engine.",
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as exc:
        logger.error(f"Image generation diagnostic failed: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image generation failed: {str(exc)}",
        )


@router.get("/export-success", response_class=HTMLResponse, tags=["Web Pages"])
def export_success_page(request: Request, pdf_url: str = "", title: str = "Your Comic"):
    """Render export completion page with download link and new comic action."""
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "pdf_url": pdf_url,
            "title": title,
        },
    )
