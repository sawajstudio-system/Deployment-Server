# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/languages/english_render.py
# 🎯 PURPOSE: इंग्लिश टेक्स्ट को साफ करके तैयार करना
# ══════════════════════════════════════════════════════════════════════════════

import re


def build_english_text(text):
    """
    इंग्लिश टेक्स्ट को साफ करके लौटाता है।
    - Extra spaces/newlines हटाता है
    - Double quotes हटाता है (ताकि ASS फाइल में दिक्कत न हो)

    Args:
        text (str): इंग्लिश टेक्स्ट

    Returns:
        str: साफ इंग्लिश टेक्स्ट
    """
    if not text:
        return ""

    # साफ-सफाई: Newlines, Double quotes और Extra spaces हटाना
    clean_text = re.sub(r'[\n\r"]', ' ', str(text))
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    return clean_text
