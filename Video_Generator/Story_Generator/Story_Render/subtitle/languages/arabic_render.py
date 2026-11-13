# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/languages/arabic_render.py
# 🎯 PURPOSE: अरबी टेक्स्ट को RTL (Right-to-Left) फॉर्मेट में तैयार करना
# ══════════════════════════════════════════════════════════════════════════════

import re


def build_arabic_text(text):
    """
    अरबी टेक्स्ट को साफ करके RTL मार्क के साथ लौटाता है।
    - Extra spaces/newlines हटाता है
    - RTL (Right-to-Left) मार्क (\u202B) लगाता है
    - PDF (Pop Directional Formatting) मार्क (\u202C) लगाता है
      (ताकि हिंदी/इंग्लिश के साथ मिक्स होने पर अरबी उल्टी न दिखे)

    Args:
        text (str): अरबी टेक्स्ट

    Returns:
        str: RTL फॉर्मेट में साफ अरबी टेक्स्ट
    """
    if not text:
        return ""

    # 1. साफ-सफाई (Extra spaces और Newlines हटाना)
    clean_text = re.sub(r'\s+', ' ', str(text)).strip()

    # 2. RTL मार्क के साथ लपेटना
    rtl_text = f"\u202B{clean_text}\u202C"

    return rtl_text
