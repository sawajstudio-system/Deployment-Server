# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/assembler/ass_saver.py
# 🎯 PURPOSE: बनी हुई ASS कंटेंट को फाइल में सेव करना
# ══════════════════════════════════════════════════════════════════════════════

import os


def save_ass(content, output_path):
    """
    ASS कंटेंट को दिए गए path पर सेव करता है।
    अगर फोल्डर नहीं है, तो पहले उसे बना देता है।

    Args:
        content (str): पूरी ASS फाइल का कंटेंट
        output_path (str): कहाँ सेव करना है (जैसे "temp/main_subtitles.ass")

    Returns:
        str: सेव किए गए फाइल का path
    """
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path
