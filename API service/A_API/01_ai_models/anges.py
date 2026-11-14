#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/A_API_room/01_ai_models/anges.py
# ══════════════════════════════════════════════════════════════════════════════
"""
Anges AI API Test — Air Mode
"""
import os
import sys
import requests


# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY_ENV  = "ANGES_API_KEY"
API_URL      = "https://apihub.agnes-ai.com/v1/chat/completions"
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


# ── ANGES TEST ──────────────────────────────────────────────────────────────
def test_anges():
    key = os.getenv(API_KEY_ENV)
    if not key:
        msg = f"⚠️ WARN Anges: {API_KEY_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    # Anges model
    payload = {
        "model": "agnes-2.5-flash",
        "messages": [{"role": "user", "content": "Say exactly: Anges is working!"}],
        "max_tokens": 20
    }

    print(f"[anges] calling: {API_URL}")
    print(f"[anges] model: {payload['model']}")

    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        print(f"[anges] HTTP {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            reply = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            model_used = data.get("model", "unknown")
            
            msg = f"✅ OK Anges Passed\n🤖 Model: {model_used}\n💬 Reply: {reply}"
            send_telegram(msg)
            print(msg)
            return 0
        else:
            msg = f"❌ FAIL Anges: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
    except Exception as e:
        msg = f"❌ ERR Anges: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1


# ── MAIN ────────────────────────────────────────────────────────────────────
def main():
    print("═" * 60)
    print("🅰️ Anges Test — Air Mode")
    print("═" * 60)
    print(f"Python: {sys.version.split()[0]}")
    print(f"ANGES_API_KEY: {'SET' if os.getenv(API_KEY_ENV) else 'MISSING'}")
    print("═" * 60)

    code = test_anges()
    print("═" * 60)
    sys.exit(code)


if __name__ == "__main__":
    main()
