/**
 * ComicCraft Client-Side Application Script
 * Handles form validation, multi-stage loading experience,
 * single-image diagnostic testing, preset story templates, and lightbox zoom.
 */

// Presets data dictionary
const PRESETS = {
    robot: {
        prompt: "A young mechanic discovers an ancient, glowing war robot buried under scrap metal in her floating island workshop. When she touches the robot's core, its optic sensors ignite with turquoise light, projecting a star map warning of an imminent void fleet.",
        character: "Maya, 17-year-old inventor with grease-smudged cheeks, copper goggles, and an aviator jacket",
        setting: "Neo-Aetheria, a soaring steampunk city of brass bridges and floating cloud docks",
        tone: "Adventure",
        artStyle: "Comic Book"
    },
    cyberpunk: {
        prompt: "A cyber-enhanced private investigator tracks an illegal rogue AI that has escaped into the neon-drenched rainy undercity, only to discover the AI is creating holographic memories for forgotten street orphans.",
        character: "Ren, trench-coated cyborg detective with a glowing blue bionic eye and neural cyberware",
        setting: "Sector 7, Neo-Kyoto in a perpetual neon-lit night rainstorm",
        tone: "Cyberpunk Noir",
        artStyle: "Graphic Novel"
    },
    fantasy: {
        prompt: "A rookie celestial cartographer gets caught in a sky storm and falls into a hidden sanctuary guarded by an ancient feathered griffin with obsidian claws.",
        character: "Kael, nimble starry-eyed explorer with celestial robes and a brass compass staff",
        setting: "The Whispering Peaks, floating mountain islands covered in bioluminescent flora",
        tone: "Dark Fantasy",
        artStyle: "Fantasy Illustration"
    },
    space: {
        prompt: "During routine repairs on a Martian moisture farm, an engineer discovers mysterious crystalline formations growing towards the surface, humming with alien radio signals.",
        character: "Elena, veteran Mars terraformer in a rugged pressurized orange-and-white EVA suit",
        setting: "Sub-surface Martian biodome and red desert canyon at twilight",
        tone: "Sci-Fi Mystery",
        artStyle: "Cinematic"
    }
};

function applyPreset(presetKey) {
    const data = PRESETS[presetKey];
    if (!data) return;

    const promptEl = document.getElementById("prompt");
    const charEl = document.getElementById("main_character");
    const settingEl = document.getElementById("setting");
    const toneEl = document.getElementById("tone");
    const styleEl = document.getElementById("art_style");

    if (promptEl) promptEl.value = data.prompt;
    if (charEl) charEl.value = data.character;
    if (settingEl) settingEl.value = data.setting;
    if (toneEl) toneEl.value = data.tone;
    if (styleEl) styleEl.value = data.artStyle;

    // Smooth scroll down to form
    const form = document.getElementById("comic-form");
    if (form) {
        form.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// Multi-stage loading animation controller
document.addEventListener("DOMContentLoaded", () => {
    const comicForm = document.getElementById("comic-form");
    const loadingOverlay = document.getElementById("loading-overlay");
    const statusText = document.getElementById("loading-status-text");

    if (comicForm && loadingOverlay && statusText) {
        comicForm.addEventListener("submit", (e) => {
            // Verify basic validity
            if (!comicForm.checkValidity()) {
                return;
            }

            loadingOverlay.style.display = "flex";

            const stages = [
                { text: "Generating 5-panel story outline...", step: 1, delay: 500 },
                { text: "Creating character scripts & visual prompts...", step: 2, delay: 2000 },
                { text: "Painting 5 AI panels in parallel...", step: 3, delay: 4000 },
                { text: "Finalizing artwork & character consistency...", step: 3, delay: 8000 },
                { text: "Building comic layout...", step: 4, delay: 11000 },
                { text: "Compiling high-resolution PDF edition...", step: 5, delay: 13000 }
            ];

            stages.forEach((stage) => {
                setTimeout(() => {
                    statusText.textContent = stage.text;
                    updateProgressStep(stage.step);
                }, stage.delay);
            });
        });
    }
});

function updateProgressStep(stepNum) {
    for (let i = 1; i <= 5; i++) {
        const stepEl = document.getElementById(`pstep-${i}`);
        if (!stepEl) continue;
        if (i < stepNum) {
            stepEl.className = "step-item done";
        } else if (i === stepNum) {
            stepEl.className = "step-item active";
        } else {
            stepEl.className = "step-item";
        }
    }
}

// Diagnostic single-image tester
async function runSingleImageTest() {
    const promptInput = document.getElementById("test-image-prompt");
    const resultBox = document.getElementById("test-image-result");
    const spinner = document.getElementById("test-spinner");
    const messageEl = document.getElementById("test-message");
    const previewEl = document.getElementById("test-img-preview");
    const btn = document.getElementById("btn-run-test-image");

    if (!promptInput || !resultBox || !messageEl || !previewEl || !btn) return;

    const promptText = promptInput.value.trim();
    if (!promptText) {
        alert("Please enter a test prompt");
        return;
    }

    resultBox.style.display = "block";
    spinner.style.display = "inline-block";
    previewEl.innerHTML = "";
    messageEl.textContent = "Requesting AI image generation... (takes ~3-8s)";
    messageEl.style.color = "#2563eb";
    btn.disabled = true;

    try {
        const apiBase = window.API_BASE_URL || "";
        const response = await fetch(`${apiBase}/test-image`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ prompt: promptText })
        });

        const data = await response.json();

        spinner.style.display = "none";
        btn.disabled = false;

        if (response.ok && data.success) {
            messageEl.textContent = `✓ Success! Real AI image generated and verified.`;
            messageEl.style.color = "#10b981";
            previewEl.innerHTML = `
                <a href="${data.image_url}" target="_blank">
                    <img src="${data.image_url}" alt="AI Test Generation">
                </a>
                <p style="font-size:0.75rem; color:#64748b; margin-top:4px;">File: ${data.image_url}</p>
            `;
        } else {
            const errDetail = data.detail || data.message || "Failed to generate image";
            messageEl.textContent = `✕ Error: ${errDetail}`;
            messageEl.style.color = "#dc2626";
        }
    } catch (err) {
        spinner.style.display = "none";
        btn.disabled = false;
        messageEl.textContent = `✕ Network/Request Error: ${err.message}`;
        messageEl.style.color = "#dc2626";
    }
}

// Image Lightbox
function openImageLightbox(imgSrc, captionText) {
    const modal = document.getElementById("image-lightbox");
    const img = document.getElementById("lightbox-img");
    const cap = document.getElementById("lightbox-caption");
    if (!modal || !img) return;

    img.src = imgSrc;
    if (cap) cap.textContent = captionText || "";
    modal.style.display = "flex";
}

function closeImageLightbox() {
    const modal = document.getElementById("image-lightbox");
    if (modal) modal.style.display = "none";
}

// ESC key to close lightbox
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        closeImageLightbox();
    }
});
