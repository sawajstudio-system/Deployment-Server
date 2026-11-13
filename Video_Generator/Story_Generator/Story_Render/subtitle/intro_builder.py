import os
import re
from ..config.styles import generate_ass_style_string, INTRO_STYLE

def create_intro_subtitle(intro_text, duration=3.5, output_path="temp/intro_sub.ass"):
    if not intro_text: return None
    clean_text = str(intro_text).strip()

    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
{generate_ass_style_string("Intro", INTRO_STYLE)}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    def ts(t):
        h, m, s = int(t // 3600), int((t % 3600) // 60), int(t % 60)
        ms = int(round((t - int(t)) * 100))
        if ms == 100: ms = 99
        return f"{h}:{m:02d}:{s:02d}.{ms:02d}"

    # गोल्डन कलर, ग्लो एफेक्ट, और बहुत धीमा फेड-इन
    formatted_text = f"{{\\fad(1000,1000)\\blur5\\c&H00D7FF&\\3c&H000000&}}{clean_text}"

    ass_content += f"Dialogue: 0,{ts(0.0)},{ts(duration)},Intro,,0,0,0,,{formatted_text}\n"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f: f.write(ass_content)
    return output_path
