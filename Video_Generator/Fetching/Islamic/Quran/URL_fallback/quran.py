#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Islamic/Quran/URL_fallback/quran.py
# 🎯 PURPOSE: AlQuran Cloud API (Free) का उपयोग करके कुरान की आयत लाना
# ✅ SELF-CONTAINED: इसे किसी API Key की ज़रूरत नहीं होती।
# ══════════════════════════════════════════════════════════════════════════════

import requests
import os
import re

def fetch(ayah="2:255", translation="en.asad"):
    """
    कुरान की आयत लाएगा।
    """
    print(f"[quran] 📖 Fetching Ayah {ayah}...")
    
    # AlQuran Cloud API का URL
    url = f"https://api.alquran.cloud/v1/ayah/{ayah}/{translation}"

    try:
        r = requests.get(url, timeout=15)
        
        if r.status_code == 200:
            data = r.json().get("data", {})
            
            text = data.get("text", "")
            surah_name = data.get("surah", {}).get("englishName", "Unknown")
            ayah_num = data.get("numberInSurah", "Unknown")
            
            # टेक्स्ट को साफ करो (अगर ज़रूरत हो)
            text = re.sub(r"\s+", " ", text).strip()
            
            print(f"[quran] ✅ Success: Surah {surah_name} (Ayah {ayah_num})")
            return {
                "surah": surah_name,
                "ayah": str(ayah_num),
                "text": text,
                "arabic": "", # अभी के लिए इंग्लिश ही ला रहे हैं, बाद में जोड़ सकते हैं
                "source": "AlQuran Cloud"
            }
        else:
            print(f"[quran] ❌ Failed: HTTP {r.status_code}")
            return None
            
    except Exception as e:
        print(f"[quran] ❌ Error: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("📖 Quran URL Test")
    print("═" * 50)
    res = fetch()
    if res:
        print(f"Surah: {res['surah']}")
        print(f"Ayah: {res['ayah']}")
        print(f"Text: {res['text'][:100]}...")
    print("═" * 50)
