#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Background/Music/URL_fallback/pixabay_music.py
# 🎯 PURPOSE: Pixabay (API या Direct CDN) से Background Music डाउनलोड करना
# ✅ SELF-CONTAINED: अगर API फेल हो, तो Direct CDN लिंक ट्राई करेगा।
# ══════════════════════════════════════════════════════════════════════════════

import os
import subprocess
import requests

def fetch(duration=60, output_path="temp/bg_music.mp3"):
    """
    Pixabay से म्यूजिक लाएगा (पहले API से, फिर Direct URL से)।
    """
    api_key = os.getenv("PIXABAY_API_KEY")
    
    # ── 1. पहले Pixabay API ट्राई करो (अगर Key है) ──────────────────────────
    if api_key:
        print("[pixabay_music] 🔍 Searching music via API...")
        url = f"https://pixabay.com/api/?key={api_key}&q=ambient+background&category=music"
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                hits = r.json().get("hits", [])
                if hits and "audio" in hits[0]:
                    audio_url = hits[0]["audio"]
                    if _download_and_process(audio_url, duration, output_path):
                        return output_path
        except Exception as e:
            print(f"[pixabay_music] ⚠️ API Error: {e}")

    # ── 2. अगर API फेल हो, तो Direct CDN लिंक ट्राई करो ─────────────────────
    print("[pixabay_music] 🔄 Trying Direct CDN Fallback...")
    
    # Pixabay के कुछ फ्री CDN लिंक्स (Ambient/Peaceful)
    cdn_urls = [
        "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=soft-ambient-112191.mp3",
        "https://cdn.pixabay.com/download/audio/2022/03/24/audio_4f3b5c5e3d.mp3?filename=peaceful-background-112194.mp3"
    ]
    
    for url in cdn_urls:
        if _download_and_process(url, duration, output_path):
            return output_path

    print("[pixabay_music] ❌ All Pixabay sources failed.")
    return None


def _download_and_process(audio_url, duration, output_path):
    """म्यूजिक डाउनलोड करके FFmpeg से प्रोसेस करने का हेल्पर फंक्शन"""
    try:
        print(f"[pixabay_music] 📥 Downloading: {audio_url[:50]}...")
        audio_data = requests.get(audio_url, timeout=30).content
        
        if len(audio_data) < 10000: # कम से कम 10KB का होना चाहिए
            return False
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        raw_music = "temp/pixabay_raw.mp3"
        
        with open(raw_music, "wb") as f:
            f.write(audio_data)

        # FFmpeg से प्रोसेस करो (Volume 20%, Fade-in/out)
        print("[pixabay_music] 🎛️ Processing music...")
        fade_out_start = max(duration - 3.0, 1.0)
        
        cmd = (
            f'ffmpeg -y -stream_loop -1 -i {raw_music} -af '
            f'"volume=0.20,afade=t=in:st=0:d=2,afade=t=out:st={fade_out_start:.2f}:d=3" '
            f'-t {duration:.2f} -c:a libmp3lame -b:a 192k {output_path}'
        )
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        
        if os.path.exists(raw_music):
            os.remove(raw_music)

        print(f"[pixabay_music] ✅ Music saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"[pixabay_music] ❌ Error: {e}")
        return False
