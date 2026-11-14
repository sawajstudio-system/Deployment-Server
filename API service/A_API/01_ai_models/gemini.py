#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/API_room/01_ai_models/gemini.py
#
# ⚠️ AGAR Backend mein folder "A_API_room" hai to:
#    Backend/System_room/A_API_room/01_ai_models/gemini.py
#    (YAML mein bhi path badalna hoga — wahan comment diya hai)
# ══════════════════════════════════════════════════════════════════════════════
"""
Google Gemini API Test — Air Mode (single file, self-diagnosing)
"""
import os
import sys
import requests


# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY_ENV  = "GEMINI_API_KEY"
API_URL      = "https://generativelanguage.googleapis.com/v1beta/models"
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


# ── GEMINI TEST ─────────────────────────────────────────────────────────────
def test_gemini():
    key = os.getenv(API_KEY_ENV)
    if not key:
        msg = f"⚠️ WARN Gemini: {API_KEY_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    url = f"{API_URL}?key={key}"
    print(f"[gemini] calling: {API_URL}")

    try:
        r = requests.get(url, timeout=30)
        print(f"[gemini] HTTP {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            models = data.get("models", [])
            msg = f"✅ OK Gemini Passed — {len(models)} models available"
            if models:
                names = [m.get("name", "?").replace("models/", "") for m in models[:3]]
                msg += f"\nSample: {', '.join(names)}"
            send_telegram(msg)
            print(msg)
            return 0
        else:
            msg = f"❌ FAIL Gemini: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
    except Exception as e:
        msg = f"❌ ERR Gemini: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1


# ── MAIN ────────────────────────────────────────────────────────────────────
def main():
    print("═" * 60)
    print("🪶 Gemini Test — Air Mode")
    print("═" * 60)
    print(f"Python: {sys.version.split()[0]}")
    print(f"GEMINI_API_KEY: {'SET' if os.getenv(API_KEY_ENV) else 'MISSING'}")
    print(f"TG_TOKEN: {'SET' if os.getenv(TG_TOKEN_ENV) else 'MISSING'}")
    print(f"TG_CHAT: {'SET' if os.getenv(TG_CHAT_ENV) else 'MISSING'}")
    print("═" * 60)

    code = test_gemini()
    print("═" * 60)
    sys.exit(code)


if __name__ == "__main__":
    main()
