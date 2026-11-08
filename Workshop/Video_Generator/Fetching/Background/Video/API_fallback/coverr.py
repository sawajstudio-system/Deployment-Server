#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Background/Video/API_fallback/coverr.py
# 🎯 PURPOSE: Coverr API से Background Video डाउनलोड करना
# ✅ SELF-CONTAINED: अगर फेल होगा, तो None रिटर्न करेगा ताकि URL_fallback चल सके।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

def fetch(query="nature", duration=60, output_path="temp/bg_video.mp4"):
    """
    Coverr से वीडियो डाउनलोड करेगा।
    """
    api_key = os.getenv("COVERR_API_KEY")
    if not api_key:
        print("[coverr] ⚠️ COVERR_API_KEY missing")
        return None

    print(f"[coverr] 🔍 Searching video for: '{query}'...")
    url = f"https://api.coverr.co/videos?query={query}&page_size=5"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            hits = r.json().get("hits", [])
            if hits:
                # Coverr में वीडियो लिंक 'urls' के अंदर होता है
                video_url = hits[0].get("urls", {}).get("mp4")
                
                if video_url:
                    print(f"[coverr] 📥 Downloading video...")
                    vid_data = requests.get(video_url, timeout=30).content
                    
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(vid_data)
                        
                    print(f"[coverr] ✅ Video saved to {output_path}")
                    return output_path
                    
        print(f"[coverr] ❌ Failed: HTTP {r.status_code}")
        return None
        
    except Exception as e:
        print(f"[coverr] ❌ Error: {e}")
        return None
