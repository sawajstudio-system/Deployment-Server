# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/builders/cta_sub_builder.py
# 🎯 PURPOSE: CTA (Call to Action) सबटाइटल बनाना — Like/Share/Subscribe
# ══════════════════════════════════════════════════════════════════════════════

from ..assembler import get_ass_header, get_all_styles, save_ass
from ..timing import ts
from ...config.colors import get_color_tag


def create_cta_subtitle(cta_text, total_duration, cta_duration=3.5, output_path="temp/cta_sub.ass"):
    """
    आखिर में दिखने वाला CTA (Like/Share/Subscribe) सबटाइटल बनाता है।

    Args:
        cta_text (str): CTA टेक्स्ट (जैसे "Follow for Daily Hadith")
        total_duration (float): वीडियो की कुल लंबाई
        cta_duration (float): CTA कितनी देर दिखे
        output_path (str): कहाँ सेव करना है

    Returns:
        str: बनी हुई ASS फाइल का path (या None)
    """
    if not cta_text:
        return None

    import re
    clean_text = re.sub(r'[\n\r"]', ' ', str(cta_text)).strip()

    # ── ASS फाइल हेडर (CTA स्टाइल के साथ) ──────────────────────────────────
    content = get_ass_header()
    content += "\n[V4+ Styles]\n"
    content += get_all_styles(include_cta=True)
    content += "\n[Events]\n"
    content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    # ── CTA का समय (वीडियो के आखिर में) ────────────────────────────────────
    start_t = max(0.0, total_duration - cta_duration)

    # ── डॉट + फेड + कलर ────────────────────────────────────────────────────
    formatted_text = f"{{\\fad(500,500)\\c{get_color_tag(2)}}}● {clean_text}"

    content += f"Dialogue: 0,{ts(start_t)},{ts(total_duration)},CTA,,0,0,0,,{formatted_text}\n"

    return save_ass(content, output_path)
