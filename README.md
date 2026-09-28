# ComicCraft — AI Comic Story Creator (v2.0)

**ComicCraft** is an environment-agnostic, full-stack generative AI application that turns story premises into complete, 5-panel illustrated comic books. Every comic panel features genuine AI-generated artwork (powered by **Pollinations AI FLUX**, **Google Imagen**, or the offline **Comic Engine**) with cinematic narrative captions and speech bubble dialogues scripted by **Google Gemini AI**. Finished comics can be previewed interactively or exported as print-ready, high-resolution PDF editions.

---

## ⚡ Key Highlights in v2.0

- **Decoupled Architecture:** Cleanly organized into `frontend/` and `backend/` directories.
- **Zero Hugging Face Dependency:** No Hugging Face API tokens required, eliminating monthly credit depletion (HTTP 402) errors.
- **Multi-Provider AI Image Engine:**
  - **Pollinations AI (FLUX / Turbo):** Ultra-fast, high-resolution, free public diffusion engine with zero API key requirement.
  - **Google Imagen:** Native Google GenAI image generation via your existing `GEMINI_API_KEY`.
  - **Procedural Comic Engine (Pillow Fallback):** Ensures 100% reliability in offline, air-gapped, or restricted network environments.
- **Deploy Anywhere:**
  - Works on **Localhost**, **Docker**, **Docker Compose**, **Kubernetes**, **Render**, **Railway**, **Google Cloud Run**, **AWS ECS**, **Fly.io**, and **Heroku**.
  - Automatically binds to `$PORT` and `$HOST` across cloud platforms.
  - Cross-platform support for Windows, Linux, and macOS.
- **Interactive Studio UI & REST API:** Complete web interface with live diagnostics, story presets, and OpenAPI Swagger documentation at `/docs`.

---

## 📂 Project Architecture

```
comic craft app/
├── backend/
│   ├── app/
│   │   ├── config.py             # Dynamic environment & path configuration
│   │   ├── main.py               # FastAPI entrypoint, CORS & static mounts
│   │   ├── routes.py             # Web & REST API routes (/generate, /health, etc.)
│   │   ├── schemas.py            # Pydantic data schemas
│   │   └── services/
│   │       ├── comic_pipeline.py # End-to-end comic generation pipeline
│   │       ├── image_generator.py# Zero-token AI image engine (Pollinations/Imagen/Pillow)
│   │       ├── gemini_flash.py   # 5-panel outline & visual character consistency
│   │       ├── gemini_pro.py     # Dialogue & narrative prompt scriptwriting
│   │       ├── layout_builder.py # Panel validation and comic layout construction
│   │       └── exporters.py      # High-resolution PDF compiler (fpdf2)
│   ├── storage/                  # Persistent storage for panels and PDF exports
│   │   ├── panels/
│   │   └── exports/
│   ├── tests/                    # Comprehensive automated test suite (pytest)
│   ├── requirements.txt          # Backend dependencies (no huggingface_hub!)
│   ├── Dockerfile                # Production backend container
│   └── pytest.ini
│
├── frontend/
│   ├── templates/                # Responsive comic studio templates (Jinja2 / HTML)
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── comic_preview.html
│   │   └── export_success.html
│   ├── css/
│   │   └── style.css             # Comic-book design system with halftone aesthetics
│   ├── js/
│   │   └── app.js                # Form handling, diagnostics & multi-stage loader
│   ├── nginx.conf                # Nginx reverse proxy configuration
│   └── Dockerfile                # Standalone frontend static container
│
├── docker-compose.yml            # 1-click orchestration for any environment
├── Dockerfile                    # Universal root container for cloud PaaS
├── run_local.ps1                 # 1-click Windows localhost runner
├── run_local.sh                  # 1-click Linux/macOS localhost runner
├── .env                          # Local environment variables
├── .env.example                  # Example template
└── pytest.ini                    # Root test runner config
```

---

## 🚀 Running on Localhost

### Prerequisites
- Python 3.10+
- Google Gemini API Key ([Google AI Studio](https://aistudio.google.com/))

### Windows (PowerShell)
```powershell
# 1. Clone repository and navigate to folder
cd "e:\comic craft app"

# 2. Configure .env file with your GEMINI_API_KEY
# (No HF_TOKEN needed!)

# 3. Launch with 1-click script
.\run_local.ps1
```

### Linux / macOS
```bash
chmod +x run_local.sh
./run_local.sh
```

### Manual Command
```bash
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Visit **http://localhost:8000** in your browser!

---

## 🐳 Deploying with Docker

### Using Docker Compose (Recommended)
```bash
docker-compose up --build
```
This builds and starts the ComicCraft service with persistent storage mounted at `./backend/storage`. Access at **http://localhost:8000**.

### Single Container Build & Run
```bash
docker build -t comiccraft .
docker run -p 8000:8000 --env-file .env comiccraft
```

---

## ☁️ Deploying to Any Cloud Environment

### 1. Render / Railway / Fly.io
- Simply connect your Git repository.
- Use Docker buildpack (the root [Dockerfile](file:///e:/comic%20craft%20app/Dockerfile) will be detected automatically).
- Set Environment Variables in dashboard:
  - `GEMINI_API_KEY`: your Google Gemini API key
  - `PORT`: provided automatically by the cloud platform

### 2. Google Cloud Run
```bash
gcloud run deploy comiccraft \
  --source . \
  --port 8000 \
  --set-env-vars GEMINI_API_KEY=your_key_here \
  --allow-unauthenticated
```

### 3. AWS App Runner / ECS
- Push image to AWS ECR.
- Deploy container pointing to port `8000`.

---

## 🧪 Automated Testing

Run the full automated test suite (12 tests) covering API endpoints, input validation, diagnostics, layout builder, PDF export, and static pages:

```bash
# From project root
python -m pytest

# Or from backend directory
cd backend && pytest
```

---

## 📋 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web Studio homepage |
| `POST` | `/generate` | Web form submission returning rendered preview page |
| `POST` | `/generate-comic/json` | REST API returning full comic JSON with panel data & PDF URL |
| `POST` | `/test-image` | Diagnostics endpoint testing AI image generation engine |
| `GET` | `/health` / `/api/health` | Health check returning status, version, and environment |
| `GET` | `/docs` | Interactive Swagger API documentation |
