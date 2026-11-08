# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Islamic/Hadis/URL_fallback/fawaz.py
# 🎯 PURPOSE: Hadith fetch करने के लिए (CDN Based - No API Key Required)
# ══════════════════════════════════════════════════════════════════════════════

import os
import re
import random
import requests

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG: हदीस की किताबें और उनके लिंक
# ══════════════════════════════════════════════════════════════════════════════
# दो मिरर (Mirror) लिंक ताकि अगर एक फेल हो तो दूसरा काम करे
BASE_URLS = [
    "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1",
    "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1",
]

# उन किताबों की लिस्ट जिनसे हम हदीस लेंगे
BOOKS = [
    {"eng": "eng-bukhari", "ara": "ara-bukhari", "name": "Sahih al-Bukhari", "max": 7000},
    {"eng": "eng-muslim", "ara": "ara-muslim", "name": "Sahih Muslim", "max": 5000},
    {"eng": "eng-abudawud", "ara": "ara-abudawud", "name": "Sunan Abu Dawud", "max": 4000},
    {"eng": "eng-tirmidhi", "ara": "ara-tirmidhi", "name": "Jami at-Tirmidhi", "max": 3500},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS: टेक्स्ट साफ करने के लिए
# ══════════════════════════════════════════════════════════════════════════════
def _sanitize(text):
    """Text साफ करने के लिए (Zero-width characters और extra spaces हटाना)"""
    if not text:
        return ""
    text = re.sub(r"[\u200b-\u200f\ufeff\u202a-\u202e]", "", str(text))
    text = text.replace("\n", " ").replace("\r", " ")
    return re.sub(r"\s+", " ", text).strip()

# ══════════════════════════════════════════════════════════════════════════════
# CORE FUNCTION: हदीस लाना
# ══════════════════════════════════════════════════════════════════════════════
def fetch(book=None, number=None):
    """
    Hadith fetch करेगा। 
    अगर सब फेल हो जाए तो hardcoded हदीस रिटर्न करेगा।
    """
    
    # 1. किताब और हदीस नंबर सेलेक्ट करना
    if book:
        matching = [b for b in BOOKS if book.lower() in b["eng"]]
        selected_book = matching[0] if matching else random.choice(BOOKS)
    else:
        selected_book = random.choice(BOOKS)

    # रैंडम हदीस नंबर (1 से लेकर उस किताब की लिमिट तक)
    hadith_num = int(number) if number else random.randint(1, min(selected_book["max"], 100))

    # 2. मिरर URLs से फेच करने की कोशिश करना
    for base in BASE_URLS:
        try:
            url_eng = f"{base}/editions/{selected_book['eng']}/{hadith_num}.json"
            r = requests.get(url_eng, timeout=15)
            
            if r.status_code != 200:
                continue
                
            data = r.json()
            hadiths = data.get("hadiths", [])
            
            if not hadiths:
                continue
                
            first = hadiths[0]
            eng_text = _sanitize(first.get("text", ""))
            
            # अगर टेक्स्ट बहुत छोटा है (जैसे सिर्फ "Sahih"), तो इसे स्किप करो
            if len(eng_text) < 30:
                continue

            # 3. अरबी टेक्स्ट भी लाओ (अगर उपलब्ध हो)
            ara_text = ""
            try:
                url_ara = f"{base}/editions/{selected_book['ara']}/{hadith_num}.json"
                r2 = requests.get(url_ara, timeout=10)
                if r2.status_code == 200:
                    ara_hadiths = r2.json().get("hadiths", [])
                    if ara_hadiths:
                        ara_text = _sanitize(ara_hadiths[0].get("text", ""))
            except Exception:
                pass # अगर अरबी फेल हो तो सिर्फ इंग्लिश चलेगी

            print(f"[fawaz] ✅ Success from {base.split('/')[2]}")
            return {
                "collection": selected_book["name"],
                "number": str(first.get("hadithnumber") or hadith_num),
                "english": eng_text,
                "arabic": ara_text,
                "source": "API"
            }
        except Exception as e:
            print(f"[fawaz] ❌ {base.split('/')[2]} failed: {e}")
            continue

    # 4. अगर सब फेल हो जाए
    print("[fawaz] ⚠️ All APIs failed — using hardcoded fallback")
    return _hardcoded()

def _hardcoded():
    """Local बैकअप (ताकि वीडियो कभी रुके नहीं)"""
    return {
        "collection": "Sahih al-Bukhari",
        "number": "1",
        "english": "The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended.",
        "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى",
        "source": "Hardcoded"
    }

# ══════════════════════════════════════════════════════════════════════════════
# TEST (Standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("📖 Fawaz Hadith Test")
    print("═" * 50)
    result = fetch()
    print(f"Collection: {result['collection']}")
    print(f"Number    : {result['number']}")
    print(f"English   : {result['english'][:100]}...")
    print(f"Arabic    : {result['arabic'][:100]}...")
    print("═" * 50)
