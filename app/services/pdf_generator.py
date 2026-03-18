import logging
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fpdf import FPDF

DEFAULT_FONT = "DejaVu"
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
FONT_DIR = BASE_DIR / "fonts"


class TawasolPDF(FPDF):
    """Reusable PDF builder for AI Tawasol documents."""

    def __init__(self, title: str = "AI Tawasol", orientation: str = "P", lang: str = "en"):
        super().__init__(orientation=orientation)
        self.doc_title = title
        self.lang = lang
        self.set_auto_page_break(auto=True, margin=20)

        self._register_fonts()

        try:
            self.set_text_shaping(True)
        except Exception:
            pass

    def _register_fonts(self):
        regular = FONT_DIR / "DejaVuSansCondensed.ttf"
        bold = FONT_DIR / "DejaVuSansCondensed-Bold.ttf"
        italic = FONT_DIR / "DejaVuSansCondensed-Oblique.ttf"

        if not regular.exists() or not bold.exists() or not italic.exists():
            raise FileNotFoundError(f"Font files are missing in: {FONT_DIR}")

        self.add_font(DEFAULT_FONT, style="", fname=str(regular), uni=True)
        self.add_font(DEFAULT_FONT, style="B", fname=str(bold), uni=True)
        self.add_font(DEFAULT_FONT, style="I", fname=str(italic), uni=True)

    def header(self):
        self.set_font(DEFAULT_FONT, "", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, self._safe(self.doc_title), align="L")
        self.ln(4)
        self.set_draw_color(74, 108, 247)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), self.w - 10, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font(DEFAULT_FONT, "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, text: str, level: int = 1):
        sizes = {1: 14, 2: 12, 3: 11}
        self.set_font(DEFAULT_FONT, "B", sizes.get(level, 11))
        self.set_text_color(44, 62, 80)
        self.ln(4)
        self.multi_cell(0, 8, self._safe(text))
        if level == 1:
            self.set_draw_color(74, 108, 247)
            self.set_line_width(0.3)
            self.line(10, self.get_y(), self.w - 10, self.get_y())
        self.ln(2)

    def body_text(self, text: Any):
        self.set_font(DEFAULT_FONT, "", 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 5, self._safe(text))
        self.ln(2)

    def bullet(self, text: Any, indent: float = 15):
        self.set_x(indent)
        self.set_font(DEFAULT_FONT, "", 10)
        self.set_text_color(60, 60, 60)
        self.cell(5, 5, "-")
        self.multi_cell(self.w - indent - 15, 5, self._safe(text))
        self.ln(1)

    def label_value(self, label: str, value: Any):
        self.set_font(DEFAULT_FONT, "B", 10)
        self.set_text_color(44, 62, 80)
        self.cell(45, 6, self._safe(label) + ":")
        self.set_font(DEFAULT_FONT, "", 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 6, self._safe(value if value not in [None, ""] else "N/A"))
        self.ln(1)

    def priority_badge(self, priority: str):
        colors = {
            "P0": (231, 76, 60),
            "P1": (230, 126, 34),
            "P2": (241, 196, 15),
            "P3": (149, 165, 166),
        }
        r, g, b = colors.get(priority, (149, 165, 166))
        self.set_fill_color(r, g, b)
        text_color = (255, 255, 255) if priority != "P2" else (51, 51, 51)
        self.set_text_color(*text_color)
        self.set_font(DEFAULT_FONT, "B", 8)
        self.cell(15, 5, self._safe(priority), fill=True, align="C")
        self.set_text_color(60, 60, 60)

    @staticmethod
    def _safe(text: Any) -> str:
        if text is None:
            return "N/A"

        s = str(text)
        replacements = {
            "\u2013": "-",
            "\u2014": "-",
            "\u2015": "-",
            "\u2018": "'",
            "\u2019": "'",
            "\u201a": ",",
            "\u201c": '"',
            "\u201d": '"',
            "\u201e": '"',
            "\u2026": "...",
            "\u00a0": " ",
            "\u200b": "",
            "\u2022": "-",
            "\u00b7": "-",
            "\u2212": "-",
            "\u00ae": "(R)",
            "\u2122": "(TM)",
            "\u00b0": "deg",
            "\u2192": "->",
            "\u2190": "<-",
            "\u2713": "v",
            "\u2714": "v",
            "\u2717": "x",
            "\u2718": "x",
            "\u00bd": "1/2",
            "\u00bc": "1/4",
            "\u00be": "3/4",
        }
        for k, v in replacements.items():
            s = s.replace(k, v)
        return s


def _to_bytes(pdf: TawasolPDF) -> bytes:
    return bytes(pdf.output())


def _now_str() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")


def _write_cover(
    pdf: TawasolPDF,
    title: str,
    conversation_id: int | None = None,
    customer_name: str | None = None,
):
    pdf.set_font(DEFAULT_FONT, "B", 18)
    pdf.set_text_color(74, 108, 247)
    pdf.multi_cell(0, 12, pdf._safe(title), align="C")

    pdf.set_font(DEFAULT_FONT, "", 9)
    pdf.set_text_color(150, 150, 150)

    meta_parts = [f"Generated: {_now_str()}"]
    if conversation_id is not None:
        meta_parts.append(f"Conversation #{conversation_id}")
    if customer_name:
        meta_parts.append(f"Customer: {customer_name}")

    pdf.cell(0, 6, "  |  ".join(meta_parts), align="C")
    pdf.ln(14)


def _join_if_list(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value) if value not in [None, ""] else "N/A"

def render_mermaid_to_png(mermaid_code: str) -> tuple[str, str]:
    """
    Render Mermaid code to a temporary PNG using mermaid-cli.
    Returns: (png_path, temp_dir)
    Docker/Linux-friendly with Puppeteer no-sandbox config.
    """
    if not mermaid_code or not mermaid_code.strip():
        raise ValueError("Empty Mermaid code")

    temp_dir = tempfile.mkdtemp(prefix="mermaid_")
    mmd_path = os.path.join(temp_dir, "diagram.mmd")
    png_path = os.path.join(temp_dir, "diagram.png")
    puppeteer_config_path = str(BASE_DIR / "puppeteer-config.json")

    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(mermaid_code)

    cmd = [
        "npx",
        "-p",
        "@mermaid-js/mermaid-cli",
        "mmdc",
        "-p",
        puppeteer_config_path,
        "-i",
        mmd_path,
        "-o",
        png_path,
        "-b",
        "transparent",
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Mermaid render failed: {e.stderr or e.stdout or str(e)}"
        ) from e

    if not os.path.exists(png_path):
        raise RuntimeError("Mermaid PNG was not created")

    return png_path, temp_dir

def add_centered_image(pdf: TawasolPDF, image_path: str, max_width: float = 170):
    x = (pdf.w - max_width) / 2
    pdf.image(image_path, x=x, w=max_width)
    pdf.ln(6)


def generate_summary_pdf(
    summary_data: dict,
    lang: str = "en",
    conversation_id: int | None = None,
    customer_name: str | None = None,
) -> bytes:
    pdf = TawasolPDF(title="Project Summary - AI Tawasol", lang="en")
    pdf.alias_nb_pages()
    pdf.add_page()

    title = "Project Summary"
    _write_cover(pdf, title, conversation_id, customer_name)

    labels = {
        "project_type": "Project Type",
        "project_domain": "Project Domain",
        "target_users": "Target Users",
        "platforms": "Platforms",
        "main_features": "Main Features",
        "timeline": "Timeline",
        "budget": "Budget",
        "notes": "Notes",
    }

    pdf.section_title(title)
    for key in [
        "project_type",
        "project_domain",
        "target_users",
        "platforms",
        "main_features",
        "timeline",
        "budget",
        "notes",
    ]:
        pdf.label_value(labels[key], _join_if_list(summary_data.get(key)))

    return _to_bytes(pdf)


def generate_swot_pdf(
    swot_data: dict,
    lang: str = "en",
    conversation_id: int | None = None,
    customer_name: str | None = None,
) -> bytes:
    pdf = TawasolPDF(title="SWOT Analysis - AI Tawasol", lang="en")
    pdf.alias_nb_pages()
    pdf.add_page()

    title = "SWOT Analysis"
    _write_cover(pdf, title, conversation_id, customer_name)

    sections = [
        ("strengths", "Strengths"),
        ("weaknesses", "Weaknesses"),
        ("opportunities", "Opportunities"),
        ("threats", "Threats"),
    ]

    for key, label in sections:
        items = swot_data.get(key, [])
        if items:
            pdf.section_title(label)
            for item in items:
                pdf.bullet(item)

    recommendation = swot_data.get("recommendation")
    if recommendation:
        pdf.section_title("Recommendation")
        pdf.body_text(recommendation)

    return _to_bytes(pdf)


def generate_activity_diagram_pdf(
    activity_data: dict,
    lang: str = "en",
    conversation_id: int | None = None,
    customer_name: str | None = None,
) -> bytes:
    pdf = TawasolPDF(title="Activity Diagram - AI Tawasol", lang="en")
    pdf.alias_nb_pages()
    pdf.add_page()

    title = activity_data.get("title") or "Activity Diagram"
    _write_cover(pdf, title, conversation_id, customer_name)

    steps = activity_data.get("steps", [])
    mermaid = activity_data.get("mermaid", "")

    if steps:
        pdf.section_title("Flow Steps")
        for step in steps:
            pdf.bullet(step)

    if mermaid:
        pdf.section_title("Activity Diagram")
        temp_dir = None
        try:
            png_path, temp_dir = render_mermaid_to_png(mermaid)
            add_centered_image(pdf, png_path, max_width=170)
        except Exception as e:
            logger.exception("Failed to render Mermaid diagram")
            pdf.set_font(DEFAULT_FONT, "", 9)
            pdf.set_text_color(180, 50, 50)
            pdf.multi_cell(0, 5, f"Diagram rendering failed: {str(e)}")
            pdf.ln(2)
            pdf.set_text_color(60, 60, 60)
            pdf.set_font(DEFAULT_FONT, "", 9)
            pdf.multi_cell(0, 5, str(mermaid))
        finally:
            if temp_dir and os.path.isdir(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

    return _to_bytes(pdf)


def generate_kano_pdf(
    kano_data: dict,
    lang: str = "en",
    conversation_id: int | None = None,
    customer_name: str | None = None,
) -> bytes:
    pdf = TawasolPDF(title="Kano Model Analysis - AI Tawasol", lang="en")
    pdf.alias_nb_pages()
    pdf.add_page()

    title = "Kano Model Feature Classification"
    _write_cover(pdf, title, conversation_id, customer_name)

    category_labels = {
        "must_be": "Must-Be (Basic/Expected)",
        "performance": "Performance (One-Dimensional)",
        "attractive": "Attractive (Delighters)",
        "indifferent": "Indifferent",
        "reverse": "Reverse",
    }

    category_colors = {
        "must_be": (231, 76, 60),
        "performance": (241, 196, 15),
        "attractive": (46, 204, 113),
        "indifferent": (149, 165, 166),
        "reverse": (52, 152, 219),
    }

    grouped = {}
    for feature in kano_data.get("features", []):
        cat = feature.get("category", "indifferent")
        grouped.setdefault(cat, []).append(feature)

    for cat_key, cat_label in category_labels.items():
        cat_features = grouped.get(cat_key, [])
        if not cat_features:
            continue

        r, g, b = category_colors.get(cat_key, (100, 100, 100))
        pdf.set_fill_color(r, g, b)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(DEFAULT_FONT, "B", 11)
        pdf.cell(0, 8, f"  {cat_label} ({len(cat_features)})", fill=True)
        pdf.ln(11)

        for f in cat_features:
            feature_name = f.get("feature") or f.get("feature_en") or "Unnamed feature"
            reason = f.get("reason") or f.get("reason_en") or ""

            pdf.set_font(DEFAULT_FONT, "B", 10)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(5, 6, "-")
            pdf.multi_cell(0, 6, pdf._safe(feature_name))

            if reason:
                pdf.set_x(20)
                pdf.set_font(DEFAULT_FONT, "I", 9)
                pdf.set_text_color(100, 100, 100)
                pdf.multi_cell(pdf.w - 30, 5, pdf._safe("Reason: " + reason))

            pdf.ln(2)

        pdf.ln(2)

    rec = kano_data.get("strategic_recommendation") or kano_data.get("strategic_recommendation_en")
    if rec:
        pdf.section_title("Strategic Recommendation")
        pdf.body_text(rec)

    return _to_bytes(pdf)


def generate_history_pdf(
    messages: list,
    conversation_id: int | None = None,
    customer_name: str | None = None,
) -> bytes:
    pdf = TawasolPDF(title="Conversation History - AI Tawasol", lang="en")
    pdf.alias_nb_pages()
    pdf.add_page()

    _write_cover(pdf, "Conversation History", conversation_id, customer_name)
    pdf.set_font(DEFAULT_FONT, "", 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, f"Messages: {len(messages)}", align="C")
    pdf.ln(12)

    role_colors = {
        "USER": (74, 108, 247),
        "ASSISTANT": (46, 204, 113),
        "SYSTEM": (149, 165, 166),
    }
    role_labels = {
        "USER": "Customer",
        "ASSISTANT": "AI Agent",
        "SYSTEM": "System",
    }

    for msg in messages:
        role = msg.role.value if hasattr(msg.role, "value") else str(msg.role)
        r, g, b = role_colors.get(role, (100, 100, 100))
        label = role_labels.get(role, role.title())

        timestamp = ""
        created_at = getattr(msg, "created_at", None)
        if created_at:
            try:
                timestamp = created_at.strftime("%H:%M:%S")
            except Exception:
                timestamp = str(created_at)

        pdf.set_fill_color(r, g, b)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(DEFAULT_FONT, "B", 9)
        pdf.cell(28, 6, f" {label} ", fill=True)

        if timestamp:
            pdf.set_text_color(150, 150, 150)
            pdf.set_font(DEFAULT_FONT, "", 8)
            pdf.cell(0, 6, f"  {timestamp}")
        pdf.ln(8)

        pdf.set_text_color(60, 60, 60)
        pdf.set_font(DEFAULT_FONT, "", 10)
        pdf.set_x(15)
        pdf.multi_cell(pdf.w - 25, 5, pdf._safe(getattr(msg, "content", "")))
        pdf.ln(3)

        pdf.set_draw_color(220, 220, 220)
        pdf.set_line_width(0.2)
        pdf.line(15, pdf.get_y(), pdf.w - 15, pdf.get_y())
        pdf.ln(4)

    return _to_bytes(pdf)
