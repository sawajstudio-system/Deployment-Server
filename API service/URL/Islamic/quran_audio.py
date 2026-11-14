#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FOLDER: Islamic
# 📄 FILE  : quran_audio.py
# 📍 PATH  : Backend/System_room/URL_room/Islamic/quran_audio.py
# ══════════════════════════════════════════════════════════════════════════════
import os, sys, requests

TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"

# EveryAyah Audio CDN (Bina Key ke)
# Format: https://everyayah.com/data/{Reciter}/{Surah}{Ayah}.mp3
# Hum Mishary Rashid Alafasy ki Surah Al-Fatiha (001) ki pehli Ayat (001) le rahe hain
AUDIO_URL = "https://everyayah.com/data/Alafasy_128kbps/001001.mp3"

def send_telegram_audio(audio_url, caption):
    tok, chat = os.getenv(TG_TOKEN_ENV), os.getenv(TG_CHAT_ENV)
    if not tok or not chat: return
    try:
        # Audio ko download karke Telegram par bhejein
        audio_data = requests.get(audio_url, timeout=30).content
        requests.post(
            f"https://api.telegram.org/bot{tok}/sendAudio", 
            data={"chat_id": chat, "caption": caption}, 
            files={"audio": ("quran.mp3", audio_data)}, 
            timeout=30
        )
    except Exception as e:
        print(f"[telegram error] {e}")

def test_quran_audio():
    print(f"[quran_audio] Fetching: {AUDIO_URL}")
    try:
        r = requests.head(AUDIO_URL, timeout=30)
        if r.status_code == 200:
            print("✅ Audio file mil gayi!")
            send_telegram_audio(AUDIO_URL, "✅ OK Quran Audio Passed\n🎧 Surah Al-Fatiha (Ayah 1) - Mishary Alafasy")
            return 0
        else:
            print(f"❌ FAIL Quran Audio: HTTP {r.status_code}")
            return 1
    except Exception as e:
        print(f"❌ ERR Quran Audio: {e}")
        return 1

if __name__ == "__main__": sys.exit(test_quran_audio())
