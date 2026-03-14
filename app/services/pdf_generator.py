"""
PDF generation service for AI Tawasol.

Generates structured PDF documents for:
- Kano Model analysis
- Conversation history
- SRS documentation

Uses fpdf2 with DejaVu Unicode TTF fonts (bundled with fpdf2) to correctly
render all characters that LLMs commonly output, including em dashes, smart
quotes, bullets, arrows, and other Unicode symbols.
"""
import io
import logging
from datetime import datetime

from fpdf import FPDF

DEFAULT_FONT = "DejaVu"

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Base PDF helper
# ──────────────────────────────────────────────

class TawasolPDF(FPDF):
    """Custom FPDF subclass with common header/footer and helpers."""

    def __init__(self, title: str = "AI Tawasol", orientation="P"):
        super().__init__(orientation=orientation)
        self.doc_title = title
        self.set_auto_page_break(auto=True, margin=20)

        # DejaVu is bundled with fpdf2 and supports full Unicode, meaning
        # all LLM-generated characters (em dashes, smart quotes, bullets,
        # arrows, etc.) will render correctly without crashing.
        self.add_font("DejaVu", style="",  fname="app/services/fonts/DejaVuSansCondensed.ttf")
        self.add_font("DejaVu", style="B", fname="app/services/fonts/DejaVuSansCondensed-Bold.ttf")
        self.add_font("DejaVu", style="I", fname="app/services/fonts/DejaVuSansCondensed-Oblique.ttf")

    def header(self):
        self.set_font(DEFAULT_FONT, "", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, self.doc_title, align="L")
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
        self.cell(0, 8, self._safe(text), new_x="LMARGIN", new_y="NEXT")
        if level == 1:
            self.set_draw_color(74, 108, 247)
            self.set_line_width(0.3)
            self.line(10, self.get_y(), self.w - 10, self.get_y())
        self.ln(2)

    def body_text(self, text: str):
        self.set_font(DEFAULT_FONT, "", 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 5, self._safe(text))
        self.ln(2)

    def bullet(self, text: str, indent: float = 15):
        self.set_x(indent)
        self.set_font(DEFAULT_FONT, "", 10)
        self.set_text_color(60, 60, 60)
        # \u2022 is the bullet character — DejaVu renders this correctly
        self.cell(5, 5, "\u2022")
        self.multi_cell(self.w - indent - 15, 5, self._safe(text))
        self.ln(1)

    def label_value(self, label: str, value: str):
        self.set_font(DEFAULT_FONT, "B", 10)
        self.set_text_color(44, 62, 80)
        self.cell(45, 6, self._safe(label) + ":")
        self.set_font(DEFAULT_FONT, "", 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 6, self._safe(value or "N/A"))
        self.ln(1)

    def priority_badge(self, priority: str):
        colors = {
            "P0": (231, 76, 60), "P1": (230, 126, 34),
            "P2": (241, 196, 15), "P3": (149, 165, 166),
        }
        r, g, b = colors.get(priority, (149, 165, 166))
        self.set_fill_color(r, g, b)
        text_color = (255, 255, 255) if priority != "P2" else (51, 51, 51)
        self.set_text_color(*text_color)
        self.set_font(DEFAULT_FONT, "B", 8)
        self.cell(15, 5, priority, fill=True, align="C")
        self.set_text_color(60, 60, 60)

    @staticmethod
    def _safe(text) -> str:
        """
        Normalize common Unicode characters that LLMs frequently output
        into clean, readable equivalents.

        With DejaVu we no longer need the latin-1 encode fallback — the font
        handles the full Unicode range. This method still normalises the most
        common "fancy" characters so the output looks clean and consistent
        regardless of what the model produced.
        """
        if text is None:
            return "N/A"
        s = str(text)

        replacements = {
            # Dashes
            "\u2013": "-",      # en dash
            "\u2014": "-",      # em dash
            "\u2015": "-",      # horizontal bar
            # Quotes
            "\u2018": "'",      # left single quotation mark
            "\u2019": "'",      # right single quotation mark
            "\u201a": ",",      # single low-9 quotation mark
            "\u201c": '"',      # left double quotation mark
            "\u201d": '"',      # right double quotation mark
            "\u201e": '"',      # double low-9 quotation mark
            # Ellipsis & spaces
            "\u2026": "...",    # horizontal ellipsis
            "\u00a0": " ",      # non-breaking space
            "\u200b": "",       # zero-width space
            # Symbols commonly produced by LLMs
            "\u2022": "-",      # bullet (we use our own bullet rendering)
            "\u00b7": "-",      # middle dot
            "\u2212": "-",      # minus sign
            "\u00ae": "(R)",    # registered trademark
            "\u2122": "(TM)",   # trademark sign
            "\u00b0": "deg",    # degree sign
            "\u2192": "->",     # rightwards arrow
            "\u2190": "<-",     # leftwards arrow
            "\u2713": "v",      # check mark
            "\u2714": "v",      # heavy check mark
            "\u2717": "x",      # ballot x
            "\u2718": "x",      # heavy ballot x
            # Fractions
            "\u00bd": "1/2",
            "\u00bc": "1/4",
            "\u00be": "3/4",
        }
        for k, v in replacements.items():
            s = s.replace(k, v)

        return s


