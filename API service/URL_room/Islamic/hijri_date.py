#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FOLDER: Islamic
# 📄 FILE  : hijri_date.py
# 📍 PATH  : Backend/System_room/URL_room/Islamic/hijri_date.py
# ══════════════════════════════════════════════════════════════════════════════
import os, sys, requests

TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"

# AlAdhan API se aaj ki Hijri date (Bina Key ke)
API_URL = "https://api.aladhan.com/v1/gToH"

def send_telegram(text):
    tok, chat = os.getenv(TG_TOKEN_ENV), os.getenv(TG_CHAT_ENV)
    if not tok or not chat: return
    try: requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": chat, "text": text[:4000]}, timeout=15)
    except Exception: pass

def test_hijri():
    print(f"[hijri_date] calling: {API_URL}")
    try:
        r = requests.get(API_URL, timeout=30)
        if r.status_code == 200:
            hijri = r.json().get("data", {}).get("hijri", {})
            
            day = hijri.get("day", "N/A")
            month = hijri.get("month", {}).get("en", "N/A")
            year = hijri.get("year", "N/A")
            
            msg = f"✅ OK Hijri Date Passed\n🌙 Today's Islamic Date: {day} {month} {year} AH"
            send_telegram(msg)
            return 0
        else:
            send_telegram(f"❌ FAIL Hijri Date: HTTP {r.status_code}")
            return 1
    except Exception as e:
        send_telegram(f"❌ ERR Hijri Date: {e}")
        return 1

if __name__ == "__main__": sys.exit(test_hijri())
