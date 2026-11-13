# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/assembler/ass_style.py
# 🎯 PURPOSE: ASS फाइल का [V4+ Styles] सेक्शन बनाना
# ══════════════════════════════════════════════════════════════════════════════

from ...config import (
    generate_ass_style_string,
    ARABIC_STYLE, HINDI_STYLE, ENGLISH_STYLE,
    INTRO_STYLE, OUTRO_STYLE, CTA_STYLE,
)

# 🟢 ASS फाइल का Style Format लाइन (हर स्टाइल से पहले यही लाइन आती है)
STYLE_FORMAT = (
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
    "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
    "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
    "Alignment, MarginL, MarginR, MarginV, Encoding"
)


def get_all_styles(include_cta=False):
    """
    सारे Style डिक्शनरी से ASS 'Style:' लाइनें बनाकर एक स्ट्रिंग में जोड़ता है।

    Args:
        include_cta (bool): अगर True है तो CTA स्टाइल भी जोड़ेगा।

    Returns:
        str: [V4+ Styles] सेक्शन (Format + सारी Style लाइनें)
    """
    lines = [STYLE_FORMAT]

    lines.append(generate_ass_style_string("Arabic",  ARABIC_STYLE))
    lines.append(generate_ass_style_string("Hindi",   HINDI_STYLE))
    lines.append(generate_ass_style_string("English", ENGLISH_STYLE))
    lines.append(generate_ass_style_string("Intro",   INTRO_STYLE))
    lines.append(generate_ass_style_string("Outro",   OUTRO_STYLE))

    if include_cta:
        lines.append(generate_ass_style_string("CTA", CTA_STYLE))

    return "\n".join(lines) + "\n"