def _to_bytes(pdf: TawasolPDF) -> bytes:
    buf = io.BytesIO()
    pdf.output(buf)
    return buf.getvalue()


# ──────────────────────────────────────────────
# 1. Kano Model PDF
# ──────────────────────────────────────────────

def generate_kano_pdf(kano_data: dict, lang: str = "en") -> bytes:
    pdf = TawasolPDF(title="Kano Model Analysis - AI Tawasol")
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title
    pdf.set_font(DEFAULT_FONT, "B", 18)
    pdf.set_text_color(74, 108, 247)
    pdf.cell(0, 12, "Kano Model Feature Classification", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font(DEFAULT_FONT, "", 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(8)

    category_labels = {
        "must_be":     "Must-Be (Basic/Expected)",
        "performance": "Performance (One-Dimensional)",
        "attractive":  "Attractive (Delighters)",
        "indifferent": "Indifferent",
        "reverse":     "Reverse",
    }

    category_colors = {
        "must_be":     (231, 76, 60),
        "performance": (241, 196, 15),
        "attractive":  (46, 204, 113),
        "indifferent": (149, 165, 166),
        "reverse":     (52, 152, 219),
    }

    features = kano_data.get("features", [])

    # Group by category
    grouped: dict = {}
    for f in features:
        cat = f.get("category", "indifferent")
        grouped.setdefault(cat, []).append(f)

    for cat_key, cat_label in category_labels.items():
        cat_features = grouped.get(cat_key, [])
        if not cat_features:
            continue

        r, g, b = category_colors.get(cat_key, (100, 100, 100))

        # Category header
        pdf.set_fill_color(r, g, b)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(DEFAULT_FONT, "B", 11)
        pdf.cell(
            0, 8,
            f"  {cat_label}  ({len(cat_features)} features)",
            fill=True, new_x="LMARGIN", new_y="NEXT",
        )
        pdf.ln(3)

        for f in cat_features:
            feature_name = f.get("feature", f.get("feature_en", ""))
            reason = f.get("reason", f.get("reason_en", ""))

            pdf.set_font(DEFAULT_FONT, "B", 10)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(5, 6, "\u2022")
            pdf.cell(0, 6, pdf._safe(feature_name), new_x="LMARGIN", new_y="NEXT")

            if reason:
                pdf.set_x(20)
                pdf.set_font(DEFAULT_FONT, "I", 9)
                pdf.set_text_color(100, 100, 100)
                pdf.multi_cell(pdf.w - 30, 5, pdf._safe(f"Reason: {reason}"))
            pdf.ln(2)

        pdf.ln(4)

    # Strategic recommendation
    rec = kano_data.get(
        "strategic_recommendation",
        kano_data.get("strategic_recommendation_en", ""),
    )
    if rec:
        pdf.section_title("Strategic Recommendation")
        pdf.body_text(rec)

    return _to_bytes(pdf)


# ──────────────────────────────────────────────
# 2. Conversation History PDF
# ──────────────────────────────────────────────

def generate_history_pdf(messages: list) -> bytes:
    pdf = TawasolPDF(title="Conversation History - AI Tawasol")
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title
    pdf.set_font(DEFAULT_FONT, "B", 18)
    pdf.set_text_color(74, 108, 247)
    pdf.cell(0, 12, "Conversation History", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font(DEFAULT_FONT, "", 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(
        0, 6,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  {len(messages)} messages",
        new_x="LMARGIN", new_y="NEXT", align="C",
    )
    pdf.ln(8)

    role_colors = {
        "USER":      (74, 108, 247),
        "ASSISTANT": (46, 204, 113),
        "SYSTEM":    (149, 165, 166),
    }

    for msg in messages:
        role = msg.role.value if hasattr(msg.role, "value") else str(msg.role)
        r, g, b = role_colors.get(role, (100, 100, 100))
        timestamp = ""
        if hasattr(msg, "created_at") and msg.created_at:
            timestamp = msg.created_at.strftime("%H:%M:%S")

        # Role badge
        pdf.set_fill_color(r, g, b)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font(DEFAULT_FONT, "B", 9)
        label = "Customer" if role == "USER" else "AI Agent"
        pdf.cell(22, 6, f" {label} ", fill=True)

        if timestamp:
            pdf.set_text_color(150, 150, 150)
            pdf.set_font(DEFAULT_FONT, "", 8)
            pdf.cell(0, 6, f"  {timestamp}")

        pdf.ln(7)

        # Message content
        pdf.set_text_color(60, 60, 60)
        pdf.set_font(DEFAULT_FONT, "", 10)
        pdf.set_x(15)
        pdf.multi_cell(pdf.w - 25, 5, pdf._safe(msg.content))
        pdf.ln(4)

        # Separator
        pdf.set_draw_color(220, 220, 220)
        pdf.set_line_width(0.2)
        pdf.line(15, pdf.get_y(), pdf.w - 15, pdf.get_y())
        pdf.ln(4)

    return _to_bytes(pdf)


# ──────────────────────────────────────────────
# 3. SRS Document PDF
# ──────────────────────────────────────────────

def generate_srs_pdf(srs_data: dict, lang: str = "en") -> bytes:
    pdf = TawasolPDF(title="Software Requirements Specification - AI Tawasol")
    pdf.alias_nb_pages()
    pdf.add_page()

    # Cover / Title
    pdf.set_font(DEFAULT_FONT, "B", 20)
    pdf.set_text_color(74, 108, 247)
    title = srs_data.get("title", "Software Requirements Specification")
    pdf.multi_cell(0, 10, pdf._safe(title), align="C")
    pdf.ln(3)

    pdf.set_font(DEFAULT_FONT, "", 10)
    pdf.set_text_color(150, 150, 150)
    version = srs_data.get("version", "1.0")
    date = srs_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    pdf.cell(
        0, 6,
        f"Version {version}  |  {date}  |  Generated by AI Tawasol",
        new_x="LMARGIN", new_y="NEXT", align="C",
    )
    pdf.ln(10)

    s = srs_data.get("sections", {})

    # 1. Introduction
    intro = s.get("introduction", {})
    if intro:
        pdf.section_title("1. Introduction")

        if intro.get("purpose"):
            pdf.section_title("1.1 Purpose", level=2)
            pdf.body_text(intro["purpose"])

        if intro.get("scope"):
            pdf.section_title("1.2 Scope", level=2)
            pdf.body_text(intro["scope"])

        definitions = intro.get("definitions", [])
        if definitions:
            pdf.section_title("1.3 Definitions", level=2)
            for d in definitions:
                term = d.get("term", "") if isinstance(d, dict) else str(d)
                defn = d.get("definition", "") if isinstance(d, dict) else ""
                if defn:
                    pdf.set_font(DEFAULT_FONT, "B", 10)
                    pdf.set_text_color(44, 62, 80)
                    pdf.cell(5, 5, "\u2022")
                    pdf.cell(50, 5, pdf._safe(term) + ":")
                    pdf.set_font(DEFAULT_FONT, "", 10)
                    pdf.set_text_color(60, 60, 60)
                    pdf.multi_cell(0, 5, pdf._safe(defn))
                    pdf.ln(1)
                else:
                    pdf.bullet(str(d))

    # 2. Overall Description
    od = s.get("overall_description", {})
    if od:
        pdf.section_title("2. Overall Description")

        if od.get("product_perspective"):
            pdf.section_title("2.1 Product Perspective", level=2)
            pdf.body_text(od["product_perspective"])

        features = od.get("product_features", [])
        if features:
            pdf.section_title("2.2 Product Features", level=2)
            for f in features:
                pdf.bullet(str(f))

        user_classes = od.get("user_classes", [])
        if user_classes:
            pdf.section_title("2.3 User Classes", level=2)
            for u in user_classes:
                if isinstance(u, dict):
                    name = u.get("class", "")
                    desc = u.get("description", "")
                    pdf.bullet(f"{name}: {desc}")
                else:
                    pdf.bullet(str(u))

        if od.get("operating_environment"):
            pdf.section_title("2.4 Operating Environment", level=2)
            pdf.body_text(od["operating_environment"])

        constraints = od.get("constraints", [])
        if constraints:
            pdf.section_title("2.5 Constraints", level=2)
            for c in constraints:
                pdf.bullet(str(c))

        assumptions = od.get("assumptions", [])
        if assumptions:
            pdf.section_title("2.6 Assumptions", level=2)
            for a in assumptions:
                pdf.bullet(str(a))

    # 3. Functional Requirements
    frs = s.get("functional_requirements", [])
    if frs:
        pdf.section_title("3. Functional Requirements")
        for fr in frs:
            fr_id    = fr.get("id", "")
            fr_title = fr.get("title", "")
            priority = fr.get("priority", "P2")

            # Header row: ID + Priority badge
            pdf.set_font(DEFAULT_FONT, "B", 10)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(25, 6, pdf._safe(fr_id))
            pdf.priority_badge(priority)
            pdf.cell(5, 5, "")
            pdf.set_font(DEFAULT_FONT, "B", 10)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(0, 6, pdf._safe(fr_title), new_x="LMARGIN", new_y="NEXT")

            # Description
            if fr.get("description"):
                pdf.set_x(15)
                pdf.body_text(fr["description"])

            # Acceptance criteria
            ac_list = fr.get("acceptance_criteria", [])
            if ac_list:
                pdf.set_x(15)
                pdf.set_font(DEFAULT_FONT, "I", 9)
                pdf.set_text_color(100, 100, 100)
                pdf.cell(0, 5, "Acceptance Criteria:", new_x="LMARGIN", new_y="NEXT")
                for ac in ac_list:
                    pdf.set_x(20)
                    pdf.set_font(DEFAULT_FONT, "", 9)
                    pdf.set_text_color(80, 80, 80)
                    pdf.cell(4, 5, "-")
                    pdf.multi_cell(pdf.w - 35, 5, pdf._safe(ac))
                    pdf.ln(1)

            pdf.ln(3)

    # 4. Non-functional Requirements
    nfrs = s.get("non_functional_requirements", [])
    if nfrs:
        pdf.section_title("4. Non-Functional Requirements")
        for nfr in nfrs:
            nfr_id    = nfr.get("id", "")
            nfr_cat   = nfr.get("category", "")
            nfr_title = nfr.get("title", "")

            pdf.set_font(DEFAULT_FONT, "B", 10)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(25, 6, pdf._safe(nfr_id))
            # Category badge
            pdf.set_fill_color(52, 152, 219)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font(DEFAULT_FONT, "B", 8)
            pdf.cell(30, 5, pdf._safe(nfr_cat.upper()), fill=True, align="C")
            pdf.cell(5, 5, "")
            pdf.set_font(DEFAULT_FONT, "B", 10)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(0, 6, pdf._safe(nfr_title), new_x="LMARGIN", new_y="NEXT")

            if nfr.get("description"):
                pdf.set_x(15)
                pdf.body_text(nfr["description"])
            pdf.ln(2)

    # 5. Constraints & Assumptions
    ca = s.get("constraints_and_assumptions", [])
    if ca:
        pdf.section_title("5. Constraints & Assumptions")
        for item in ca:
            pdf.bullet(str(item))

    # 6. Acceptance Criteria Summary
    acs = s.get("acceptance_criteria_summary")
    if acs:
        pdf.section_title("6. Acceptance Criteria Summary")
        pdf.body_text(acs)

    return _to_bytes(pdf)