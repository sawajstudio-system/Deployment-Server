#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/A_API_room/02_audio_media/cloudinary.py
# ══════════════════════════════════════════════════════════════════════════════
"""
Cloudinary API Test — Air Mode
Docs: https://cloudinary.com/documentation/admin_api
"""
import os
import sys
import base64
import requests

# ── CONFIG ──────────────────────────────────────────────────────────────────
CLOUD_NAME_ENV = "CLOUDINARY_CLOUD_NAME"
API_KEY_ENV    = "CLOUDINARY_API_KEY"
API_SECRET_ENV = "CLOUDINARY_API_SECRET"
TG_TOKEN_ENV   = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV    = "TELEGRAM_API_REPORT_CHAT_ID"

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

# ── CLOUDINARY TEST ─────────────────────────────────────────────────────────
def test_cloudinary():
    cloud_name = os.getenv(CLOUD_NAME_ENV)
    api_key    = os.getenv(API_KEY_ENV)
    api_secret = os.getenv(API_SECRET_ENV)

    if not cloud_name or not api_key or not api_secret:
        msg = "⚠️ WARN Cloudinary: Keys missing"
        send_telegram(msg)
        print(msg)
        return 2

    # Cloudinary uses Basic Auth (base64 of api_key:api_secret)
    auth_str = f"{api_key}:{api_secret}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    
    url = f"https://api.cloudinary.com/v1_1/{cloud_name}/usage"
    headers = {"Authorization": f"Basic {auth_b64}"}

    print(f"[cloudinary] calling: {url}")

    try:
        r = requests.get(url, headers=headers, timeout=30)
        print(f"[cloudinary] HTTP {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            plan = data.get("plan", "unknown")
            
            msg = f"✅ OK Cloudinary Passed\n📦 Plan: {plan}"
            send_telegram(msg)
            print(msg)
            return 0
        else:
            msg = f"❌ FAIL Cloudinary: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
    except Exception as e:
        msg = f"❌ ERR Cloudinary: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1

# ── MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("═" * 60)
    print("📸 Cloudinary Test — Air Mode")
    print("═" * 60)
    code = test_cloudinary()
    sys.exit(code)
