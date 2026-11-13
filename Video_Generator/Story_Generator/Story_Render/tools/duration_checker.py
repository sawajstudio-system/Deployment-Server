# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/tools/duration_checker.py
# 🎯 PURPOSE: ऑडियो (MP3) की लंबाई (Duration) सेकंड में निकालना
# ══════════════════════════════════════════════════════════════════════════════

import subprocess
import os


def get_audio_duration(audio_path):
    """
    किसी भी ऑडियो फाइल की लंबाई सेकंड में लौटाता है।

    Example:
        get_audio_duration("temp/voice.mp3")  → 25.4

    Args:
        audio_path (str): ऑडियो फाइल का path

    Returns:
        float: सेकंड में अवधि (फाइल न मिले तो 15.0 डिफ़ॉल्ट)
    """
    print(f"⏱️ [duration_checker] Checking duration for: {audio_path}")

    if not os.path.exists(audio_path):
        print(f"❌ [duration_checker] File not found: {audio_path}")
        return 15.0

    try:
        cmd = (
            f'ffprobe -v error -show_entries format=duration '
            f'-of default=noprint_wrappers=1:nokey=1 "{audio_path}"'
        )
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        duration = float(result.stdout.strip())
        print(f"✅ [duration_checker] Audio length is: {duration:.2f} seconds")
        return duration
    except Exception as e:
        print(f"⚠️ [duration_checker] Error: {e}. Using default 15.0 seconds.")
        return 15.0
