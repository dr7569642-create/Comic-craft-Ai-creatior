import logging
import uuid
from pathlib import Path
from PIL import Image
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from app.config import settings
from app.schemas import ComicLayout

logger = logging.getLogger(__name__)


def sanitize_pdf_text(text: str) -> str:
    """Sanitize smart typography and unsupported characters for standard PDF fonts."""
    if not text:
        return ""
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": " - ",
        "\u2026": "...",
        "\u00a0": " ",
        "•": "*",
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    # Ensure compatible latin-1 encoding
    return text.encode("latin-1", "replace").decode("latin-1")


class ComicPDF(FPDF):
    """Custom comic-styled PDF document generator."""

    def __init__(self, title: str):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.comic_title = sanitize_pdf_text(title)
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        if self.page_no() > 1:
            self.set_font("helvetica", "B", 9)
            self.set_text_color(120, 120, 130)
            self.cell(100, 8, sanitize_pdf_text(f"COMICCRAFT  |  {self.comic_title}"), align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.cell(80, 8, f"Page {self.page_no()}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.line(15, 18, 195, 18)
            self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(140, 140, 150)
        self.cell(0, 8, sanitize_pdf_text("Created with ComicCraft AI - Real AI Comic Story Creator"), align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def save_pdf(layout: ComicLayout) -> tuple[Path, str]:
    """Generate a high-quality multi-page PDF from the comic layout with real AI images."""
    unique_id = uuid.uuid4().hex[:8]
    pdf_filename = f"comic_{unique_id}.pdf"
    pdf_path = settings.EXPORTS_DIR / pdf_filename

    pdf = ComicPDF(title=layout.title)

    # ---------------- PAGE 1: COVER & OVERVIEW ----------------
    pdf.add_page()
    pdf.set_fill_color(248, 249, 252)
    pdf.rect(10, 10, 190, 277, "D")

    # Banner Header
    pdf.set_fill_color(255, 75, 43)  # Comic vibrant orange/red
    pdf.rect(15, 15, 180, 26, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("helvetica", "B", 20)
    pdf.set_xy(15, 20)
    pdf.cell(180, 10, sanitize_pdf_text(layout.title.upper()), align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("helvetica", "B", 10)
    pdf.cell(180, 6, "COMICCRAFT AI STORY CREATOR", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(8)

    # Metadata Card
    pdf.set_text_color(40, 44, 52)
    pdf.set_fill_color(240, 243, 248)
    pdf.set_draw_color(210, 215, 225)
    pdf.rect(15, 48, 180, 40, "DF")

    pdf.set_xy(20, 51)
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(40, 7, "Main Character:", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font("helvetica", "", 11)
    pdf.cell(0, 7, sanitize_pdf_text(layout.main_character), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_x(20)
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(40, 7, "Setting:", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font("helvetica", "", 11)
    pdf.cell(0, 7, sanitize_pdf_text(layout.setting), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_x(20)
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(40, 7, "Tone & Style:", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font("helvetica", "", 11)
    pdf.cell(0, 7, f"{sanitize_pdf_text(layout.tone)}  |  {sanitize_pdf_text(layout.art_style)}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_x(20)
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(40, 7, "Story Premise:", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font("helvetica", "I", 10)
    pdf.multi_cell(130, 5, sanitize_pdf_text(layout.prompt))

    pdf.ln(6)

    # First panel preview on cover page
    first_panel = layout.panels[0]
    img_file = Path(first_panel.image_path)
    if img_file.exists():
        with Image.open(img_file) as im:
            orig_w, orig_h = im.size
        target_w = 150
        target_h = min(110.0, (orig_h / orig_w) * target_w)
        x_pos = (210 - target_w) / 2
        y_pos = 98

        # Draw panel box border
        pdf.set_draw_color(20, 20, 30)
        pdf.set_line_width(1.0)
        pdf.rect(x_pos - 2, y_pos - 2, target_w + 4, target_h + 4, "D")
        pdf.image(str(img_file), x=x_pos, y=y_pos, w=target_w, h=target_h)

        # Narration below preview
        pdf.set_xy(15, y_pos + target_h + 8)
        pdf.set_fill_color(255, 245, 180)  # Classic comic narration yellow
        pdf.set_draw_color(50, 50, 60)
        pdf.set_line_width(0.5)

        narration_text = sanitize_pdf_text(f"PANEL 1: {first_panel.narration}")
        pdf.set_font("helvetica", "B", 10)
        pdf.multi_cell(180, 6, narration_text, border=1, fill=True)

    # ---------------- PAGES 2 TO 6: INDIVIDUAL PANELS ----------------
    for panel in layout.panels:
        pdf.add_page()
        pdf.set_draw_color(30, 35, 45)
        pdf.set_line_width(0.8)

        # Panel Banner Badge
        pdf.set_fill_color(30, 35, 45)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("helvetica", "B", 14)
        pdf.rect(15, 24, 180, 10, "F")
        badge_text = f"PANEL {panel.panel_number} OF 5"
        if panel.mood:
            badge_text += f"  -  [{sanitize_pdf_text(panel.mood).upper()}]"
        pdf.set_xy(15, 24)
        pdf.cell(180, 10, badge_text, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.ln(5)

        # Real AI Generated Image
        img_path = Path(panel.image_path)
        if not img_path.exists():
            raise FileNotFoundError(f"Cannot export PDF: image file {img_path} not found.")

        with Image.open(img_path) as im:
            orig_w, orig_h = im.size

        # Fit within 180mm x 140mm area
        max_w = 176.0
        max_h = 135.0
        scale = min(max_w / orig_w, max_h / orig_h)
        target_w = orig_w * scale
        target_h = orig_h * scale
        x_pos = (210 - target_w) / 2
        y_pos = pdf.get_y() + 2

        # Comic Frame Outer Border
        pdf.set_fill_color(245, 247, 250)
        pdf.rect(x_pos - 3, y_pos - 3, target_w + 6, target_h + 6, "FD")
        pdf.image(str(img_path), x=x_pos, y=y_pos, w=target_w, h=target_h)

        # Move below image
        pdf.set_y(y_pos + target_h + 8)

        # Narration Box (Yellow caption box)
        if panel.narration:
            pdf.set_fill_color(255, 250, 205)  # Lemon chiffon comic box
            pdf.set_text_color(20, 20, 20)
            pdf.set_font("helvetica", "B", 10)
            pdf.set_x(15)
            pdf.multi_cell(
                180,
                6,
                sanitize_pdf_text(f"NARRATION:  {panel.narration}"),
                border=1,
                fill=True,
            )
            pdf.ln(3)

        # Dialogue Bubble Box (White speech bubble style box)
        if panel.dialogue:
            pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(15, 23, 42)
            pdf.set_font("helvetica", "", 10)
            pdf.set_x(15)
            pdf.multi_cell(
                180,
                6,
                sanitize_pdf_text(f"DIALOGUE:  {panel.dialogue}"),
                border=1,
                fill=True,
            )
            pdf.ln(3)

        # Scene description caption
        if panel.scene_description:
            pdf.set_font("helvetica", "I", 8)
            pdf.set_text_color(100, 110, 125)
            pdf.set_x(15)
            pdf.cell(180, 5, sanitize_pdf_text(f"Scene: {panel.scene_description}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Output to disk
    pdf.output(str(pdf_path))
    logger.info(f"Successfully generated PDF export at: {pdf_path}")

    download_url = f"/static/exports/{pdf_filename}"
    return pdf_path, download_url
