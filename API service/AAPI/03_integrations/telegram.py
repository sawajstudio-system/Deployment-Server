#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/A_API_room/03_integrations/telegram.py
# ══════════════════════════════════════════════════════════════════════════════
"""
Telegram Bot API Test — Air Mode
"""
import os
import sys
import requests

# ── CONFIG ──────────────────────────────────────────────────────────────────
# Hum wahi token use kar rahe hain jo report bhejne ke liye use hota hai
BOT_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN" 
API_URL       = "https://api.telegram.org"
TG_TOKEN_ENV  = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV   = "TELEGRAM_API_REPORT_CHAT_ID"

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

# ── TELEGRAM BOT TEST ───────────────────────────────────────────────────────
def test_telegram():
    bot_token = os.getenv(BOT_TOKEN_ENV)
    if not bot_token:
        msg = f"⚠️ WARN Telegram: {BOT_TOKEN_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    url = f"{API_URL}/bot{bot_token}/getMe"

    print(f"[telegram] calling: getMe API")

    try:
        r = requests.get(url, timeout=30)
        print(f"[telegram] HTTP {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            if data.get("ok"):
                bot_info = data.get("result", {})
                username = bot_info.get("username", "unknown")
                first_name = bot_info.get("first_name", "")
                
                msg = f"✅ OK Telegram Bot Passed\n🤖 Bot: @{username}\n📛 Name: {first_name}"
                send_telegram(msg)
                print(msg)
                return 0
            else:
                msg = f"❌ FAIL Telegram Bot: API returned ok=false"
                send_telegram(msg)
                print(msg)
                return 1
        else:
            msg = f"❌ FAIL Telegram Bot: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
    except Exception as e:
        msg = f"❌ ERR Telegram Bot: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1

# ── MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("═" * 60)
    print("📱 Telegram Bot Test — Air Mode")
    print("═" * 60)
    code = test_telegram()
    sys.exit(code)
