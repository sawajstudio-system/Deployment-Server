# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/main_render.py
# 🎯 PURPOSE: पूरा स्टोरी रेंडर पाइपलाइन — subtitle + CTA + FFmpeg render
# ══════════════════════════════════════════════════════════════════════════════

import os
from .tools import get_audio_duration, generate_cta_image
from .subtitle import (
    create_main_subtitles,
    create_intro_subtitle,
    create_outro_subtitle,
)
from .video_engine import build_ffmpeg_cmd, run_ffmpeg
from .config import (
    generate_ass_style_string,
    ARABIC_STYLE, HINDI_STYLE, ENGLISH_STYLE,
    INTRO_STYLE, OUTRO_STYLE,
)


# ══════════════════════════════════════════════════════════════════════════════
# 🔧 HELPER: सारी ASS फाइलों को एक master फाइल में मिलाना
# ══════════════════════════════════════════════════════════════════════════════
def merge_ass_files(file_paths, output_path):
    """
    Intro + Main + Outro (और CTA) की अलग-अलग ASS फाइलों को एक साथ जोड़ता है।
    हर फाइल से सिर्फ 'Dialogue:' लाइनें उठाता है।

    Args:
        file_paths (list): ASS फाइलों के paths
        output_path (str): बनी हुई master फाइल का path

    Returns:
        str: master ASS फाइल का path
    """
    master_header = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        "PlayResX: 1080\n"
        "PlayResY: 1920\n"
        "WrapStyle: 2\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"{generate_ass_style_string('Arabic', ARABIC_STYLE)}\n"
        f"{generate_ass_style_string('Hindi', HINDI_STYLE)}\n"
        f"{generate_ass_style_string('English', ENGLISH_STYLE)}\n"
        f"{generate_ass_style_string('Intro', INTRO_STYLE)}\n"
        f"{generate_ass_style_string('Outro', OUTRO_STYLE)}\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )

    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as master_file:
        master_file.write(master_header)
        for path in file_paths:
            if path and os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("Dialogue:"):
                            master_file.write(line)

    return output_path


# ══════════════════════════════════════════════════════════════════════════════
# 🎬 MAIN FUNCTION: पूरा वीडियो तैयार करना
# ══════════════════════════════════════════════════════════════════════════════
def build_and_render_story(
    bg_video,
    music_path,
    voice_path,
    hadith,
    hindi_text,
    intro_text,
    outro_text,
    cta_text,
    output_path="temp/Final_Story.mp4"
):
    """
    पूरी स्टोरी वीडियो बनाता है:
        1. Subtitle फाइलें बनाना (intro + main + outro)
        2. CTA इमेज बनाना
        3. सबको एक master ASS में मिलाना
        4. FFmpeg से फाइनल वीडियो रेंडर करना

    Args:
        bg_video (str): बैकग्राउंड वीडियो path
        music_path (str): बैकग्राउंड म्यूजिक path
        voice_path (str): वॉइस audio path
        hadith (dict): जिसमें "arabic" और "english" keys हों
        hindi_text (str): हिंदी अनुवाद
        intro_text (str): इंट्रो का टेक्स्ट
        outro_text (str): आउट्रो का टेक्स्ट
        cta_text (str): CTA का टेक्स्ट
        output_path (str): फाइनल वीडियो का path

    Returns:
        str: फाइनल वीडियो का path (या None अगर फेल)
    """
    print("🎬 [main_render] Starting Cinematic Render...")
    os.makedirs("temp", exist_ok=True)

    # ── 1. वॉइस की लंबाई निकालो ─────────────────────────────────────────────
    duration = get_audio_duration(voice_path)

    # ── 2. सबटाइटल फाइलें बनाओ ──────────────────────────────────────────────
    intro_ass = create_intro_subtitle(intro_text, duration=2.5, output_path="temp/part_intro.ass")
    main_ass  = create_main_subtitles(hadith, hindi_text, duration, output_path="temp/part_main.ass")
    outro_ass = create_outro_subtitle(outro_text, duration, outro_duration=3.5, output_path="temp/part_outro.ass")

    # ── 3. CTA इमेज बनाओ ────────────────────────────────────────────────────
    cta_image = generate_cta_image(output_path="temp/cta_image.png")

    # ── 4. सारी ASS फाइलों को master में मिलाओ ──────────────────────────────
    master_ass = merge_ass_files(
        [intro_ass, main_ass, outro_ass],
        output_path="temp/master_subtitles.ass"
    )

    # ── 5. FFmpeg command बनाओ + रन करो ─────────────────────────────────────
    logo_path = "../assets/logo.png"   # Video_Generator/assets/logo.png

    cmd = build_ffmpeg_cmd(
        bg_video=bg_video,
        voice_path=voice_path,
        music_path=music_path,
        cta_image_path=cta_image,
        logo_path=logo_path,
        master_ass_path=master_ass,
        duration=duration,
        output_path=output_path
    )

    success = run_ffmpeg(cmd)

    if success and os.path.exists(output_path):
        print(f"✅ [main_render] Video Ready: {output_path}")
        return output_path

    print("❌ [main_render] Rendering Failed.")
    return None
