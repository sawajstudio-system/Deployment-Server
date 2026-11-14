#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/A_API_room/02_audio_media/elevenlabs_test.py
# 🎯 PURPOSE: ElevenLabs API Test (Voice Generation Check)
# ══════════════════════════════════════════════════════════════════════════════

import os
import sys
import requests

# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY_ENV  = "ELEVENLABS_API_KEY"
TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"

# Adam voice ID (Deep male voice)
VOICE_ID = "pNInz6obpgDQGcFmaJgB" 
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

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


# ── ELEVENLABS TEST ─────────────────────────────────────────────────────────
def test_elevenlabs():
    key = os.getenv(API_KEY_ENV)
    if not key:
        msg = f"⚠️ WARN ElevenLabs: {API_KEY_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": key
    }
    
    # Short text to save credits (only 1 char test)
    payload = {
        "text": "Test",
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    print(f"[elevenlabs] calling: {API_URL}")
    print(f"[elevenlabs] Voice ID: {VOICE_ID}")

    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        print(f"[elevenlabs] HTTP {r.status_code}")

        if r.status_code == 200 and len(r.content) > 1000:
            size_kb = len(r.content) / 1024
            msg = f"✅ OK ElevenLabs Passed\n🎙️ Voice generated ({size_kb:.1f} KB)"
            send_telegram(msg)
            print(msg)
            return 0
        else:
            msg = f"❌ FAIL ElevenLabs: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
            
    except Exception as e:
        msg = f"❌ ERR ElevenLabs: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1


# ── MAIN ────────────────────────────────────────────────────────────────────
def main():
    print("═" * 60)
    print("🎙️ ElevenLabs Test — Air Mode")
    print("═" * 60)
    print(f"Python: {sys.version.split()[0]}")
    print(f"ELEVENLABS_API_KEY: {'SET' if os.getenv(API_KEY_ENV) else 'MISSING'}")
    print("═" * 60)

    code = test_elevenlabs()
    print("═" * 60)
    sys.exit(code)


if __name__ == "__main__":
    main()
