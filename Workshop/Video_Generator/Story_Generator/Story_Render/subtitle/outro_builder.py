import os
import re
from ..config.colors import get_color_tag
from ..config.styles import generate_ass_style_string, OUTRO_STYLE

def create_outro_subtitle(outro_text, total_duration, outro_duration=3.5, output_path="temp/outro_sub.ass"):
    if not outro_text: return None
    clean_text = re.sub(r'[\n\r"]', ' ', str(outro_text)).strip()

    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
{generate_ass_style_string("Outro", OUTRO_STYLE)}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    def ts(t):
        h, m, s = int(t // 3600), int((t % 3600) // 60), int(t % 60)
        ms = int(round((t - int(t)) * 100))
        if ms == 100: ms = 99
        return f"{h}:{m:02d}:{s:02d}.{ms:02d}"

    start_t = max(0.0, total_duration - outro_duration)
    formatted_text = f"{{\\fad(500,500)\\c{get_color_tag(1)}}}{clean_text}"
    ass_content += f"Dialogue: 0,{ts(start_t)},{ts(total_duration)},Outro,,0,0,0,,{formatted_text}\n"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f: f.write(ass_content)
    return output_path
