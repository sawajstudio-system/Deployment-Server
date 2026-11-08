import os, subprocess, sys
from .logo_watermark import get_logo_filter

def render_final_video(bg_video, music_path, voice_path, master_ass_path, cta_image_path, duration, output_path="temp/Final_Story.mp4"):
    print("🎬 [ffmpeg_render] Starting Fast Render...")
    sys.stdout.flush()
    if not bg_video or not os.path.exists(bg_video) or not os.path.exists(voice_path): return None
    logo_scale_filter, logo_path = get_logo_filter()
    cmd_list = ["ffmpeg", "-y", "-stream_loop", "-1", "-i", bg_video, "-i", voice_path]
    has_music = os.path.exists(music_path) and os.path.getsize(music_path) > 0
    if has_music: cmd_list.extend(["-i", music_path])
    cmd_list.extend(["-loop", "1", "-i", cta_image_path])
    cta_idx = 3 if has_music else 2
    has_logo = bool(logo_scale_filter)
    if has_logo:
        cmd_list.extend(["-i", logo_path])
        logo_idx = 4 if has_music else 3
    v_filters = "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg];"
    current_v_out = "bg"
    if has_logo:
        v_filters += f"[{logo_idx}:v]{logo_scale_filter}[logo];"
        v_filters += f"[{current_v_out}][logo]overlay=W-w-40:40[bg_with_logo];"
        current_v_out = "bg_with_logo"
    abs_ass_path = os.path.abspath(master_ass_path)
    v_filters += f"[{current_v_out}]subtitles='{abs_ass_path}':force_style='Fontname=Noto Sans Devanagari'[v_sub];"
    cta_start_time = max(0, duration - 4.5)
    v_filters += f"[v_sub][{cta_idx}:v]overlay=0:0:enable='gte(t,{cta_start_time})'[v_out];"
    a_filters = "[1:a]volume=1.0[a1]; [2:a]volume=0.2[a2]; [a1][a2]amix=inputs=2:duration=first[a_out]" if has_music else "[1:a]volume=1.0[a_out]"
    
    cmd_list.extend([
        "-filter_complex", f"{v_filters} {a_filters}", 
        "-map", "[v_out]", "-map", "[a_out]", 
        # 🟢 SUPERFAST RENDERING MAGIC
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30", 
        "-threads", "0", "-r", "24",
        "-c:a", "aac", "-b:a", "128k", 
        "-t", f"{duration:.2f}", "-shortest", output_path
    ])
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True)
        return output_path if result.returncode == 0 else None
    except Exception: return None
