#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Islamic/Dua/API_fallback/ummah.py
# 🎯 PURPOSE: UMMAH API का उपयोग करके रैंडम दुआ (Dua) लाना
# ✅ SELF-CONTAINED: अगर API फेल होगी, तो अपने अंदर से Local Dua (Fallback) देगा।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests
import re

def fetch():
    """
    UMMAH API से एक रैंडम दुआ लाएगा। अगर फेल होगा तो Hardcoded Dua देगा।
    """
    api_key = os.getenv("UMMAH_API_KEY")
    
    if not api_key:
        print("[ummah] ⚠️ UMMAH_API_KEY missing. Using local fallback.")
        return _hardcoded()

    print("[ummah] 🤲 Fetching random Dua from API...")
    
    url = "https://ummahapi.com/api/duas/random"
    headers = {
        "X-API-Key": api_key,
        "Accept": "application/json"
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)
        
        # 1. चेक करो कि स्टेटस 200 है या नहीं
        if r.status_code == 200:
            try:
                # 2. चेक करो कि रिस्पॉन्स सही JSON है या नहीं
                json_data = r.json()
                data = json_data.get("data", {})
                
                arabic = data.get("arabic", "")
                english = data.get("translation", "")
                reference = data.get("reference", "Unknown")
                
                if arabic and english:
                    # टेक्स्ट को साफ करो
                    arabic = re.sub(r'\s+', ' ', arabic).strip()
                    english = re.sub(r'\s+', ' ', english).strip()
                    
                    print("[ummah] ✅ Success: Dua fetched from API")
                    return {
                        "arabic": arabic,
                        "english": english,
                        "reference": reference,
                        "source": "UMMAH API"
                    }
                else:
                    print("[ummah] ⚠️ API returned empty data.")
            except ValueError:
                print("[ummah] ❌ Failed to parse JSON response.")
        else:
            print(f"[ummah] ❌ Failed: HTTP {r.status_code}")
            
    except Exception as e:
        print(f"[ummah] ❌ API Error: {e}")

    # 3. अगर सब कुछ फेल हो जाए, तो लोकल बैकअप इस्तेमाल करो
    print("[ummah] 🔄 Switching to Local Hardcoded Fallback...")
    return _hardcoded()


def _hardcoded():
    """Local बैकअप (ताकि वीडियो कभी रुके नहीं)"""
    return {
        "arabic": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ",
        "english": "Our Lord, give us in this world [that which is] good and in the Hereafter [that which is] good and protect us from the punishment of the Fire.",
        "reference": "Surah Al-Baqarah (2:201)",
        "source": "Hardcoded Fallback"
    }

# ══════════════════════════════════════════════════════════════════════════════
# TEST (standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🤲 UMMAH Dua Test")
    print("═" * 50)
    res = fetch()
    
    print("\n--- Result ---")
    print(f"Source   : {res.get('source')}")
    print(f"Reference: {res.get('reference')}")
    print(f"Arabic   : {res.get('arabic')[:50]}...")
    print(f"English  : {res.get('english')[:100]}...")
    print("═" * 50)
