#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/A_API_room/01_ai_models/cohere.py
# ══════════════════════════════════════════════════════════════════════════════
"""
Cohere API Test — Air Mode
"""
import os
import sys
import requests


# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY_ENV  = "COHERE_API_KEY"
API_URL      = "https://api.cohere.com/v2/chat"
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


# ── COHERE TEST ─────────────────────────────────────────────────────────────
def test_cohere():
    key = os.getenv(API_KEY_ENV)
    if not key:
        msg = f"⚠️ WARN Cohere: {API_KEY_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    # Cohere latest model
    payload = {
        "model": "command-a-03-2025",
        "messages": [{"role": "user", "content": "Say exactly: Cohere is working!"}],
        "max_tokens": 20
    }

    print(f"[cohere] calling: {API_URL}")
    print(f"[cohere] model: {payload['model']}")

    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        print(f"[cohere] HTTP {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            # Cohere v2 response format
            reply = data.get("message", {}).get("content", [{}])[0].get("text", "").strip()
            model_used = data.get("model", "unknown")
            
            msg = f"✅ OK Cohere Passed\n🤖 Model: {model_used}\n💬 Reply: {reply}"
            send_telegram(msg)
            print(msg)
            return 0
        else:
            msg = f"❌ FAIL Cohere: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
    except Exception as e:
        msg = f"❌ ERR Cohere: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1


# ── MAIN ────────────────────────────────────────────────────────────────────
def main():
    print("═" * 60)
    print("🧠 Cohere Test — Air Mode")
    print("═" * 60)
    print(f"Python: {sys.version.split()[0]}")
    print(f"COHERE_API_KEY: {'SET' if os.getenv(API_KEY_ENV) else 'MISSING'}")
    print("═" * 60)

    code = test_cohere()
    print("═" * 60)
    sys.exit(code)


if __name__ == "__main__":
    main()
