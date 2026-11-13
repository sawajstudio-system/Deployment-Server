#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Islamic/Quran/URL_fallback/quran_tafsir.py
# 🎯 PURPOSE: Quran.com API का उपयोग करके आयत की तफसीर (Tafsir) लाना
# ✅ SELF-CONTAINED: इसे किसी API Key की ज़रूरत नहीं होती।
# ══════════════════════════════════════════════════════════════════════════════

import re
import requests

def fetch(ayah="2:255"):
    """
    कुरान की आयत की तफसीर (Tafsir Ibn Kathir) लाएगा।
    """
    print(f"[quran_tafsir] 📖 Fetching Tafsir for Ayah {ayah}...")
    
    # Quran.com API v4 (169 = Tafsir Ibn Kathir in English)
    url = f"https://api.quran.com/api/v4/tafsirs/169/by_ayah/{ayah}"

    try:
        r = requests.get(url, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            tafsir_data = data.get("tafsir", {})
            tafsir_text = tafsir_data.get("text", "")
            
            if not tafsir_text:
                print("[quran_tafsir] ⚠️ No tafsir text found in response.")
                return None

            # HTML टैग्स हटाओ (क्योंकि API कभी-कभी HTML में टेक्स्ट देता है)
            clean_text = re.sub('<[^<]+?>', '', tafsir_text).strip()
            clean_text = re.sub(r'\s+', ' ', clean_text) # Extra spaces हटाओ
            
            print(f"[quran_tafsir] ✅ Success: Tafsir fetched ({len(clean_text)} chars)")
            return {
                "ayah": ayah,
                "tafsir": clean_text,
                "source": "Quran.com (Ibn Kathir)"
            }
        else:
            print(f"[quran_tafsir] ❌ Failed: HTTP {r.status_code}")
            return None
            
    except Exception as e:
        print(f"[quran_tafsir] ❌ Error: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("📖 Quran Tafsir Test")
    print("═" * 50)
    
    # आयतुल कुर्सी (2:255) की तफसीर
    res = fetch("2:255")
    if res:
        print("\n--- Tafsir Preview ---")
        print(res["tafsir"][:200] + "...")
    print("═" * 50)
