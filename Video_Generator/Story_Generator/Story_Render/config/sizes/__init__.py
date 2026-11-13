# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/config/sizes/__init__.py
# 🎯 PURPOSE: sizes फोल्डर को Python Package बनाना और सारे साइज़/मार्जिन बाहर उपलब्ध कराना
# ══════════════════════════════════════════════════════════════════════════════

# ── Font Sizes ──────────────────────────────────────────────────────────────
from .font_sizes import (
    ARABIC_SIZE,
    HINDI_SIZE,
    ENGLISH_SIZE,
    INTRO_SIZE,
    OUTRO_SIZE,
    CTA_SIZE,
)

# ── Margins ─────────────────────────────────────────────────────────────────
from .margins import (
    MARGIN_L,
    ARABIC_MARGIN_V,
    HINDI_MARGIN_V,
    ENGLISH_MARGIN_V,
    INTRO_MARGIN_V,
    OUTRO_MARGIN_V,
    CTA_MARGIN_V,
)

# ── Screen Size ─────────────────────────────────────────────────────────────
from .screen_size import PLAY_RES_X, PLAY_RES_Y, ASPECT_RATIO

# ── Public Exports ──────────────────────────────────────────────────────────
__all__ = [
    "ARABIC_SIZE", "HINDI_SIZE", "ENGLISH_SIZE", "INTRO_SIZE", "OUTRO_SIZE", "CTA_SIZE",
    "MARGIN_L",
    "ARABIC_MARGIN_V", "HINDI_MARGIN_V", "ENGLISH_MARGIN_V",
    "INTRO_MARGIN_V", "OUTRO_MARGIN_V", "CTA_MARGIN_V",
    "PLAY_RES_X", "PLAY_RES_Y", "ASPECT_RATIO",
]
