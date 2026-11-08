import os

# 🟢 मुख्य फोल्डर जहाँ सब कुछ बनेगा
BASE = "Video_Generator/Story_Generator/Story_Render"

def create_file(path, lines_list):
    full_path = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines_list))
    print(f"✅ Created: {full_path}")

def generate():
    print("🚀 Generating Full Project Structure...")

    # 1. CONFIG FILES
    create_file("config/screen.py", [
        'PLAY_RES_X = 1080',
        'PLAY_RES_Y = 1920'
    ])

    create_file("config/colors.py", [
        '# रंगों के हेक्स कोड',
        'WHITE = "&H00FFFFFF&"',
        'GOLD = "&H0000D7FF&"',
        'BLACK = "&H00000000&"',
        'DOT_COLORS = ["&H00FFFF&", "&H00D7FF&", "&H507FFF&", "&H90EE90&", "&HD670DA&", "&HEBCE87&"]'
    ])

    create_file("config/fonts.py", [
        'import random',
        'ARABIC_FONTS = ["Amiri", "Reem Kufi", "Scheherazade"]',
        'HINDI_FONTS = ["Yatra One", "Rozha One", "Eczar"]',
        'ENGLISH_FONTS = ["Playfair Display", "Cinzel", "Montserrat", "Lora"]',
        'SELECTED_ARABIC = random.choice(ARABIC_FONTS)',
        'SELECTED_HINDI = random.choice(HINDI_FONTS)',
        'SELECTED_ENGLISH = random.choice(ENGLISH_FONTS)'
    ])

    create_file("config/sizes.py", [
        'ARABIC_SIZE = 85',
        'HINDI_SIZE = 75',
        'ENGLISH_SIZE = 60',
        'ARABIC_MARGIN_V = 700',
        'HINDI_MARGIN_V = 550',
        'ENGLISH_MARGIN_V = 400'
    ])

    # 2. SUBTITLE FILES
    create_file("subtitle/ass_header.py", [
        'from ..config.screen import PLAY_RES_X, PLAY_RES_Y',
        '',
        'def get_header():',
        '    return f"[Script Info]\\nScriptType: v4.00+\\nPlayResX: {PLAY_RES_X}\\nPlayResY: {PLAY_RES_Y}\\nWrapStyle: 2\\n"'
    ])

    create_file("subtitle/ass_style.py", [
        'from ..config.fonts import SELECTED_ARABIC, SELECTED_HINDI, SELECTED_ENGLISH',
        'from ..config.sizes import ARABIC_SIZE, HINDI_SIZE, ENGLISH_SIZE, ARABIC_MARGIN_V, HINDI_MARGIN_V, ENGLISH_MARGIN_V',
        'from ..config.colors import BLACK',
        '',
        'def get_style():',
        '    s1 = f"Style: Arabic,{SELECTED_ARABIC},{ARABIC_SIZE},&H00FFFFFF,&H000000FF,{BLACK},&H80000000,-1,0,0,0,100,100,0,0,1,3,2,1,40,40,{ARABIC_MARGIN_V},1"',
        '    s2 = f"Style: Hindi,{SELECTED_HINDI},{HINDI_SIZE},&H00FFFFFF,&H000000FF,{BLACK},&H80000000,-1,0,0,0,100,100,0,0,1,3,2,1,40,40,{HINDI_MARGIN_V},1"',
        '    s3 = f"Style: English,{SELECTED_ENGLISH},{ENGLISH_SIZE},&H00FFFFFF,&H000000FF,{BLACK},&H80000000,-1,0,0,0,100,100,0,0,1,3,2,1,40,40,{ENGLISH_MARGIN_V},1"',
        '    return "[V4+ Styles]\\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\\n" + s1 + "\\n" + s2 + "\\n" + s3 + "\\n"'
    ])

    create_file("subtitle/ass_saver.py", [
        'import os',
        'def save_ass(content, path):',
        '    os.makedirs(os.path.dirname(path), exist_ok=True)',
        '    with open(path, "w", encoding="utf-8") as f:',
        '        f.write(content)'
    ])

    create_file("subtitle/timing.py", [
        'def format_time(seconds):',
        '    h = int(seconds // 3600)',
        '    m = int((seconds % 3600) // 60)',
        '    s = int(seconds % 60)',
        '    ms = int(round((seconds - int(seconds)) * 100))',
        '    if ms == 100: ms = 99',
        '    return f"{h}:{m:02d}:{s:02d}.{ms:02d}"',
        '',
        'def get_word_timings(text, start_time, total_duration):',
        '    words = text.split()',
        '    if not words: return []',
        '    weights = [2.0 if w[-1] in ".!?।" else 1.5 if w[-1] in ",،;:" else 1.0 for w in words]',
        '    total_weight = sum(weights)',
        '    time_per_weight = total_duration / total_weight',
        '    timings = []',
        '    current_time = start_time',
        '    for i, w in enumerate(words):',
        '        dur = weights[i] * time_per_weight',
        '        timings.append((w, current_time, current_time + dur))',
        '        current_time += dur',
        '    return timings'
    ])

    # 3. VENDORS
    create_file("vendors/hindi_vendor.py", [
        'import re',
        'from ..config.colors import WHITE, DOT_COLORS',
        'from ..subtitle.timing import format_time, get_word_timings',
        'def build_hindi(text, start_t, end_t):',
        '    clean = re.sub(r\'[\\n\\r"]\', " ", str(text)).strip()',
        '    if not clean: return ""',
        '    timings = get_word_timings(clean, start_t, end_t - start_t)',
        '    lines = ""',
        '    for i, (word, w_start, w_end) in enumerate(timings):',
        '        start_idx = max(0, i - 2)',
        '        visible = [t[0] for t in timings[start_idx:i+1]]',
        '        dot = f"{{\\\\c{DOT_COLORS[1]}}}●  "',
        '        words_str = ""',
        '        for j, vw in enumerate(visible):',
        '            if j == len(visible) - 1:',
        '                cs = int((w_end - w_start) * 100)',
        '                words_str += f"{{\\\\c{WHITE}\\\\k{cs}}}{vw} "',
        '            else:',
        '                words_str += f"{{\\\\c{WHITE}}}{vw} "',
        '        lines += f"Dialogue: 0,{format_time(w_start)},{format_time(w_end)},Hindi,,0,0,,{dot}{words_str.strip()}\\n"',
        '    return lines'
    ])

    create_file("vendors/english_vendor.py", [
        'import re',
        'from ..config.colors import WHITE, DOT_COLORS',
        'from ..subtitle.timing import format_time, get_word_timings',
        'def build_english(text, start_t, end_t):',
        '    clean = re.sub(r\'[\\n\\r"]\', " ", str(text)).strip()',
        '    if not clean: return ""',
        '    timings = get_word_timings(clean, start_t, end_t - start_t)',
        '    lines = ""',
        '    for i, (word, w_start, w_end) in enumerate(timings):',
        '        start_idx = max(0, i - 2)',
        '        visible = [t[0] for t in timings[start_idx:i+1]]',
        '        dot = f"{{\\\\c{DOT_COLORS[2]}}}●  "',
        '        words_str = ""',
        '        for j, vw in enumerate(visible):',
        '            if j == len(visible) - 1:',
        '                cs = int((w_end - w_start) * 100)',
        '                words_str += f"{{\\\\c{WHITE}\\\\k{cs}}}{vw} "',
        '            else:',
        '                words_str += f"{{\\\\c{WHITE}}}{vw} "',
        '        lines += f"Dialogue: 0,{format_time(w_start)},{format_time(w_end)},English,,0,0,,{dot}{words_str.strip()}\\n"',
        '    return lines'
    ])

    create_file("vendors/arabic_vendor.py", [
        'import re',
        'from ..config.colors import WHITE, DOT_COLORS',
        'from ..subtitle.timing import format_time, get_word_timings',
        'def build_arabic(text, start_t, end_t):',
        '    clean = re.sub(r\'[\\n\\r"]\', " ", str(text)).strip()',
        '    if not clean: return ""',
        '    timings = get_word_timings(clean, start_t, end_t - start_t)',
        '    lines = ""',
        '    for i, (word, w_start, w_end) in enumerate(timings):',
        '        start_idx = max(0, i - 2)',
        '        visible = [t[0] for t in timings[start_idx:i+1]]',
        '        dot = f"\\\\u202B{{\\\\c{DOT_COLORS[0]}}}●  "',
        '        words_str = ""',
        '        for j, vw in enumerate(visible):',
        '            if j == len(visible) - 1:',
        '                cs = int((w_end - w_start) * 100)',
        '                words_str += f"{{\\\\c{WHITE}\\\\k{cs}}}{vw} "',
        '            else:',
        '                words_str += f"{{\\\\c{WHITE}}}{vw} "',
        '        lines += f"Dialogue: 0,{format_time(w_start)},{format_time(w_end)},Arabic,,0,0,,{dot}{words_str.strip()}\\\\u202C\\n"',
        '    return lines'
    ])

    # 4. BUILDERS
    create_file("builders/main_sub_builder.py", [
        'from ..subtitle.ass_header import get_header',
        'from ..subtitle.ass_style import get_style',
        'from ..subtitle.ass_saver import save_ass',
        'from ..vendors.arabic_vendor import build_arabic',
        'from ..vendors.hindi_vendor import build_hindi',
        'from ..vendors.english_vendor import build_english',
        '',
        'def build_main_subs(hadith, hindi_text, duration):',
        '    header = get_header()',
        '    style = get_style()',
        '    events = "\\n[Events]\\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\\n"',
        '    start_t = 4.0',
        '    end_t = max(duration - 5.5, start_t + 1.0)',
        '    lines = ""',
        '    if hadith.get("arabic"): lines += build_arabic(hadith["arabic"], start_t, end_t)',
        '    if hindi_text: lines += build_hindi(hindi_text, start_t, end_t)',
        '    if hadith.get("english"): lines += build_english(hadith["english"], start_t, end_t)',
        '    content = header + "\\n" + style + "\\n" + events + lines',
        '    out_path = "temp/main_subs.ass"',
        '    save_ass(content, out_path)',
        '    return out_path'
    ])

    # 5. ENGINE
    create_file("engine/logo_processor.py", [
        'def get_logo_filter(logo_width=420, logo_height=150):',
        '    return (',
        '        f"scale={logo_width}:{logo_height},format=rgba,"',
        '        f"split[logo_src][shadow_src];"',
        '        f"[shadow_src]colorchannelmixer=rr=0:gg=0:bb=0:aa=0.6,boxblur=5:2[shadow_blur];"',
        '        f"[shadow_blur][logo_src]overlay=3:3"',
        '    )'
    ])

    create_file("engine/ffmpeg_builder.py", [
        'import os',
        'import subprocess',
        'from .logo_processor import get_logo_filter',
        '',
        'def render_video(bg_video, music_path, voice_path, ass_path, cta_img, duration, output="temp/final.mp4"):',
        '    base_assets = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets"))',
        '    logo_path = os.path.join(base_assets, "logo.png")',
        '    fonts_dir = os.path.join(base_assets, "fonts")',
        '    has_logo = os.path.exists(logo_path)',
        '    cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-i", bg_video, "-i", voice_path]',
        '    has_music = os.path.exists(music_path) and os.path.getsize(music_path) > 0',
        '    if has_music: cmd.extend(["-i", music_path])',
        '    cmd.extend(["-loop", "1", "-i", cta_img])',
        '    cta_idx = 3 if has_music else 2',
        '    if has_logo:',
        '        cmd.extend(["-i", logo_path])',
        '        logo_idx = 4 if has_music else 3',
        '    v_filters = "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,vignette=PI/4[bg];"',
        '    current_out = "bg"',
        '    cta_start = max(0, duration - 5.0)',
        '    if has_logo:',
        '        v_filters += f"[{logo_idx}:v]split[logo_mov][logo_fix];"',
        '        v_filters += f"[logo_mov]{get_logo_filter(420, 150)}[logo_mov_scaled];"',
        '        v_filters += f"[logo_fix]{get_logo_filter(600, 220)}[logo_fix_scaled];"',
        '        v_filters += f"[{current_out}][logo_mov_scaled]overlay=x=\'W-w-40\':y=\'40\':enable=\'lt(t,{cta_start})\'[bg_logo1];"',
        '        v_filters += f"[bg_logo1][logo_fix_scaled]overlay=x=\'(W-w)/2\':y=\'800\':enable=\'gte(t,{cta_start})\'[bg_logo2];"',
        '        current_out = "bg_logo2"',
        '    abs_ass = os.path.abspath(ass_path)',
        '    if os.path.isdir(fonts_dir):',
        '        v_filters += f"[{current_out}]subtitles=\'{abs_ass}\':fontsdir=\'{fonts_dir}\'[v_sub];"',
        '    else:',
        '        v_filters += f"[{current_out}]subtitles=\'{abs_ass}\'[v_sub];"',
        '    v_filters += f"[v_sub][{cta_idx}:v]overlay=0:0:enable=\'gte(t,{cta_start})\'[v_out]"',
        '    if has_music:',
        '        a_filters = "[2:a]volume=0.15[bgm];[bgm][1:a]sidechaincompress=threshold=0.05:ratio=8:attack=50:release=500[ducked_bgm];[1:a][ducked_bgm]amix=inputs=2:duration=first[a_out]"',
        '    else:',
        '        a_filters = "[1:a]volume=1.0[a_out]"',
        '    cmd.extend(["-filter_complex", f"{v_filters}; {a_filters}", "-map", "[v_out]", "-map", "[a_out]", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30", "-threads", "0", "-r", "24", "-c:a", "aac", "-b:a", "128k", "-t", f"{duration:.2f}", "-shortest", output])',
        '    try:',
        '        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)',
        '        if result.returncode != 0:',
        '            print("❌ FFMPEG ERROR:", result.stderr[-1000:])',
        '            return None',
        '        return output',
        '    except Exception as e:',
        '        print("❌ EXCEPTION:", e)',
        '        return None'
    ])

    # 6. MAIN RENDER
    create_file("main_render.py", [
        'import os',
        'from .builders.main_sub_builder import build_main_subs',
        'from .engine.ffmpeg_builder import render_video',
        '',
        'def build_and_render_story(bg_video, music_path, voice_path, hadith, hindi_text, intro_text, outro_text, cta_text, output_path="temp/Final_Story.mp4"):',
        '    print("🎬 [main_render] Building Story...")',
        '    duration = 30.0',
        '    ass_path = build_main_subs(hadith, hindi_text, duration)',
        '    cta_img = "temp/cta.png"',
        '    if not os.path.exists(cta_img):',
        '        from PIL import Image',
        '        img = Image.new("RGBA", (1080, 1920), (0,0,0,0))',
        '        img.save(cta_img)',
        '    return render_video(bg_video, music_path, voice_path, ass_path, cta_img, duration, output_path)'
    ])

    # 7. INIT FILES
    init_dirs = ["config", "subtitle", "vendors", "builders", "engine"]
    for d in init_dirs:
        create_file(os.path.join(d, "__init__.py"), [""])

    print("🎉 All files generated successfully!")

if __name__ == "__main__":
    generate()
