# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/__init__.py
# 🎯 PURPOSE: subtitle फोल्डर को Python Package बनाना
#            (assembler + builders + timing + languages सब एक जगह)
# ══════════════════════════════════════════════════════════════════════════════

# ── Assembler ───────────────────────────────────────────────────────────────
from .assembler import get_ass_header, get_all_styles, save_ass

# ── Builders ────────────────────────────────────────────────────────────────
from .builders import (
    create_main_subtitles,
    create_intro_subtitle,
    create_outro_subtitle,
    create_cta_subtitle,
)

# ── Timing ──────────────────────────────────────────────────────────────────
from .timing import ts, compute_word_timings

# ── Languages ───────────────────────────────────────────────────────────────
from .languages import build_arabic_text, build_hindi_text, build_english_text

# ── Public Exports ──────────────────────────────────────────────────────────
__all__ = [
    # Assembler
    "get_ass_header", "get_all_styles", "save_ass",
    # Builders
    "create_main_subtitles", "create_intro_subtitle",
    "create_outro_subtitle", "create_cta_subtitle",
    # Timing
    "ts", "compute_word_timings",
    # Languages
    "build_arabic_text", "build_hindi_text", "build_english_text",
]
