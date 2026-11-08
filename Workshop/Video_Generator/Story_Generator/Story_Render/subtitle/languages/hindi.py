# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/languages/hindi.py
# 🎯 PURPOSE: हिंदी (देवनागरी) टेक्स्ट को स्क्रीन के लिए तैयार करना
# ══════════════════════════════════════════════════════════════════════════════

import re

def build_hindi_text(text, text_color, dot_color):
    """
    यह फंक्शन हिंदी के टेक्स्ट को स्क्रीन के लिए तैयार करता है।
    - टेक्स्ट को साफ करता है।
    - डॉट (●) को बाईं तरफ लगाता है।
    - टेक्स्ट और डॉट का रंग सेट करता है।
    """
    if not text:
        return ""

    # 1. टेक्स्ट को साफ करना (Extra spaces और Newlines हटाना)
    clean_text = re.sub(r'\s+', ' ', str(text)).strip()

    # 2. रंग और डॉट लगाना
    # हिंदी में डॉट बाईं तरफ (Left) दिखना चाहिए, इसलिए डॉट पहले आएगा
    colored_text = f"{{\\c{dot_color}}}● {{\\c{text_color}}}{clean_text}"

    return colored_text

# ══════════════════════════════════════════════════════════════════════════════
# TEST (Standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🇮🇳 Hindi Language Builder Test")
    print("═" * 50)
    
    # टेस्ट टेक्स्ट (हिंदी में)
    test_text = "इन्नमल"
    text_color = "&H00D7FF&" # गोल्डन
    dot_color = "&H00FF00&"  # हरा
    
    result = build_hindi_text(test_text, text_color, dot_color)
    
    print("\n--- Result (ASS Format) ---")
    print(result)
    print("\n(यह कोड जब FFmpeg में जाएगा, तो स्क्रीन पर 🟢 ● इन्नमल दिखेगा)")
    print("═" * 50)
