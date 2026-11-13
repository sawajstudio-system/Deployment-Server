#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FOLDER: Other
# 📄 FILE  : quotes.py
# 📍 PATH  : Backend/System_room/URL_room/Other/quotes.py
# ══════════════════════════════════════════════════════════════════════════════
import os, sys, requests

TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"
API_URL = "https://zenquotes.io/api/random"

def send_telegram(text):
    tok, chat = os.getenv(TG_TOKEN_ENV), os.getenv(TG_CHAT_ENV)
    if not tok or not chat: return
    try: requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": chat, "text": text[:4000]}, timeout=15)
    except Exception: pass

def test_quotes():
    print(f"[quotes] calling: {API_URL}")
    try:
        r = requests.get(API_URL, timeout=30)
        if r.status_code == 200:
            data = r.json()[0]
            send_telegram(f"✅ OK Quotes Passed\n💬 \"{data.get('q')}\"\n✍️ — {data.get('a')}")
            return 0
        else:
            send_telegram(f"❌ FAIL Quotes: HTTP {r.status_code}")
            return 1
    except Exception as e:
        send_telegram(f"❌ ERR Quotes: {e}")
        return 1

if __name__ == "__main__": sys.exit(test_quotes())
