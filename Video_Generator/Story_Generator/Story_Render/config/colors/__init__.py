# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/config/colors/__init__.py
# 🎯 PURPOSE: colors फोल्डर को Python Package बनाना और सारे रंग बाहर उपलब्ध कराना
# ══════════════════════════════════════════════════════════════════════════════

# ── Premium Palette + Helper ────────────────────────────────────────────────
from .hex_colors import PREMIUM_COLORS, get_color_tag

# ── Individual Colors ───────────────────────────────────────────────────────
from .base_color import BASE_COLOR
from .highlight_color import HIGHLIGHT_COLOR
from .arabic_text_color import ARABIC_TEXT_COLOR
from .hindi_text_color import HINDI_TEXT_COLOR
from .english_text_color import ENGLISH_TEXT_COLOR
from .intro_text_color import INTRO_TEXT_COLOR
from .outro_text_color import OUTRO_TEXT_COLOR
from .cta_text_color import CTA_TEXT_COLOR

# ── Public Exports ──────────────────────────────────────────────────────────
__all__ = [
    "PREMIUM_COLORS",
    "get_color_tag",
    "BASE_COLOR",
    "HIGHLIGHT_COLOR",
    "ARABIC_TEXT_COLOR",
    "HINDI_TEXT_COLOR",
    "ENGLISH_TEXT_COLOR",
    "INTRO_TEXT_COLOR",
    "OUTRO_TEXT_COLOR",
    "CTA_TEXT_COLOR",
]
