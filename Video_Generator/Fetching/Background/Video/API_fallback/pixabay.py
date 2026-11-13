#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Background/Video/API_fallback/pixabay.py
# 🎯 PURPOSE: Pixabay API से Background Video डाउनलोड करना
# ✅ SELF-CONTAINED: अगर फेल होगा, तो None रिटर्न करेगा ताकि अगली फाइल चल सके।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

def fetch(query="islamic mosque night", duration=60, output_path="temp/bg_video.mp4"):
    """
    Pixabay से वीडियो डाउनलोड करेगा।
    """
    api_key = os.getenv("PIXABAY_API_KEY")
    if not api_key:
        print("[pixabay] ⚠️ PIXABAY_API_KEY missing")
        return None

    print(f"[pixabay] 🔍 Searching video for: '{query}'...")
    # Orientation vertical (portrait) ताकि मोबाइल के लिए सही रहे
    url = f"https://pixabay.com/api/videos/?key={api_key}&q={query}&orientation=vertical&per_page=5"

    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            hits = r.json().get("hits", [])
            if hits:
                # सबसे अच्छी क्वालिटी वाला वीडियो (large) निकालो
                video_url = hits[0].get("videos", {}).get("large", {}).get("url")
                
                if video_url:
                    # वीडियो डाउनलोड करो
                    print(f"[pixabay] 📥 Downloading video...")
                    vid_data = requests.get(video_url, timeout=30).content
                    
                    # फोल्डर बनाओ और सेव करो
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(vid_data)
                        
                    print(f"[pixabay] ✅ Video saved to {output_path}")
                    return output_path
                    
        print(f"[pixabay] ❌ Failed: HTTP {r.status_code}")
        return None
        
    except Exception as e:
        print(f"[pixabay] ❌ Error: {e}")
        return None
