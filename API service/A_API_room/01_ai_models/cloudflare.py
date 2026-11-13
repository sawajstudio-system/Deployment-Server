#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/A_API_room/01_ai_models/cloudflare.py
# ══════════════════════════════════════════════════════════════════════════════
"""
Cloudflare Workers AI Test — Air Mode (Latest Model)
"""
import os
import sys
import requests


# ── CONFIG ──────────────────────────────────────────────────────────────────
ACC_ENV      = "CLOUDFLARE_ACCOUNT_ID"
TOKEN_ENV    = "CLOUDFLARE_API_TOKEN"
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


# ── CLOUDFLARE TEST ─────────────────────────────────────────────────────────
def test_cloudflare():
    acc   = os.getenv(ACC_ENV)
    token = os.getenv(TOKEN_ENV)

    if not acc or not token:
        msg = f"⚠️ WARN Cloudflare: {ACC_ENV} ya {TOKEN_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    # ✅ Latest Working Model: Llama 3.3 70B Fast
    model = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
    url = f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/{model}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [{"role": "user", "content": "Say exactly: Cloudflare is working!"}],
        "max_tokens": 20
    }

    print(f"[cloudflare] calling: {url}")
    print(f"[cloudflare] model: {model}")

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"[cloudflare] HTTP {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            # Cloudflare response format
            reply = data.get("result", {}).get("response", "").strip()
            
            msg = f"✅ OK Cloudflare Passed\n🤖 Model: {model}\n💬 Reply: {reply}"
            send_telegram(msg)
            print(msg)
            return 0
        else:
            msg = f"❌ FAIL Cloudflare: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
    except Exception as e:
        msg = f"❌ ERR Cloudflare: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1


# ── MAIN ────────────────────────────────────────────────────────────────────
def main():
    print("═" * 60)
    print("☁️ Cloudflare Test — Air Mode")
    print("═" * 60)
    print(f"ACCOUNT_ID: {'SET' if os.getenv(ACC_ENV) else 'MISSING'}")
    print(f"API_TOKEN:  {'SET' if os.getenv(TOKEN_ENV) else 'MISSING'}")
    print("═" * 60)

    code = test_cloudflare()
    print("═" * 60)
    sys.exit(code)


if __name__ == "__main__":
    main()
