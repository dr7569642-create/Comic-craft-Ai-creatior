# MASTER PROMPT — BUILD COMICCRAFT FROM SCRATCH
# REAL AI VERSION — NO DEMO MODE

Act as an expert full-stack Python, FastAPI, Generative AI and UI developer.

Build the complete project called:

COMICCRAFT — AI COMIC STORY CREATOR

Build everything directly in the current workspace.

IMPORTANT:
- Do NOT create a demo-only application.
- Do NOT create placeholder comic images.
- Do NOT use fake image generation.
- Do NOT use Demo Mode.
- The application must use REAL Gemini AI for story generation.
- The application must use REAL AI image generation for every comic panel.
- The final result must display actual AI-generated images.
- The application must export the actual generated images into a PDF.
- Create all required files completely.
- Install dependencies.
- Run tests.
- Start the application.
- Fix errors before finishing.
- Do not merely explain the code.

==================================================
1. PROJECT PURPOSE
==================================================

ComicCraft is an AI-powered web application that allows a user to enter:

1. Story prompt
2. Main character
3. Setting
4. Tone
5. Art style

The system must then:

User Input
    ↓
Gemini generates 5-panel outline
    ↓
Gemini generates narration/dialogue/visual descriptions
    ↓
AI image generator creates 5 actual illustrations
    ↓
Comic layout is created
    ↓
Comic is displayed in browser
    ↓
User can export the comic as PDF

The final comic must contain EXACTLY 5 panels.

==================================================
2. TECHNOLOGY STACK
==================================================

Use:

Backend:
- Python
- FastAPI
- Uvicorn
- Pydantic
- Pydantic Settings
- Jinja2

Frontend:
- HTML
- CSS
- JavaScript
- Jinja2 templates

AI:
- Google GenAI SDK (`google-genai`)
- Gemini models for story generation
- Hugging Face InferenceClient for image generation

Images:
- Pillow where needed for image handling

PDF:
- fpdf2

Testing:
- pytest
- httpx

Environment:
- python-dotenv
- .env

DO NOT use the obsolete `google-generativeai` package.

==================================================
3. REAL AI ONLY
==================================================

There must be NO:

- DEMO_MODE
- fake images
- placeholder images
- gradient-only panel images
- scene-description cards pretending to be images
- hard-coded sample comic images
- local fake image generation as the final output

Every generated panel must contain a REAL AI-generated image.

If an API fails, show the actual error and handle it properly.

Do NOT silently replace a failed AI image with a fake image.

==================================================
4. PROJECT STRUCTURE
==================================================

Create:

ComicCraft/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── routes.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── comic_pipeline.py
│       ├── gemini_flash.py
│       ├── gemini_pro.py
│       ├── image_generator.py
│       ├── layout_builder.py
│       └── exporters.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   ├── panels/
│   └── exports/
│
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_api.py
│   ├── test_pages.py
│   └── test_layout_export.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

==================================================
5. ENVIRONMENT CONFIGURATION
==================================================

Create `.env.example`:

GEMINI_API_KEY=
HF_TOKEN=

GEMINI_OUTLINE_MODEL=gemini-2.5-flash
GEMINI_STORY_MODEL=gemini-2.5-pro

IMAGE_MODEL=stabilityai/stable-diffusion-xl-base-1.0

Create configuration using Pydantic Settings.

The real `.env` must NOT be committed to Git.

Never hard-code API keys.

Never expose API keys in HTML, JSON responses, browser console or frontend JavaScript.

==================================================
6. GEMINI OUTLINE GENERATION
==================================================

Create:

app/services/gemini_flash.py

Implement:

generate_outline()

Use the modern Google GenAI SDK:

from google import genai

The outline generator must produce exactly 5 panels.

For each panel generate:

- panel number
- scene description
- action
- characters
- location/environment
- visual direction
- emotional beat
- suggested dialogue/action

The five panels must form one coherent story.

The story must have:

Panel 1:
Introduction/setup

Panel 2:
Development/discovery

Panel 3:
Conflict

