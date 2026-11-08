#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Islamic/Hijri_date/URL_fallback/hijri_date.py
# 🎯 PURPOSE: AlAdhan API का उपयोग करके आज की इस्लामिक तारीख (Hijri) लाना
# ✅ SELF-CONTAINED: इसे किसी API Key की ज़रूरत नहीं होती।
# ══════════════════════════════════════════════════════════════════════════════

import requests

def fetch():
    """
    आज की इस्लामिक (Hijri) तारीख लाएगा।
    """
    print("[hijri_date] 📅 Fetching today's Hijri date...")
    
    # AlAdhan API (ग्रेगोरियन से हिजरी तारीख में बदलने के लिए)
    url = "https://api.aladhan.com/v1/gToH"

    try:
        r = requests.get(url, timeout=15)
        
        if r.status_code == 200:
            data = r.json().get("data", {}).get("hijri", {})
            
            day = data.get("day", "")
            month_en = data.get("month", {}).get("en", "")
            month_ar = data.get("month", {}).get("ar", "")
            year = data.get("year", "")
            
            if day and month_en and year:
                date_str = f"{day} {month_en} {year} AH"
                
                print(f"[hijri_date] ✅ Success: {date_str}")
                return {
                    "day": day,
                    "month_en": month_en,
                    "month_ar": month_ar,
                    "year": year,
                    "formatted": date_str,
                    "source": "AlAdhan API"
                }
            else:
                print("[hijri_date] ⚠️ Incomplete data received.")
                return None
        else:
            print(f"[hijri_date] ❌ Failed: HTTP {r.status_code}")
            return None
            
    except Exception as e:
        print(f"[hijri_date] ❌ Error: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("📅 Hijri Date Test")
    print("═" * 50)
    res = fetch()
    if res:
        print("\n--- Result ---")
        print(f"Date: {res['formatted']}")
    print("═" * 50)
