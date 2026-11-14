#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FOLDER: Islamic
# 📄 FILE  : UMMAH.py
# 📍 PATH  : Backend/System_room/A_API_room/Islamic/UMMAH.py
# ══════════════════════════════════════════════════════════════════════════════
import os, sys, requests

TG_TOKEN_ENV  = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV   = "TELEGRAM_API_REPORT_CHAT_ID"
UMMAH_KEY_ENV = "UMMAH_API_KEY"

API_URL = "https://ummahapi.com/api/duas/random"

def send_telegram(text):
    tok, chat = os.getenv(TG_TOKEN_ENV), os.getenv(TG_CHAT_ENV)
    if not tok or not chat: return
    try: requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": chat, "text": text[:4000]}, timeout=15)
    except Exception: pass

def test_ummah():
    api_key = os.getenv(UMMAH_KEY_ENV)
    headers = {"X-API-Key": api_key} if api_key else {}

    print(f"[UMMAH] calling: {API_URL}")
    try:
        r = requests.get(API_URL, headers=headers, timeout=30)
        if r.status_code == 200:
            data = r.json().get("data", {})
            arabic = data.get("arabic", "N/A")
            english = data.get("translation", "N/A")
            reference = data.get("reference", "N/A")
            
            msg = (f"✅ OK UMMAH (Duas) Passed\n"
                   f"🕌 Arabic: {arabic[:150]}...\n"
                   f"🇬🇧 English: {english[:150]}...\n"
                   f"📖 Ref: {reference}")
            send_telegram(msg)
            return 0
        else:
            send_telegram(f"❌ FAIL UMMAH: HTTP {r.status_code}")
            return 1
    except Exception as e:
        send_telegram(f"❌ ERR UMMAH: {e}")
        return 1

if __name__ == "__main__": sys.exit(test_ummah())