Panel 4:
Climax/action

Panel 5:
Resolution

These are structural guidelines, not hard-coded story content.

The actual story must be based on the user's prompt.

Use structured Pydantic output where supported.

==================================================
7. GEMINI STORY GENERATION
==================================================

Create:

app/services/gemini_pro.py

Implement:

generate_story()

Generate the complete story content for the five panels.

Each panel must contain:

- narration
- dialogue
- visual description
- action
- character information
- environment
- mood
- image-generation prompt

Maintain continuity between panels.

The same main character must remain visually consistent.

Do not randomly change:

- character identity
- clothing
- major appearance
- setting
- story tone

unless the story itself requires it.

==================================================
8. IMAGE GENERATION
==================================================

Create:

app/services/image_generator.py

Implement:

generate_image()

Use:

from huggingface_hub import InferenceClient

Use:

InferenceClient.text_to_image()

Use:

HF_TOKEN

Use the configured:

IMAGE_MODEL

Every panel must trigger an actual image-generation request.

Generate exactly 5 images.

Save each generated image under:

static/panels/

Use unique filenames.

Example:

panel_1_<unique>.png
panel_2_<unique>.png
panel_3_<unique>.png
panel_4_<unique>.png
panel_5_<unique>.png

The generated images must be real image files.

Do NOT create fake images.

Do NOT replace the image with text.

Do NOT create colored placeholders.

==================================================
9. IMAGE PROMPT QUALITY
==================================================

The image prompt must be generated from the panel story.

Every image prompt should include:

- main character
- character appearance
- character action
- environment
- important objects
- camera/framing
- lighting
- mood
- tone
- art style
- cinematic/comic composition
- continuity information

The user's selected art style must strongly influence the image.

Examples:

Comic Book
Graphic Novel
Anime
Manga
Watercolor
Fantasy Illustration
Cinematic
Cartoon

The system should pass the selected art style into every image-generation prompt.

==================================================
10. CHARACTER CONSISTENCY
==================================================

Character consistency is very important.

Use the same character description across all five image prompts.

If the user enters:

Main Character:
Maya

then all five images should depict the same Maya.

Store a consistent character description and append it to every panel image prompt.

Do not generate five unrelated characters.

==================================================
11. COMIC PIPELINE
==================================================

Create:

app/services/comic_pipeline.py

The pipeline must be:

1. Validate user input.
2. Generate 5-panel outline using Gemini.
3. Generate detailed story using Gemini.
4. Build 5 image prompts.
5. Generate image 1.
6. Generate image 2.
7. Generate image 3.
8. Generate image 4.
9. Generate image 5.
10. Build comic layout.
11. Make PDF.
12. Return the completed comic.

If any AI generation fails:

- stop the generation gracefully
- return a useful error
- do not silently use fake content

==================================================
12. COMIC LAYOUT
==================================================

Create:

app/services/layout_builder.py

Implement:

build_comic_layout()

Each comic panel must contain:

- panel number
- actual generated image
- narration
- dialogue
- scene description
- art style
- story metadata

The actual image must be the main visual element.

The scene description must NOT replace the image.

==================================================
13. FRONTEND DESIGN
==================================================

Create a polished comic-themed responsive UI.

The homepage must include:

COMICCRAFT

"AI Comic Story Creator"

Input fields:

Story Prompt
Main Character
Setting
Tone
Art Style

Add:

Generate Comic button

Show loading status while AI generation is running.

Show meaningful error messages.

Use a modern comic-book visual design.

Use:

- comic-style cards
- speech bubbles where appropriate
- panel borders
- responsive layout
- attractive typography
- clear buttons
- mobile-friendly layout

==================================================
14. COMIC PREVIEW
==================================================

comic_preview.html must display exactly 5 panels.

Each panel should look approximately like:

--------------------------------
PANEL 1

[ LARGE REAL AI-GENERATED IMAGE ]

Narration:
...

Dialogue:
"..."

--------------------------------

The image should occupy approximately 60–70% of the visual panel.

