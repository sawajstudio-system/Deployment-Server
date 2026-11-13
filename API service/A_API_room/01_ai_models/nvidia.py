#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/A_API_room/01_ai_models/nvidia.py
# ══════════════════════════════════════════════════════════════════════════════
"""
NVIDIA NIM API Test — Air Mode (Fixed for Nemotron reasoning_content)
"""
import os
import sys
import requests


# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY_ENV  = "NVIDIA_API_KEY"
API_URL      = "https://integrate.api.nvidia.com/v1/chat/completions"
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


# ── NVIDIA TEST ─────────────────────────────────────────────────────────────
def test_nvidia():
    key = os.getenv(API_KEY_ENV)
    if not key:
        msg = f"⚠️ WARN NVIDIA: {API_KEY_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    # Nemotron Ultra model
    payload = {
        "model": "nvidia/nemotron-3-ultra-550b-a55b",
        "messages": [{"role": "user", "content": "Say exactly: NVIDIA is working!"}],
        "max_tokens": 20
    }

    print(f"[nvidia] calling: {API_URL}")
    print(f"[nvidia] model: {payload['model']}")

    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        print(f"[nvidia] HTTP {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            msg_obj = data.get("choices", [{}])[0].get("message", {})
            
            # ✅ FIX: content None ho sakta hai, reasoning_content check karo
            reply = (msg_obj.get("content") or msg_obj.get("reasoning_content") or "").strip()
            model_used = data.get("model", "unknown")
            
            msg = f"✅ OK NVIDIA Passed\n🤖 Model: {model_used}\n💬 Reply: {reply}"
            send_telegram(msg)
            print(msg)
            return 0
        else:
            msg = f"❌ FAIL NVIDIA: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
    except Exception as e:
        msg = f"❌ ERR NVIDIA: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1


# ── MAIN ────────────────────────────────────────────────────────────────────
def main():
    print("═" * 60)
    print("🟢 NVIDIA Test — Air Mode")
    print("═" * 60)
    print(f"Python: {sys.version.split()[0]}")
    print(f"NVIDIA_API_KEY: {'SET' if os.getenv(API_KEY_ENV) else 'MISSING'}")
    print("═" * 60)

    code = test_nvidia()
    print("═" * 60)
    sys.exit(code)


if __name__ == "__main__":
    main()
