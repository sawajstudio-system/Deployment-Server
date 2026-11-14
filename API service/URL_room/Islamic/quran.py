#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FOLDER: Islamic
# 📄 FILE  : quran.py
# 📍 PATH  : Backend/System_room/URL_room/Islamic/quran.py
# ══════════════════════════════════════════════════════════════════════════════
import os, sys, requests

TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"
# AlQuran Cloud API (Free, No Key)
API_URL = "https://api.alquran.cloud/v1/ayah/2:255/en.asad"

def send_telegram(text):
    tok, chat = os.getenv(TG_TOKEN_ENV), os.getenv(TG_CHAT_ENV)
    if not tok or not chat: return
    try: requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": chat, "text": text[:4000]}, timeout=15)
    except Exception: pass

def test_quran():
    print(f"[quran] calling: {API_URL}")
    try:
        r = requests.get(API_URL, timeout=30)
        if r.status_code == 200:
            data = r.json().get("data", {})
            english_text = data.get("text", "No text")
            surah_name = data.get("surah", {}).get("englishName", "Unknown")
            ayah_num = data.get("numberInSurah", "Unknown")
            
            msg = f"✅ OK Quran Passed\n📖 Surah: {surah_name} (Ayah {ayah_num})\n📜 Text: {english_text[:300]}..."
            send_telegram(msg)
            return 0
        else:
            send_telegram(f"❌ FAIL Quran: HTTP {r.status_code}")
            return 1
    except Exception as e:
        send_telegram(f"❌ ERR Quran: {e}")
        return 1

if __name__ == "__main__": sys.exit(test_quran())
