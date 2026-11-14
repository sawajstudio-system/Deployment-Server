#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FOLDER: Islamic
# 📄 FILE  : hadees.py
# 📍 PATH  : Backend/System_room/URL_room/Islamic/hadees.py
# ══════════════════════════════════════════════════════════════════════════════
import os, sys, requests

TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"
# ✅ Nayi Active API (Fawaz Ahmed Hadith API)
API_URL = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/eng-bukhari.json"

def send_telegram(text):
    tok, chat = os.getenv(TG_TOKEN_ENV), os.getenv(TG_CHAT_ENV)
    if not tok or not chat: return
    try: requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": chat, "text": text[:4000]}, timeout=15)
    except Exception: pass

def test_hadees():
    print(f"[hadees] calling: {API_URL}")
    try:
        r = requests.get(API_URL, timeout=30)
        if r.status_code == 200:
            data = r.json()
            # Is API mein data 'hadiths' array ke andar hota hai
            hadiths = data.get("hadiths", [])
            if hadiths:
                # Pehli hadith uthate hain
                first_hadith = hadiths[0]
                text = first_hadith.get("text", "No text found")
                send_telegram(f"✅ OK Hadees Passed\n📖 {text[:300]}...")
                return 0
            else:
                send_telegram("❌ FAIL Hadees: No hadiths found in response")
                return 1
        else:
            send_telegram(f"❌ FAIL Hadees: HTTP {r.status_code}")
            return 1
    except Exception as e:
        send_telegram(f"❌ ERR Hadees: {e}")
        return 1

if __name__ == "__main__": sys.exit(test_hadees())
