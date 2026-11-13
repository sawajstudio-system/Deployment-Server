# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/builders/outro_sub_builder.py
# 🎯 PURPOSE: आउट्रो (Outro) सबटाइटल बनाना — आखिर में धन्यवाद
# ══════════════════════════════════════════════════════════════════════════════

from ..assembler import get_ass_header, get_all_styles, save_ass
from ..timing import ts
from ...config.colors import get_color_tag


def create_outro_subtitle(outro_text, total_duration, outro_duration=3.5, output_path="temp/outro_sub.ass"):
    """
    आखिर में दिखने वाला आउट्रो सबटाइटल बनाता है (धन्यवाद / JazakAllah Khair)।

    Args:
        outro_text (str): आउट्रो का टेक्स्ट
        total_duration (float): वीडियो की कुल लंबाई
        outro_duration (float): आउट्रो कितनी देर दिखे
        output_path (str): कहाँ सेव करना है

    Returns:
        str: बनी हुई ASS फाइल का path (या None)
    """
    if not outro_text:
        return None

    clean_text = str(outro_text).strip()

    # ── ASS फाइल हेडर ───────────────────────────────────────────────────────
    content = get_ass_header()
    content += "\n[V4+ Styles]\n"
    content += get_all_styles()
    content += "\n[Events]\n"
    content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    # ── आउट्रो का समय (वीडियो के आखिर में) ──────────────────────────────────
    start_t = max(0.0, total_duration - outro_duration)

    # ── प्रीमियम कलर + सॉफ्ट फेड ────────────────────────────────────────────
    formatted_text = f"{{\\fad(500,500)\\c{get_color_tag(1)}}}{clean_text}"

    content += f"Dialogue: 0,{ts(start_t)},{ts(total_duration)},Outro,,0,0,0,,{formatted_text}\n"

    return save_ass(content, output_path)
