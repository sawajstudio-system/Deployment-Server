#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/A_API_room/01_ai_models/groq.py
# ══════════════════════════════════════════════════════════════════════════════
"""
Groq API Test — Air Mode
"""
import os
import sys
import requests


# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY_ENV  = "GROQ_API_KEY"
API_URL      = "https://api.groq.com/openai/v1/chat/completions"
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


# ── GROQ TEST ───────────────────────────────────────────────────────────────
def test_groq():
    key = os.getenv(API_KEY_ENV)
    if not key:
        msg = f"⚠️ WARN Groq: {API_KEY_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    # Groq API Headers
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    # Groq API Payload (Latest working model - openai/gpt-oss-120b)
    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [{"role": "user", "content": "Say exactly: Groq is working!"}],
        "max_tokens": 20
    }

    print(f"[groq] calling: {API_URL}")
    print(f"[groq] model: {payload['model']}")

    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        print(f"[groq] HTTP {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            reply = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            model_used = data.get("model", "unknown")
            
            msg = f"✅ OK Groq Passed\n🤖 Model: {model_used}\n💬 Reply: {reply}"
            send_telegram(msg)
            print(msg)
            return 0
        else:
            msg = f"❌ FAIL Groq: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
    except Exception as e:
        msg = f"❌ ERR Groq: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1


# ── MAIN ────────────────────────────────────────────────────────────────────
def main():
    print("═" * 60)
    print("⚡ Groq Test — Air Mode")
    print("═" * 60)
    print(f"Python: {sys.version.split()[0]}")
    print(f"GROQ_API_KEY: {'SET' if os.getenv(API_KEY_ENV) else 'MISSING'}")
    print("═" * 60)

    code = test_groq()
    print("═" * 60)
    sys.exit(code)


if __name__ == "__main__":
    main()
