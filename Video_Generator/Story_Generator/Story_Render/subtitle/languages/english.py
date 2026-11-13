# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/languages/english.py
# 🎯 PURPOSE: इंग्लिश टेक्स्ट को स्क्रीन के लिए तैयार करना
# ══════════════════════════════════════════════════════════════════════════════

import re

def build_english_text(text, text_color, dot_color):
    """
    यह फंक्शन इंग्लिश के टेक्स्ट को स्क्रीन के लिए तैयार करता है।
    - टेक्स्ट को साफ करता है।
    - डॉट (●) को बाईं तरफ लगाता है।
    - टेक्स्ट और डॉट का रंग सेट करता है।
    """
    if not text:
        return ""

    # 1. टेक्स्ट को साफ करना (Extra spaces, Newlines और Double Quotes हटाना)
    clean_text = re.sub(r'[\n\r"]', ' ', str(text))
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    # 2. रंग और डॉट लगाना
    # इंग्लिश में भी डॉट बाईं तरफ (Left) दिखना चाहिए, इसलिए डॉट पहले आएगा
    colored_text = f"{{\\c{dot_color}}}● {{\\c{text_color}}}{clean_text}"

    return colored_text

# ══════════════════════════════════════════════════════════════════════════════
# TEST (Standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🇬🇧 English Language Builder Test")
    print("═" * 50)
    
    # टेस्ट टेक्स्ट (इंग्लिश में)
    test_text = "Actions are"
    text_color = "&H00D7FF&" # गोल्डन
    dot_color = "&H00FF00&"  # हरा
    
    result = build_english_text(test_text, text_color, dot_color)
    
    print("\n--- Result (ASS Format) ---")
    print(result)
    print("\n(यह कोड जब FFmpeg में जाएगा, तो स्क्रीन पर 🟢 ● Actions are दिखेगा)")
    print("═" * 50)
