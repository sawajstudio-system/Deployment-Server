#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FOLDER: 02_audio_media
# 📄 FILE  : natural_sound.py
# 📍 PATH  : Backend/System_room/A_API_room/02_audio_media/natural_sound.py
# ══════════════════════════════════════════════════════════════════════════════
import os, sys, requests

TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"
FS_KEY_ENV   = "FREESOUND_API_KEY"

API_URL = "https://freesound.org/apiv2/search/text/"

def send_telegram_audio(audio_url, caption):
    tok, chat = os.getenv(TG_TOKEN_ENV), os.getenv(TG_CHAT_ENV)
    if not tok or not chat: return
    try:
        audio_data = requests.get(audio_url, timeout=60).content
        requests.post(
            f"https://api.telegram.org/bot{tok}/sendAudio", 
            data={"chat_id": chat, "caption": caption}, 
            files={"audio": ("natural_sound.mp3", audio_data)}, 
            timeout=60
        )
    except Exception as e:
        print(f"[telegram error] {e}")

def test_natural_sound():
    key = os.getenv(FS_KEY_ENV)
    if not key: return 2

    params = {
        "query": "jungle nature",
        "token": key,
        "fields": "id,name,previews",
        "page_size": 1
    }

    print(f"[natural_sound] calling: {API_URL}")
    try:
        r = requests.get(API_URL, params=params, timeout=30)
        if r.status_code == 200:
            results = r.json().get("results", [])
            if results:
                sound = results[0]
                previews = sound.get("previews", {})
                audio_url = previews.get("preview-hq-mp3") or previews.get("preview-lq-mp3")
                
                if audio_url:
                    send_telegram_audio(audio_url, f"✅ OK Natural Sound Passed\n🎵 {sound.get('name')}")
                    return 0
            return 1
        return 1
    except Exception: return 1

if __name__ == "__main__": sys.exit(test_natural_sound())
