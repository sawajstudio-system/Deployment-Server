# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/config/styles.py
# 🎯 PURPOSE: वीडियो के टेक्स्ट का साइज़, फॉन्ट, और पोजीशन (Margin/Alignment)
# ══════════════════════════════════════════════════════════════════════════════

# 📺 स्क्रीन का रेसोलुशन (मोबाइल वीडियो 1080x1920 के लिए)
PLAY_RES_X = 1080
PLAY_RES_Y = 1920

# ══════════════════════════════════════════════════════════════════════════════
# 1. मुख्य हदीस के टेक्स्ट की सेटिंग्स (Main Story)
# ══════════════════════════════════════════════════════════════════════════════
# Alignment=1 का मतलब है नीचे बाईं तरफ (Bottom-Left)
# MarginV का मतलब है स्क्रीन के नीचे से कितना ऊपर उठकर दिखेगा

ARABIC_STYLE = {
    "font": "Noto Naskh Arabic",
    "size": 85,
    "alignment": 1,
    "margin_l": 120,   # बाईं तरफ से 120px का गैप
    "margin_v": 370,   # नीचे से 370px ऊपर
    "bold": -1         # -1 का मतलब Bold (मोटा) है
}

HINDI_STYLE = {
    "font": "Noto Sans Devanagari",
    "size": 75,
    "alignment": 1,
    "margin_l": 120,
    "margin_v": 260,   # अरबी के ठीक नीचे
    "bold": -1
}

ENGLISH_STYLE = {
    "font": "Noto Sans",
    "size": 60,
    "alignment": 1,
    "margin_l": 120,
    "margin_v": 150,   # हिंदी के ठीक नीचे
    "bold": -1
}

# ══════════════════════════════════════════════════════════════════════════════
# 2. Intro, Outro और CTA की सेटिंग्स (स्क्रीन के बीच या नीचे)
# ══════════════════════════════════════════════════════════════════════════════
# Alignment=2 का मतलब है स्क्रीन के बीच में (Bottom-Center)
# Alignment=5 का मतलब है स्क्रीन के बिल्कुल बीच में (Top-Center)

INTRO_STYLE = {
    "font": "Noto Sans",
    "size": 90,
    "alignment": 5,    # स्क्रीन के बीच में (Top-Center)
    "margin_v": 700,   # बीच में दिखाने के लिए मार्जिन
    "bold": -1
}

OUTRO_STYLE = {
    "font": "Noto Sans",
    "size": 85,
    "alignment": 5,
    "margin_v": 800,
    "bold": -1
}

CTA_STYLE = {
    "font": "Noto Sans",
    "size": 60,
    "alignment": 2,    # स्क्रीन के निचले हिस्से के बीच में
    "margin_v": 300,
    "bold": -1
}

# ══════════════════════════════════════════════════════════════════════════════
# 🛠️ HELPER FUNCTION: स्टाइल्स को ASS फॉर्मेट में बदलने के लिए
# ══════════════════════════════════════════════════════════════════════════════
def generate_ass_style_string(name, style_dict):
    """
    यह फंक्शन हमारे डिक्शनरी (dict) को ASS फाइल के स्टाइल फॉर्मेट में बदलता है।
    """
    # डिफ़ॉल्ट रंग (White) का कोड
    primary_colour = "&H00FFFFFF&" 
    outline_colour = "&H00000000&"
    
    return (
        f"Style: {name},{style_dict['font']},{style_dict['size']},"
        f"{primary_colour},&H000000FF&,{outline_colour},&H80000000,"
        f"{style_dict['bold']},0,0,0,100,100,0,0,1,3,2,"
        f"{style_dict['alignment']},40,40,{style_dict['margin_v']},1"
    )
