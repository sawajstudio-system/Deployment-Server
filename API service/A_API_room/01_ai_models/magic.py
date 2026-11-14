#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/A_API_room/01_ai_models/magic.py
#
# ✅ LIVE DOCS VERIFIED (docs.magichour.ai)
# ══════════════════════════════════════════════════════════════════════════════
"""
MagicHour (Magic) API Test — Air Mode
"""
import os
import sys
import requests


# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY_ENV  = "MAGICHOUR_API_KEY"
# ✅ Sahi Endpoint (Docs ke mutabiq)
API_URL      = "https://api.magichour.ai/v1/ai-image-generator"
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


# ── MAGIC TEST ──────────────────────────────────────────────────────────────
def test_magic():
    key = os.getenv(API_KEY_ENV)
    if not key:
        msg = f"⚠️ WARN Magic: {API_KEY_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    # ✅ Official Docs Payload (ai-image-generator ke liye)
    payload = {
        "name": "API Test Generation",
        "image_count": 1,
        "model": "z-image-turbo",
        "aspect_ratio": "1:1",
        "resolution": "640px",
        "style": {
            "prompt": "A cute cat sitting on a table, highly detailed, 4k",
            "tool": "ai-anime-generator"
        }
    }

    print(f"[magic] calling: {API_URL}")

    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        print(f"[magic] HTTP {r.status_code}")

        if r.status_code in (200, 201, 202):
            data = r.json()
            project_id = data.get("id", "unknown")
            
            msg = f"✅ OK Magic Passed\n🪄 Project ID: {project_id}\n💬 Status: {data.get('status', 'created')}"
            send_telegram(msg)
            print(msg)
            return 0
        else:
            msg = f"❌ FAIL Magic: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
    except Exception as e:
        msg = f"❌ ERR Magic: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1


# ── MAIN ────────────────────────────────────────────────────────────────────
def main():
    print("═" * 60)
    print("🪄 Magic (MagicHour) Test — Air Mode")
    print("═" * 60)
    print(f"Python: {sys.version.split()[0]}")
    print(f"MAGICHOUR_API_KEY: {'SET' if os.getenv(API_KEY_ENV) else 'MISSING'}")
    print("═" * 60)

    code = test_magic()
    print("═" * 60)
    sys.exit(code)


if __name__ == "__main__":
    main()
