#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/A_API_room/05_video_services/pexels.py
# ══════════════════════════════════════════════════════════════════════════════
"""
Pexels API Test — Air Mode (Photo Search)
Docs: https://www.pexels.com/api/documentation/
"""
import os
import sys
import requests

# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY_ENV  = "PEXELS_API_KEY"
API_URL      = "https://api.pexels.com/v1/search"
TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"

# ── TELEGRAM ────────────────────────────────────────────────────────────────
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

# ── PEXELS TEST ─────────────────────────────────────────────────────────────
def test_pexels():
    key = os.getenv(API_KEY_ENV)
    if not key:
        msg = f"⚠️ WARN Pexels: {API_KEY_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    # Pexels requires the API key directly in the Authorization header (no Bearer prefix)
    headers = {
        "Authorization": key
    }
    
    params = {
        "query": "nature",
        "per_page": 1
    }

    print(f"[pexels] calling: {API_URL}")

    try:
        r = requests.get(API_URL, headers=headers, params=params, timeout=30)
        print(f"[pexels] HTTP {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            photos = data.get("photos", [])
            
            if photos:
                photo = photos[0]
                image_url = photo.get("src", {}).get("original", "")
                photographer = photo.get("photographer", "unknown")
                
                msg = f"✅ OK Pexels Passed\n📸 Photographer: {photographer}\n🖼️ Image: {image_url[:100]}..."
                send_telegram(msg)
                print(msg)
                return 0
            else:
                msg = f"✅ OK Pexels Passed (no photos found)"
                send_telegram(msg)
                print(msg)
                return 0
        else:
            msg = f"❌ FAIL Pexels: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
    except Exception as e:
        msg = f"❌ ERR Pexels: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1

# ── MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("═" * 60)
    print("🎬 Pexels Test — Air Mode")
    print("═" * 60)
    code = test_pexels()
    sys.exit(code)
