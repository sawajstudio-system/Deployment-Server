#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Islamic/Quran/URL_fallback/quran_audio.py
# 🎯 PURPOSE: EveryAyah CDN से कुरान की ऑडियो डाउनलोड करना (No Key Required)
# ✅ SELF-CONTAINED: इसे किसी API Key की ज़रूरत नहीं होती।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

def fetch(surah=1, ayah=1, output_path="temp/quran_audio.mp3"):
    """
    EveryAyah CDN से कुरान की आयत की ऑडियो डाउनलोड करेगा।
    """
    # सूरह और आयत को 3-डिजिट फॉर्मेट में बदलो (जैसे 1 -> 001)
    s_str = str(surah).zfill(3)
    a_str = str(ayah).zfill(3)
    
    # Mishary Rashid Alafasy की आवाज़ (128kbps)
    reciter = "Alafasy_128kbps"
    
    print(f"[quran_audio] 🎧 Fetching audio for Surah {surah}, Ayah {ayah}...")
    
    # CDN URL फॉर्मेट: https://everyayah.com/data/{reciter}/{surah}{ayah}.mp3
    url = f"https://everyayah.com/data/{reciter}/{s_str}{a_str}.mp3"

    try:
        r = requests.get(url, timeout=30)
        
        if r.status_code == 200 and len(r.content) > 5000: # कम से कम 5KB की फाइल होनी चाहिए
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "wb") as f:
                f.write(r.content)
                
            print(f"[quran_audio] ✅ Audio saved to {output_path}")
            return output_path
        else:
            print(f"[quran_audio] ❌ Failed: HTTP {r.status_code} or File too small")
            return None
            
    except Exception as e:
        print(f"[quran_audio] ❌ Error: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("📖 Quran Audio Test")
    print("═" * 50)
    # सूरह अल-फातिहा (1), आयत 1
    res = fetch(surah=1, ayah=1)
    if res:
        print(f"Success! Audio saved at: {res}")
    print("═" * 50)
