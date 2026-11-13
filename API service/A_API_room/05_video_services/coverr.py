#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/A_API_room/05_video_services/coverr.py
# ══════════════════════════════════════════════════════════════════════════════
"""
Coverr API Test — Air Mode
"""
import os
import sys
import requests

API_KEY_ENV  = "COVERR_API_KEY"
API_URL      = "https://api.coverr.co/videos?query=nature&page_size=1"
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

def test_coverr():
    key = os.getenv(API_KEY_ENV)
    if not key:
        msg = f"⚠️ WARN Coverr: {API_KEY_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    headers = {"Authorization": f"Bearer {key}"}

    print(f"[coverr] calling: {API_URL}")

    try:
        r = requests.get(API_URL, headers=headers, timeout=30)
        print(f"[coverr] HTTP {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            hits = data.get("hits", [])
            if hits:
                msg = f"✅ OK Coverr Passed\n🎬 Video found: {hits[0].get('title', 'Unknown')}"
                send_telegram(msg)
                print(msg)
                return 0
            msg = "✅ OK Coverr Passed (no videos found)"
            send_telegram(msg)
            print(msg)
            return 0
        else:
            msg = f"❌ FAIL Coverr: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
    except Exception as e:
        msg = f"❌ ERR Coverr: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1

if __name__ == "__main__":
    print("═" * 60)
    print("🎬 Coverr Test — Air Mode")
    print("═" * 60)
    sys.exit(test_coverr())
