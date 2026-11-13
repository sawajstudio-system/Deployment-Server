# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/builders/intro_sub_builder.py
# 🎯 PURPOSE: इंट्रो (Intro) सबटाइटल बनाना — शुरुआत में धीमा फेड-इन
# ══════════════════════════════════════════════════════════════════════════════

from ..assembler import get_ass_header, get_all_styles, save_ass
from ..timing import ts
from ...config.colors import INTRO_TEXT_COLOR


def create_intro_subtitle(intro_text, duration=3.5, output_path="temp/intro_sub.ass"):
    """
    शुरुआत के लिए इंट्रो सबटाइटल बनाता है (गोल्डन कलर + ग्लो + धीमा फेड)।

    Args:
        intro_text (str): इंट्रो का टेक्स्ट (जैसे "Sawaj Studio Presents")
        duration (float): इंट्रो कितनी देर दिखे (सेकंड में)
        output_path (str): कहाँ सेव करना है

    Returns:
        str: बनी हुई ASS फाइल का path (या None अगर टेक्स्ट खाली हो)
    """
    if not intro_text:
        return None

    clean_text = str(intro_text).strip()

    # ── ASS फाइल हेडर ───────────────────────────────────────────────────────
    content = get_ass_header()
    content += "\n[V4+ Styles]\n"
    content += get_all_styles()
    content += "\n[Events]\n"
    content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    # ── गोल्डन कलर + ग्लो (blur5) + धीमा फेड-इन/आउट (1000ms) ───────────────
    formatted_text = f"{{\\fad(1000,1000)\\blur5\\c{INTRO_TEXT_COLOR}\\3c&H000000&}}{clean_text}"

    content += f"Dialogue: 0,{ts(0.0)},{ts(duration)},Intro,,0,0,0,,{formatted_text}\n"

    return save_ass(content, output_path)
