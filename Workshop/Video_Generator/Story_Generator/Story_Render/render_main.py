import os
from .tools.audio_helper import get_audio_duration
from .tools.cta_generator import generate_cta_image
from .subtitle.ass_builder import create_main_subtitles
from .subtitle.intro_builder import create_intro_subtitle
from .subtitle.outro_builder import create_outro_subtitle
from .video_engine.ffmpeg_render import render_final_video
from .config.styles import generate_ass_style_string, ARABIC_STYLE, HINDI_STYLE, ENGLISH_STYLE, INTRO_STYLE, OUTRO_STYLE
def merge_ass_files(file_paths, output_path):
    master_header = f"""[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n{generate_ass_style_string("Arabic", ARABIC_STYLE)}\n{generate_ass_style_string("Hindi", HINDI_STYLE)}\n{generate_ass_style_string("English", ENGLISH_STYLE)}\n{generate_ass_style_string("Intro", INTRO_STYLE)}\n{generate_ass_style_string("Outro", OUTRO_STYLE)}\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"""
    with open(output_path, "w", encoding="utf-8") as master_file:
        master_file.write(master_header)
        for path in file_paths:
            if path and os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("Dialogue:"): master_file.write(line)
    return output_path
def build_and_render_story(bg_video, music_path, voice_path, hadith, hindi_text, intro_text, outro_text, cta_text, output_path="temp/Final_Story.mp4"):
    os.makedirs("temp", exist_ok=True)
    duration = get_audio_duration(voice_path)
    intro_ass = create_intro_subtitle(intro_text, duration=2.5, output_path="temp/part_intro.ass")
    main_ass = create_main_subtitles(hadith, hindi_text, duration, output_path="temp/part_main.ass")
    outro_ass = create_outro_subtitle(outro_text, duration, outro_duration=3.5, output_path="temp/part_outro.ass")
    cta_image = generate_cta_image(output_path="temp/cta_image.png")
    master_ass = merge_ass_files([intro_ass, main_ass, outro_ass], output_path="temp/master_subtitles.ass")
    return render_final_video(bg_video=bg_video, music_path=music_path, voice_path=voice_path, master_ass_path=master_ass, cta_image_path=cta_image, duration=duration, output_path=output_path)
