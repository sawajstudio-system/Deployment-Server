#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Background/Photo/API_fallback/pixabay.py
# 🎯 PURPOSE: Pixabay API से Background Photo (तस्वीर) डाउनलोड करना
# ✅ SELF-CONTAINED: अगर फेल होगा, तो None रिटर्न करेगा ताकि URL_fallback चल सके।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

def fetch(query="islamic mosque sunset", output_path="temp/bg_photo.jpg"):
    """
    Pixabay से फोटो डाउनलोड करेगा।
    """
    api_key = os.getenv("PIXABAY_API_KEY")
    if not api_key:
        print("[pixabay] ⚠️ PIXABAY_API_KEY missing")
        return None

    print(f"[pixabay] 🔍 Searching photo for: '{query}'...")
    
    # Pixabay फोटो सर्च URL (orientation=vertical for portrait)
    url = f"https://pixabay.com/api/?key={api_key}&q={query}&image_type=photo&orientation=vertical&per_page=5"

    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            hits = r.json().get("hits", [])
            if hits:
                # सबसे अच्छी क्वालिटी वाली तस्वीर (largeImageURL) निकालो
                photo_url = hits[0].get("largeImageURL") or hits[0].get("webformatURL")
                
                if photo_url:
                    print(f"[pixabay] 📥 Downloading photo...")
                    img_data = requests.get(photo_url, timeout=30).content
                    
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(img_data)
                        
                    print(f"[pixabay] ✅ Photo saved to {output_path}")
                    return output_path
                    
        print(f"[pixabay] ❌ Failed: HTTP {r.status_code}")
        return None
        
    except Exception as e:
        print(f"[pixabay] ❌ Error: {e}")
        return None
