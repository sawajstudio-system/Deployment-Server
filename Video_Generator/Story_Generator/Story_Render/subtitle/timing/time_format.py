# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/timing/time_format.py
# 🎯 PURPOSE: सेकंड को ASS टाइम फॉर्मेट (H:MM:SS.CC) में बदलना
# ══════════════════════════════════════════════════════════════════════════════

def ts(t):
    """
    सेकंड को ASS टाइम फॉर्मेट में बदलता है।

    Example:
        ts(65.42) → "0:01:05.42"

    Args:
        t (float): सेकंड में समय

    Returns:
        str: ASS टाइम स्ट्रिंग
    """
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 100))

    # ASS में 100 centiseconds = 1 second, इसलिए 100 → 99 करना पड़ता है
    if ms == 100:
        ms = 99

    return f"{h}:{m:02d}:{s:02d}.{ms:02d}"