The text should be underneath or integrated as comic-style text.

Do NOT make the scene description the main visual.

The actual generated image must be clearly visible.

==================================================
15. PANEL IMAGE VALIDATION
==================================================

Before returning the completed comic, verify:

- image file exists
- image file is not empty
- image has valid image format
- image can be opened
- image URL/path exists
- browser can access the image

If an image fails:

return an error.

Do not create a placeholder.

==================================================
16. API ROUTES
==================================================

Implement:

GET /

POST /generate

POST /generate-comic/json

POST /test-image

GET /export-success

GET /health

Mount:

/static

Enable FastAPI documentation:

/docs

==================================================
17. HEALTH ENDPOINT
==================================================

GET /health must return:

{
    "status": "ok",
    "service": "ComicCraft"
}

==================================================
18. JSON API
==================================================

POST /generate-comic/json

Accept:

{
    "prompt": "A young inventor discovers a mysterious robot.",
    "main_character": "Maya",
    "setting": "A futuristic city",
    "tone": "Adventure",
    "art_style": "Comic book"
}

Return:

- success status
- comic title
- five panels
- image URLs
- narration
- dialogue
- PDF URL

==================================================
19. INPUT VALIDATION
==================================================

Use Pydantic.

Reject empty:

- prompt
- main character
- setting
- tone
- art style

Return clean validation errors.

==================================================
20. PDF EXPORT
==================================================

Create:

app/services/exporters.py

Implement:

save_pdf()

Use fpdf2.

The PDF must contain:

- comic title
- all 5 actual AI-generated images
- panel numbers
- narration
- dialogue

Use the REAL generated image files.

Do not put placeholder graphics into the PDF.

Save under:

static/exports/

Return a usable download URL.

==================================================
21. PDF LAYOUT
==================================================

Make the PDF readable and professional.

Possible layout:

Page 1:
Comic title + Panel 1

Page 2:
Panel 2

Page 3:
Panel 3

Page 4:
Panel 4

Page 5:
Panel 5

Or use a suitable multi-panel layout if readable.

The images must not be distorted.

Preserve aspect ratio.

==================================================
22. EXPORT SUCCESS PAGE
==================================================

Create:

export_success.html

Show:

Comic exported successfully.

Download PDF

Create Another Comic

==================================================
23. IMAGE TEST
==================================================

Create:

POST /test-image

This route should test the actual Hugging Face image generation service.

It must generate a real test image.

Save it under:

static/panels/

Return the image URL.

This allows image generation to be tested independently from the complete comic pipeline.

==================================================
24. ERROR HANDLING
==================================================

Handle:

- invalid Gemini API key
- invalid Hugging Face token
- unavailable model
- Hugging Face generation failure
- Gemini generation failure
- network failure
- malformed AI response
- PDF generation failure
- missing files
- invalid user input

Errors must be understandable.

Never expose secret keys.

Never silently switch to fake/demo generation.

==================================================
25. LOADING EXPERIENCE
==================================================

AI image generation may take time.

Show:

"Generating your comic..."

Then:

"Creating story..."

Then:

"Generating panel artwork..."

Then:

"Building your comic..."

Then:

"Creating PDF..."

Use frontend JavaScript for a good loading experience.

Do not make the user think the application is frozen.

==================================================
26. REQUIREMENTS.TXT
==================================================

Create requirements.txt containing compatible versions of:

fastapi
uvicorn[standard]
jinja2
python-multipart
pydantic
pydantic-settings
python-dotenv
google-genai
huggingface_hub
Pillow
fpdf2
httpx
pytest

Install all required dependencies.

==================================================
27. SECURITY
==================================================

Create .gitignore including:

