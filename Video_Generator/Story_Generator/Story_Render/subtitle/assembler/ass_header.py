# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/assembler/ass_header.py
# 🎯 PURPOSE: ASS फाइल का Header (Script Info) बनाना
# ══════════════════════════════════════════════════════════════════════════════

def get_ass_header():
    """
    यह फंक्शन ASS फाइल का 'Script Info' सेक्शन देता है।
    इसमें स्क्रीन का साइज़ और रैपिंग स्टाइल तय होता है।
    """
    return (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        "PlayResX: 1080\n"
        "PlayResY: 1920\n"
        "WrapStyle: 2\n"
    )
