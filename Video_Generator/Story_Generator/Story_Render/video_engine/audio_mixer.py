# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/video_engine/audio_mixer.py
# 🎯 PURPOSE: ऑडियो मिक्सिंग का FFmpeg filter बनाना
#            (Voice + Music, Music को Voice के हिसाब से डक करना)
# ══════════════════════════════════════════════════════════════════════════════

def build_audio_filter(has_music):
    """
    ऑडियो मिक्सिंग के लिए FFmpeg filter string बनाता है।

    - अगर म्यूजिक है: Voice को मुख्य रखता है, Music को 15% वॉल्यूम पर
      sidechaincompress से डक करता है (जब आवाज़ आए तो म्यूजिक धीमा हो)
    - अगर म्यूजिक नहीं है: सिर्फ Voice प्ले होगी

    Args:
        has_music (bool): क्या म्यूजिक फाइल मौजूद है?

    Returns:
        str: FFmpeg audio filter string
    """
    if has_music:
        return (
            "[2:a]volume=0.15[bgm];"
            "[bgm][1:a]sidechaincompress=threshold=0.05:ratio=8:attack=50:release=500[ducked_bgm];"
            "[1:a][ducked_bgm]amix=inputs=2:duration=first[a_out]"
        )
    return "[1:a]volume=1.0[a_out]"
