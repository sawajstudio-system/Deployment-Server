import os
import re
from ..config.colors import get_color_tag
from ..config.styles import generate_ass_style_string, ARABIC_STYLE, HINDI_STYLE, ENGLISH_STYLE
from .languages.arabic import build_arabic_text
from .languages.hindi import build_hindi_text
from .languages.english import build_english_text

def create_main_subtitles(hadith, hindi_text, duration, output_path="temp/main_subtitles.ass"):
    print("✍️ [ass_builder] Building Main Subtitles (Continuous & Smooth)...")
    
    ara_text = re.sub(r'[\n\r"]', ' ', str(hadith.get("arabic", ""))).strip()
    hin_text = re.sub(r'[\n\r"]', ' ', str(hindi_text)).strip()
    eng_text = re.sub(r'[\n\r"]', ' ', str(hadith.get("english", ""))).strip()

    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
{generate_ass_style_string("Arabic", ARABIC_STYLE)}
{generate_ass_style_string("Hindi", HINDI_STYLE)}
{generate_ass_style_string("English", ENGLISH_STYLE)}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def ts(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = int(t % 60)
        ms = int(round((t - int(t)) * 100))
        if ms == 100: ms = 99
        return f"{h}:{m:02d}:{s:02d}.{ms:02d}"

    start_t = 1.0
    end_t = max(duration - 0.5, start_t + 1.0)
    total_dur = end_t - start_t
    window_size = 3

    def process_language(text, style_name, lang_idx, builder_func):
        words = text.split()
        if not words: return ""
        
        t_per_word = total_dur / len(words)
        lines = ""
        
        for i, w in enumerate(words):
            w_start = start_t + (i * t_per_word)
            w_end = start_t + ((i + 1) * t_per_word) if i < len(words) - 1 else end_t
                
            start_idx = max(0, i - window_size + 1)
            display_text = " ".join(words[start_idx:i+1])
            
            text_color = get_color_tag(i)
            dot_color = get_color_tag(i + (lang_idx * 3))
            formatted_text = builder_func(display_text, text_color, dot_color)
            
            lines += f"Dialogue: 0,{ts(w_start)},{ts(w_end)},{style_name},,0,0,0,,{formatted_text}\n"
            
        return lines

    if ara_text: ass_content += process_language(ara_text, "Arabic", 0, build_arabic_text)
    if hin_text: ass_content += process_language(hin_text, "Hindi", 1, build_hindi_text)
    if eng_text: ass_content += process_language(eng_text, "English", 2, build_english_text)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ass_content)
    return output_path
