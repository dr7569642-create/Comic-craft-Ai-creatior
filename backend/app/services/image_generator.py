import io
import logging
import math
import random
import socket
import sys
import urllib.parse
import uuid
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

# Conditional IPv4 socket resolution for Windows to eliminate IPv6 lookup delays
if sys.platform == "win32":
    try:
        _orig_getaddrinfo = socket.getaddrinfo

        def _ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
            return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

        socket.getaddrinfo = _ipv4_getaddrinfo
    except Exception:
        pass


def validate_image_file(image_path: Path) -> None:
    """Validate that the image file exists, is not empty, and is a valid readable image."""
    if not image_path.exists():
        raise FileNotFoundError(f"Image file does not exist at {image_path}")

    file_size = image_path.stat().st_size
    if file_size == 0:
        raise ValueError(f"Image file at {image_path} is empty (0 bytes).")

    try:
        with Image.open(image_path) as img:
            img.verify()
    except Exception as exc:
        raise ValueError(f"Image file at {image_path} is corrupted or invalid format: {exc}") from exc


def generate_procedural_comic_panel(
    prompt: str, output_path: Path, panel_index: int | None = None
) -> Path:
    """Generate a stylized comic book illustration using Pillow.
    Ensures 100% offline/air-gapped reliability in any environment without external APIs.
    """
    width, height = 768, 768
    panel_idx = panel_index or 1

    # Narrative mood palette per panel index
    palettes = {
        1: ((20, 24, 48), (59, 130, 246), "#60a5fa", "ESTABLISHING SHOT"),
        2: ((30, 20, 45), (168, 85, 247), "#c084fc", "INCITING BEAT"),
        3: ((45, 20, 20), (239, 68, 68), "#f87171", "RISING CONFLICT"),
        4: ((50, 30, 10), (249, 115, 22), "#fb923c", "CLIMACTIC PEAK"),
        5: ((15, 35, 25), (16, 185, 129), "#34d399", "RESOLUTION"),
    }
    bg_dark, bg_accent, glow_hex, beat_name = palettes.get(
        panel_idx, ((25, 25, 35), (99, 102, 241), "#818cf8", "COMIC SCENE")
    )

    # 1. Base gradient
    img = Image.new("RGB", (width, height), color=bg_dark)
    draw = ImageDraw.Draw(img)

    for y in range(height):
        ratio = y / height
        r = int(bg_dark[0] * (1 - ratio) + bg_accent[0] * ratio)
        g = int(bg_dark[1] * (1 - ratio) + bg_accent[1] * ratio)
        b = int(bg_dark[2] * (1 - ratio) + bg_accent[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 2. Dynamic Comic Action Burst / Rays
    center_x, center_y = width // 2, height // 2
    num_rays = 24
    for i in range(num_rays):
        angle = (2 * math.pi / num_rays) * i
        ray_x = center_x + int(math.cos(angle) * width)
        ray_y = center_y + int(math.sin(angle) * height)
        draw.polygon(
            [
                (center_x, center_y),
                (ray_x, ray_y),
                (center_x + int(math.cos(angle + 0.08) * width), center_y + int(math.sin(angle + 0.08) * height)),
            ],
            fill=(255, 255, 255, 20),
        )

    # 3. Comic Halftone Dots
    for x in range(30, width - 30, 24):
        for y in range(30, height - 30, 24):
            dist = math.hypot(x - center_x, y - center_y)
            dot_rad = max(1, int(4 * (1 - dist / (width * 0.7))))
            if dot_rad > 0:
                draw.ellipse(
                    [(x - dot_rad, y - dot_rad), (x + dot_rad, y + dot_rad)],
                    fill=(255, 255, 255),
                )

    # 4. Comic Book Action Silhouette / Focus Frame
    inner_margin = 40
    draw.rectangle(
        [(inner_margin, inner_margin), (width - inner_margin, height - inner_margin)],
        outline="#ffffff",
        width=5,
    )
    draw.rectangle(
        [(inner_margin + 6, inner_margin + 6), (width - inner_margin - 6, height - inner_margin - 6)],
        outline=glow_hex,
        width=2,
    )

    # 5. Dramatic Center Comic Focus Shield
    shield_rad = 180
    draw.ellipse(
        [(center_x - shield_rad, center_y - shield_rad), (center_x + shield_rad, center_y + shield_rad)],
        outline="#ffffff",
        width=4,
    )
    draw.ellipse(
        [(center_x - shield_rad + 8, center_y - shield_rad + 8), (center_x + shield_rad - 8, center_y + shield_rad - 8)],
        outline=glow_hex,
        width=3,
    )

    # Comic Hero Emblem Silhouette
    draw.polygon(
        [
            (center_x, center_y - 100),
            (center_x + 90, center_y - 10),
            (center_x + 50, center_y + 100),
            (center_x - 50, center_y + 100),
            (center_x - 90, center_y - 10),
        ],
        fill=(15, 18, 25),
        outline="#ffffff",
    )

    # Star glyph inside emblem
    star_points = []
    for step in range(10):
        r = 55 if step % 2 == 0 else 25
        ang = step * math.pi / 5 - math.pi / 2
        star_points.append((center_x + int(r * math.cos(ang)), center_y + 5 + int(r * math.sin(ang))))
    draw.polygon(star_points, fill=glow_hex, outline="#ffffff")

    # 6. Comic Panel Tag & Beat Header Banner
    draw.rectangle([(55, 55), (340, 105)], fill="#0f172a", outline="#ffffff", width=2)
    draw.rectangle([(60, 60), (335, 100)], fill="#ff4b2b")
    draw.text((75, 68), f"PANEL {panel_idx}  •  {beat_name}", fill="#ffffff")

    # 7. Comic Narration Box at Bottom
    clean_snippet = prompt.replace("\n", " ").strip()
    if len(clean_snippet) > 85:
        clean_snippet = clean_snippet[:82] + "..."
    draw.rectangle([(55, height - 125), (width - 55, height - 55)], fill="#0f172a", outline="#ffffff", width=2)
    draw.rectangle([(60, height - 120), (width - 60, height - 60)], fill="#fef08a")
    draw.text((75, height - 108), f"SCENE: {clean_snippet}", fill="#1e293b")

    img.save(output_path, format="PNG")
    validate_image_file(output_path)
    logger.info(f"Generated procedural comic panel: {output_path.name}")
    return output_path


def generate_image_pollinations(prompt: str, output_path: Path) -> Path:
    """Generate high-quality AI art using Pollinations AI (FLUX model, zero API keys required)."""
    # Clean and encode prompt
    safe_prompt = prompt.replace("\n", " ").strip()[:500]
    encoded_prompt = urllib.parse.quote(safe_prompt)

    url = (
        f"{settings.POLLINATIONS_BASE_URL}/{encoded_prompt}"
        f"?width=768&height=768&nologo=true"
    )

    logger.info(f"Calling Pollinations AI for: {safe_prompt[:60]}...")

    headers = {
        "User-Agent": "ComicCraft/2.0 (AI Comic Creator; environment-agnostic)"
    }

    with httpx.Client(timeout=15.0, follow_redirects=True) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()

        # Parse raw image bytes via PIL
        img = Image.open(io.BytesIO(response.content))
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output_path, format="PNG")

    validate_image_file(output_path)
    logger.info(f"Successfully generated Pollinations AI image: {output_path.name}")
    return output_path


def generate_image_imagen(prompt: str, output_path: Path) -> Path:
    """Generate AI art via Google Imagen (imagen-3.0-generate-002) using GEMINI_API_KEY."""
    if not settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY.strip():
        raise ValueError("GEMINI_API_KEY is not configured for Google Imagen.")

    from google import genai

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    logger.info(f"Calling Google Imagen for prompt: {prompt[:60]}...")

    result = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=prompt,
        config=dict(
            number_of_images=1,
            aspect_ratio="1:1",
            output_mime_type="image/png",
        ),
    )

    if not result.generated_images:
        raise RuntimeError("No image was returned from Google Imagen.")

    image_bytes = result.generated_images[0].image.image_bytes
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(output_path, format="PNG")

    validate_image_file(output_path)
    return output_path


