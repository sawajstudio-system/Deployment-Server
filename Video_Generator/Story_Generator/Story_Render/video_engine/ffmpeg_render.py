import os, subprocess, sys
from .logo_watermark import get_logo_filter

def render_final_video(bg_video, music_path, voice_path, master_ass_path, cta_image_path, duration, output_path="temp/Final_Story.mp4"):
    print("🎬 [ffmpeg_render] Starting Cinematic Render with Perfect Logo Size...")
    sys.stdout.flush()
    
    if not bg_video or not os.path.exists(bg_video) or not os.path.exists(voice_path): 
        return None
        
    logo_path = "../assets/logo.png"
    has_logo = os.path.exists(logo_path)
    
    cmd_list = ["ffmpeg", "-y", "-stream_loop", "-1", "-i", bg_video, "-i", voice_path]
    
    has_music = os.path.exists(music_path) and os.path.getsize(music_path) > 0
    if has_music: cmd_list.extend(["-i", music_path])
        
    cmd_list.extend(["-loop", "1", "-i", cta_image_path])
    cta_idx = 3 if has_music else 2
    
    if has_logo:
        cmd_list.extend(["-i", logo_path])
        logo_idx = 4 if has_music else 3
        
    v_filters = "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,vignette=PI/4[bg];"
    current_v_out = "bg"
    
    cta_start_time = max(0, duration - 5.0)
    
    if has_logo:
        # 🟢 परफेक्ट साइज़ (न बहुत बड़ा, न बहुत छोटा)
        logo_filter_moving = get_logo_filter(logo_width=280, logo_height=90)  # वीडियो के दौरान
        logo_filter_fixed = get_logo_filter(logo_width=450, logo_height=150)  # आखिर में CTA के समय
        
        v_filters += f"[{logo_idx}:v]split[logo_mov][logo_fix];"
        v_filters += f"[logo_mov]{logo_filter_moving}[logo_mov_scaled];"
        v_filters += f"[logo_fix]{logo_filter_fixed}[logo_fix_scaled];"
        
        x_expr = "40+abs(mod(t*80,2*(W-w-80))-(W-w-80))"
        y_expr = "40+abs(mod(t*100,2*(H-h-80))-(H-h-80))"
        
        v_filters += f"[{current_v_out}][logo_mov_scaled]overlay=x='{x_expr}':y='{y_expr}':enable='lt(t,{cta_start_time})'[bg_with_moving_logo];"
        
        # आखिर में बड़ा लोगो बटन्स के ऊपर (y=850 पर)
        v_filters += f"[bg_with_moving_logo][logo_fix_scaled]overlay=x='(W-w)/2':y='850':enable='gte(t,{cta_start_time})'[bg_with_logo];"
        current_v_out = "bg_with_logo"
        
    abs_ass_path = os.path.abspath(master_ass_path)
    fonts_dir = os.path.abspath("Video_Generator/assets/fonts")
    
    v_filters += f"[{current_v_out}]subtitles='{abs_ass_path}':fontsdir='{fonts_dir}'[v_sub];"
    
    v_filters += f"[v_sub][{cta_idx}:v]overlay=0:0:enable='gte(t,{cta_start_time})'[v_out]"
    
    if has_music:
        a_filters = "[2:a]volume=0.15[bgm];[bgm][1:a]sidechaincompress=threshold=0.05:ratio=8:attack=50:release=500[ducked_bgm];[1:a][ducked_bgm]amix=inputs=2:duration=first[a_out]"
    else:
        a_filters = "[1:a]volume=1.0[a_out]"
    
    cmd_list.extend([
        "-filter_complex", f"{v_filters}; {a_filters}", 
        "-map", "[v_out]", "-map", "[a_out]", 
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30", "-threads", "0", "-r", "24",
        "-c:a", "aac", "-b:a", "128k", 
        "-t", f"{duration:.2f}", "-shortest", output_path
    ])
    
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"❌ FFmpeg Error: {result.stderr[:500]}")
            return None
        return output_path
    except Exception as e: 
        print(f"❌ FFmpeg Exception: {e}")
        return None