.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
static/panels/*
static/exports/*

Keep:

static/panels/.gitkeep
static/exports/.gitkeep

Never expose API credentials.

==================================================
28. TESTS
==================================================

Create tests for:

- health endpoint
- homepage
- input validation
- JSON API
- layout builder
- PDF export
- image endpoint

Do not mock the final user-facing image behavior in the application itself.

For unit tests that cannot call paid/external AI services, structure tests appropriately, but ensure the actual application code uses the real APIs.

Run:

pytest -q

Fix all code errors.

==================================================
29. README
==================================================

Create a complete beginner-friendly README.

Include:

Project overview

Features

Architecture

Folder structure

Prerequisites

Python installation

Virtual environment setup

Windows instructions

macOS/Linux instructions

Dependency installation

API key setup

Running the application

Testing

API documentation

Troubleshooting

PDF export

Image generation

==================================================
30. SETUP COMMANDS
==================================================

README must include:

Windows:

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

Run:

uvicorn app.main:app --reload

macOS/Linux:

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

Run:

uvicorn app.main:app --reload

==================================================
31. ENVIRONMENT SETUP
==================================================

Create `.env.example`:

GEMINI_API_KEY=
HF_TOKEN=

GEMINI_OUTLINE_MODEL=gemini-2.5-flash
GEMINI_STORY_MODEL=gemini-2.5-pro

IMAGE_MODEL=stabilityai/stable-diffusion-xl-base-1.0

IMPORTANT:

There is NO DEMO_MODE variable.

The application must always use the real AI services.

==================================================
32. FINAL VERIFICATION
==================================================

After building the project:

1. Check every file.
2. Check every import.
3. Install dependencies.
4. Run pytest.
5. Fix failures.
6. Start FastAPI.
7. Open homepage.
8. Open /docs.
9. Test /health.
10. Test /test-image.
11. Confirm a REAL AI image is generated.
12. Generate a complete comic.
13. Confirm exactly 5 AI-generated images.
14. Confirm each panel displays its actual image.
15. Confirm the five images are different and correspond to their scenes.
16. Confirm narration and dialogue appear correctly.
17. Export PDF.
18. Open the PDF.
19. Confirm all 5 actual images are present.
20. Fix any remaining errors.

==================================================
33. CRITICAL IMAGE REQUIREMENT
==================================================

The final result MUST visually look like an actual AI-generated comic.

For example:

PANEL 1
[ACTUAL AI IMAGE OF CHARACTER + SCENE]

PANEL 2
[ACTUAL AI IMAGE OF CHARACTER + NEW SCENE]

PANEL 3
[ACTUAL AI IMAGE OF CHARACTER + CONFLICT]

PANEL 4
[ACTUAL AI IMAGE OF CHARACTER + ACTION]

PANEL 5
[ACTUAL AI IMAGE OF CHARACTER + RESOLUTION]

Do NOT display:

"SCENE VISUALIZATION"

as a replacement for the image.

Do NOT display a colored gradient as the image.

Do NOT display a fake placeholder.

Do NOT use hard-coded sample artwork.

Every panel must contain a genuine AI-generated image.

==================================================
34. IMPORTANT IMPLEMENTATION RULE
==================================================

Do not claim that image generation works merely because the code exists.

Actually test the image-generation endpoint.

Verify that a real image file is returned by the image-generation provider.

Verify that the file is saved.

Verify that the browser displays it.

Verify that the PDF contains it.

==================================================
35. FINAL RESPONSE
==================================================

When finished, report:

1. Files created
2. Dependencies installed
3. Tests passed
4. Application URL
5. API documentation URL
6. Image generation status
7. PDF export status
8. Any remaining issue

If an external API cannot be tested because the API key is missing or invalid, clearly say so.

Do NOT switch to Demo Mode.

Do NOT create fake images to hide the problem.

==================================================
FINAL COMMAND
==================================================

BUILD THE COMPLETE COMICCRAFT APPLICATION NOW.

CREATE ALL FILES.

USE REAL GEMINI AI.

USE REAL AI IMAGE GENERATION.

GENERATE EXACTLY 5 REAL AI-GENERATED COMIC IMAGES.

DISPLAY THEM IN THE WEB APPLICATION.

EXPORT THEM TO PDF.

TEST EVERYTHING.

FIX ALL ERRORS.

DO NOT STOP AT CODE GENERATION.

# END OF MASTER PROMPT