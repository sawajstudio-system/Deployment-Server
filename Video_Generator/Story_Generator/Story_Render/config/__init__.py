# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/config/__init__.py
# 🎯 PURPOSE: config फोल्डर का मास्टर — fonts + sizes जोड़कर Style Dictionaries बनाना
#            और ASS स्टाइल स्ट्रिंग जनरेट करने वाला फंक्शन देना
# ══════════════════════════════════════════════════════════════════════════════

# ── Fonts (Selected) ────────────────────────────────────────────────────────
from .fonts import SELECTED_ARABIC, SELECTED_HINDI, SELECTED_ENGLISH

# ── Sizes / Margins ─────────────────────────────────────────────────────────
from .sizes import (
    ARABIC_SIZE, HINDI_SIZE, ENGLISH_SIZE, INTRO_SIZE, OUTRO_SIZE, CTA_SIZE,
    MARGIN_L,
    ARABIC_MARGIN_V, HINDI_MARGIN_V, ENGLISH_MARGIN_V,
    INTRO_MARGIN_V, OUTRO_MARGIN_V, CTA_MARGIN_V,
)

# ── Colors ──────────────────────────────────────────────────────────────────
from .colors import BASE_COLOR


# ══════════════════════════════════════════════════════════════════════════════
# 🎨 STYLE DICTIONARIES
# (यही डिक्शनरी ASS फाइल में Style लाइन बनाने के लिए इस्तेमाल होती हैं)
# ══════════════════════════════════════════════════════════════════════════════
ARABIC_STYLE  = {"font": SELECTED_ARABIC,  "size": ARABIC_SIZE,  "alignment": 1, "margin_l": MARGIN_L, "margin_v": ARABIC_MARGIN_V,  "bold": -1}
HINDI_STYLE   = {"font": SELECTED_HINDI,   "size": HINDI_SIZE,   "alignment": 1, "margin_l": MARGIN_L, "margin_v": HINDI_MARGIN_V,   "bold": -1}
ENGLISH_STYLE = {"font": SELECTED_ENGLISH, "size": ENGLISH_SIZE, "alignment": 1, "margin_l": MARGIN_L, "margin_v": ENGLISH_MARGIN_V, "bold": -1}

INTRO_STYLE   = {"font": SELECTED_ENGLISH, "size": INTRO_SIZE,   "alignment": 8, "margin_v": INTRO_MARGIN_V, "bold": -1}
OUTRO_STYLE   = {"font": SELECTED_ENGLISH, "size": OUTRO_SIZE,   "alignment": 8, "margin_v": OUTRO_MARGIN_V, "bold": -1}
CTA_STYLE     = {"font": SELECTED_ENGLISH, "size": CTA_SIZE,     "alignment": 2, "margin_v": CTA_MARGIN_V,   "bold": -1}


# ══════════════════════════════════════════════════════════════════════════════
# 🛠️ HELPER: ASS Style लाइन बनाना
# ══════════════════════════════════════════════════════════════════════════════
def generate_ass_style_string(name, style_dict):
    """
    एक स्टाइल डिक्शनरी लेकर ASS फाइल के 'Style:' फॉर्मेट में लाइन बनाता है।

    Example:
        Style: Arabic,Amiri,85,&H00FFFFFF&,&H000000FF&,&H00000000&,&H80000000,
               -1,0,0,0,100,100,0,0,1,3,2,1,40,40,700,1
    """
    primary_colour = BASE_COLOR              # सफेद टेक्स्ट
    secondary_colour = "&H000000FF&"
    outline_colour = "&H00000000&"           # काला आउटलाइन
    back_colour = "&H80000000"

    return (
        f"Style: {name},{style_dict['font']},{style_dict['size']},"
        f"{primary_colour},{secondary_colour},{outline_colour},{back_colour},"
        f"{style_dict['bold']},0,0,0,100,100,0,0,1,3,2,"
        f"{style_dict['alignment']},40,40,{style_dict['margin_v']},1"
    )


# ── Public Exports ──────────────────────────────────────────────────────────
__all__ = [
    "ARABIC_STYLE", "HINDI_STYLE", "ENGLISH_STYLE",
    "INTRO_STYLE", "OUTRO_STYLE", "CTA_STYLE",
    "generate_ass_style_string",
]
