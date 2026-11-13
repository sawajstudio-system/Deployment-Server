# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/video_engine/ffmpeg_runner.py
# 🎯 PURPOSE: तैयार किया हुआ FFmpeg command रन करना
# ══════════════════════════════════════════════════════════════════════════════

import subprocess


def run_ffmpeg(cmd_list, timeout=300):
    """
    FFmpeg command को subprocess में रन करता है।

    Args:
        cmd_list (list): FFmpeg command (list of arguments)
        timeout (int): कितनी देर में खत्म होना चाहिए (सेकंड में)

    Returns:
        bool: True अगर सफल, False अगर फेल
    """
    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode != 0:
            print(f"❌ FFmpeg Error: {result.stderr[:500]}")
            return False
        return True
    except Exception as e:
        print(f"❌ FFmpeg Exception: {e}")
        return False
