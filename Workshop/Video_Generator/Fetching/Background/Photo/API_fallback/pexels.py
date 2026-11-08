#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Background/Photo/API_fallback/pexels.py
# 🎯 PURPOSE: Pexels API से Background Photo (तस्वीर) डाउनलोड करना
# ✅ SELF-CONTAINED: अगर फेल होगा, तो None रिटर्न करेगा ताकि Pixabay ट्राई हो सके।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

def fetch(query="islamic mosque sunset", output_path="temp/bg_photo.jpg"):
    """
    Pexels से फोटो डाउनलोड करेगा।
    """
    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key:
        print("[pexels] ⚠️ PEXELS_API_KEY missing")
        return None

    print(f"[pexels] 🔍 Searching photo for: '{query}'...")
    headers = {"Authorization": api_key}
    
    # Pexels का फोटो सर्च URL (v1/search)
    url = f"https://api.pexels.com/v1/search?query={query}&orientation=portrait&per_page=5"

    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            photos = r.json().get("photos", [])
            if photos:
                # सबसे अच्छी क्वालिटी वाली तस्वीर का लिंक निकालो
                photo_url = photos[0].get("src", {}).get("original")
                
                if photo_url:
                    print(f"[pexels] 📥 Downloading photo...")
                    img_data = requests.get(photo_url, timeout=30).content
                    
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(img_data)
                        
                    print(f"[pexels] ✅ Photo saved to {output_path}")
                    return output_path
                    
        print(f"[pexels] ❌ Failed: HTTP {r.status_code}")
        return None
        
    except Exception as e:
        print(f"[pexels] ❌ Error: {e}")
        return None
