#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/A_API_room/05_video_services/pixabay.py
# ══════════════════════════════════════════════════════════════════════════════
"""
Pixabay API Test — Air Mode
"""
import os
import sys
import requests

API_KEY_ENV  = "PIXABAY_API_KEY"
API_URL      = "https://pixabay.com/api/"
TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"

def send_telegram(text):
    tok  = os.getenv(TG_TOKEN_ENV)
    chat = os.getenv(TG_CHAT_ENV)
    if not tok or not chat:
        print(f"[no telegram] {text}")
        return
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{tok}/sendMessage",
            json={"chat_id": chat, "text": text[:4000]},
            timeout=15,
        )
        print(f"[telegram] sent: HTTP {r.status_code}")
    except Exception as e:
        print(f"[telegram error] {e}")

def test_pixabay():
    key = os.getenv(API_KEY_ENV)
    if not key:
        msg = f"⚠️ WARN Pixabay: {API_KEY_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    params = {
        "key": key,
        "q": "nature",
        "per_page": 3,
        "image_type": "photo",
        "safesearch": "true"
    }

    print(f"[pixabay] calling: {API_URL}")

    try:
        r = requests.get(API_URL, params=params, timeout=30)
        print(f"[pixabay] HTTP {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            hits = data.get("hits", [])
            
            if hits:
                photo = hits[0]
                image_url = photo.get("largeImageURL") or photo.get("webformatURL", "")
                user = photo.get("user", "unknown")
                
                msg = f"✅ OK Pixabay Passed\n👤 User: {user}\n🖼️ Image: {image_url[:100]}..."
                send_telegram(msg)
                print(msg)
                return 0
            else:
                msg = f"✅ OK Pixabay Passed (no photos found)"
                send_telegram(msg)
                print(msg)
                return 0
        else:
            msg = f"❌ FAIL Pixabay: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
    except Exception as e:
        msg = f"❌ ERR Pixabay: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1

if __name__ == "__main__":
    print("═" * 60)
    print("🖼️ Pixabay Test — Air Mode")
    print("═" * 60)
    sys.exit(test_pixabay())
