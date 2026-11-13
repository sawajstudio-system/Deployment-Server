# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/languages/arabic.py
# 🎯 PURPOSE: अरबी टेक्स्ट को RTL (Right-to-Left) फॉर्मेट में सेट करना
# ══════════════════════════════════════════════════════════════════════════════

import re

def build_arabic_text(text, text_color, dot_color):
    """
    यह फंक्शन अरबी के टेक्स्ट को स्क्रीन के लिए तैयार करता है।
    - RTL मार्क (\u202B) लगाता है ताकि अक्षर सही दिशा में दिखें।
    - टेक्स्ट का रंग सेट करता है।
    - डॉट (●) को टेक्स्ट के साथ जोड़ता है।
    """
    if not text:
        return ""

    # 1. टेक्स्ट को साफ करना (Extra spaces और Newlines हटाना)
    clean_text = re.sub(r'\s+', ' ', str(text)).strip()

    # 2. RTL (Right-to-Left) और PDF (Pop Directional Formatting) मार्क लगाना
    # यह सुनिश्चित करता है कि जब अरबी, हिंदी या इंग्लिश के साथ मिक्स हो, 
    # तो अरबी के अक्षर उल्टे न हों।
    rtl_text = f"\u202B{clean_text}\u202C"

    # 3. रंग और डॉट लगाना
    # अरबी में डॉट दाईं तरफ (Right) दिखना चाहिए, इसलिए डॉट टेक्स्ट के बाद आएगा
    # (ASS फॉर्मेट में RTL की वजह से यह विजुअली दाईं तरफ ही दिखेगा)
    colored_text = f"{{\\c{text_color}}}{rtl_text} {{\\c{dot_color}}}●"

    return colored_text

# ══════════════════════════════════════════════════════════════════════════════
# TEST (Standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🕌 Arabic Language Builder Test")
    print("═" * 50)
    
    # टेस्ट टेक्स्ट (अरबी में)
    test_text = "إِنَّمَا الأَعْمَالُ"
    text_color = "&H00D7FF&" # गोल्डन
    dot_color = "&H00FF00&"  # हरा
    
    result = build_arabic_text(test_text, text_color, dot_color)
    
    print("\n--- Result (ASS Format) ---")
    print(result)
    print("\n(यह कोड जब FFmpeg में जाएगा, तो स्क्रीन पर सुनहरे रंग में 'إِنَّمَا الأَعْمَالُ ●' सही दिशा में दिखेगा)")
    print("═" * 50)
