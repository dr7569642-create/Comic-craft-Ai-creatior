import logging
import socket
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Force IPv4 socket resolution on Windows to eliminate 20-30s IPv6 connect hangs
if sys.platform == "win32":
    try:
        _orig_getaddrinfo = socket.getaddrinfo

        def _ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
            return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

        socket.getaddrinfo = _ipv4_getaddrinfo
    except Exception:
        pass

from app.config import settings
from app.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title="ComicCraft — AI Comic Story Creator",
    description="Full-stack AI comic story creator generating genuine 5-panel illustrated stories using Google Gemini and fast, zero-token AI image generation.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Cross-Origin Resource Sharing (CORS) for decoupled cloud/frontend deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount media storage for generated panels and PDF exports
app.mount("/static/panels", StaticFiles(directory=str(settings.PANELS_DIR)), name="panels")
app.mount("/static/exports", StaticFiles(directory=str(settings.EXPORTS_DIR)), name="exports")

# Mount frontend styling and client-side logic
if (settings.FRONTEND_DIR / "css").exists():
    app.mount("/static/css", StaticFiles(directory=str(settings.FRONTEND_DIR / "css")), name="css")
if (settings.FRONTEND_DIR / "js").exists():
    app.mount("/static/js", StaticFiles(directory=str(settings.FRONTEND_DIR / "js")), name="js")

# General static mount fallback
if settings.FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(settings.FRONTEND_DIR)), name="static")

# Include application routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=(settings.ENVIRONMENT == "development"),
    )
