# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/video_engine/ffmpeg_builder.py
# ══════════════════════════════════════════════════════════════════════════════

import os
from .video_filter import build_video_filter
from .audio_mixer import build_audio_filter


def build_ffmpeg_cmd(
    bg_video, voice_path, music_path, cta_image_path,
    logo_path, master_ass_path, duration, output_path
):
    has_music = os.path.exists(music_path) and os.path.getsize(music_path) > 0
    has_logo = os.path.exists(logo_path)

    cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-i", bg_video, "-i", voice_path]

    if has_music:
        cmd += ["-i", music_path]

    cmd += ["-loop", "1", "-i", cta_image_path]
    cta_idx = 3 if has_music else 2

    logo_idx = -1
    if has_logo:
        cmd += ["-i", logo_path]
        logo_idx = 4 if has_music else 3

    cta_start_time = max(0, duration - 5.0)

    # 🟢 यहाँ has_logo के साथ logo_idx भी भेज रहे हैं ताकि filter को पता हो लोगो कहाँ है
    video_filters, current_v_out = build_video_filter(has_logo, logo_idx, cta_idx, cta_start_time)

    abs_ass_path = os.path.abspath(master_ass_path)
    fonts_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "assets", "fonts"
    ))

    video_filters += (
        f"[{current_v_out}]"
        f"subtitles='{abs_ass_path}':fontsdir='{fonts_dir}'"
        f"[v_sub];"
    )

    video_filters += (
        f"[v_sub][{cta_idx}:v]"
        f"overlay=0:0:enable='gte(t,{cta_start_time})'[v_out]"
    )

    audio_filters = build_audio_filter(has_music)

    cmd += [
        "-filter_complex", f"{video_filters}; {audio_filters}",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30", "-threads", "0", "-r", "24",
        "-c:a", "aac", "-b:a", "128k",
        "-t", f"{duration:.2f}", "-shortest", output_path
    ]

    return cmd