def generate_image(
    prompt: str, output_path: Path | None = None, panel_index: int | None = None
) -> Path:
    """Master AI image generation function.
    Multi-provider support:
    1. Pollinations AI (FLUX/Turbo - free, public, no API tokens needed)
    2. Google Imagen (via GEMINI_API_KEY if configured)
    3. Procedural Comic Art Engine (Pillow - 100% offline-ready fallback)

    Ensures zero dependency on Hugging Face API and works in ANY environment.
    """
    if output_path is None:
        unique_id = uuid.uuid4().hex[:8]
        prefix = f"panel_{panel_index}_" if panel_index is not None else "test_"
        filename = f"{prefix}{unique_id}.png"
        output_path = settings.PANELS_DIR / filename

    output_path.parent.mkdir(parents=True, exist_ok=True)

    provider = settings.IMAGE_PROVIDER.lower().strip()

    # 1. If explicit procedural requested
    if provider == "procedural":
        return generate_procedural_comic_panel(prompt, output_path, panel_index)

    # 2. If Google Imagen requested
    if provider == "imagen":
        try:
            return generate_image_imagen(prompt, output_path)
        except Exception as exc:
            logger.warning(f"Google Imagen failed: {exc}. Trying Pollinations AI fallback...")

    # 3. Primary AI Generator: Pollinations AI (FLUX)
    try:
        return generate_image_pollinations(prompt, output_path)
    except Exception as exc:
        logger.warning(
            f"Pollinations AI image generation failed: {exc}. "
            "Falling back to high-resolution procedural comic engine..."
        )

    # 4. Failsafe: Procedural Comic Panel Generator
    try:
        return generate_procedural_comic_panel(prompt, output_path, panel_index)
    except Exception as fallback_exc:
        logger.error(f"Procedural comic generation failed: {fallback_exc}", exc_info=True)
        if output_path.exists():
            try:
                output_path.unlink()
            except OSError:
                pass
        raise RuntimeError(f"All image generation methods failed: {fallback_exc}") from fallback_exc
