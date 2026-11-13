import os
import re
from ..config.colors import get_color_tag
from ..config.styles import generate_ass_style_string, ARABIC_STYLE, HINDI_STYLE, ENGLISH_STYLE

def create_main_subtitles(hadith, hindi_text, duration, output_path="temp/main_subtitles.ass"):
    print("✍️ [ass_builder] Building Left-Aligned Smooth Subtitles...")
    
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
        h, m, s = int(t // 3600), int((t % 3600) // 60), int(t % 60)
        ms = int(round((t - int(t)) * 100))
        if ms == 100: ms = 99
        return f"{h}:{m:02d}:{s:02d}.{ms:02d}"

    start_t = 4.0 
    end_t = max(duration - 5.5, start_t + 1.0) 
    total_dur = end_t - start_t

    def process_language(text, style_name, lang_idx):
        words = text.split()
        if not words: return ""
        
        weights = []
        for w in words:
            if w[-1] in ['.', '!', '?', '।']: weights.append(2.0) 
            elif w[-1] in [',', '،', ';', ':']: weights.append(1.5) 
            else: weights.append(1.0) 

        total_weight = sum(weights)
        time_per_weight = total_dur / total_weight
        
        word_timings = []
        current_time = 0
        for weight in weights:
            duration_w = weight * time_per_weight
            word_timings.append((current_time, current_time + duration_w))
            current_time += duration_w

        window_size = 3 
        lines = ""
        
        for i in range(len(words)):
            w_start = start_t + word_timings[i][0]
            w_end = start_t + word_timings[i][1]
            
            start_idx = max(0, i - window_size + 1)
            visible_words = words[start_idx:i+1]
            
            dot_color = get_color_tag(i // 3 + (lang_idx * 3))
            
            if lang_idx == 0: # अरबी RTL
                karaoke_text = f"\u202B{{\\c{dot_color}}}●  "
            else:
                karaoke_text = f"{{\\c{dot_color}}}●  "
                
            for j, word in enumerate(visible_words):
                global_idx = start_idx + j
                color = get_color_tag(global_idx)
                
                if global_idx == i:
                    cs = int((w_end - w_start) * 100)
                    karaoke_text += f"{{\\c{color}\\k{cs}}}{word} "
                else:
                    karaoke_text += f"{{\\c{color}}}{word} "
                
            if lang_idx == 0: karaoke_text += "\u202C"
                
            lines += f"Dialogue: 0,{ts(w_start)},{ts(w_end)},{style_name},,,0,0,,{karaoke_text.strip()}\n"

        return lines

    if ara_text: ass_content += process_language(ara_text, "Arabic", 0)
    if hin_text: ass_content += process_language(hin_text, "Hindi", 1)
    if eng_text: ass_content += process_language(eng_text, "English", 2)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ass_content)
    return output_path
