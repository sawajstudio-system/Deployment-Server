#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FOLDER: Other
# 📄 FILE  : translator.py
# 📍 PATH  : Backend/System_room/URL_room/Other/translator.py
# ══════════════════════════════════════════════════════════════════════════════
import os, sys, requests

TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"
# MyMemory API (Free, No Key required for basic use)
API_URL = "https://api.mymemory.translated.net/get"

def send_telegram(text):
    tok, chat = os.getenv(TG_TOKEN_ENV), os.getenv(TG_CHAT_ENV)
    if not tok or not chat: return
    try: requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": chat, "text": text[:4000]}, timeout=15)
    except Exception: pass

def test_translator():
    # Test 1: Hindi to English
    hindi_text = "नमस्ते, आप कैसे हैं?"
    print(f"[translator] Translating Hindi to English: {hindi_text}")
    try:
        r = requests.get(API_URL, params={"q": hindi_text, "langpair": "hi|en"}, timeout=30)
        if r.status_code == 200:
            data = r.json()
            english_text = data.get("responseData", {}).get("translatedText", "No translation")
            
            # Test 2: English to Hindi (using the translated text)
            print(f"[translator] Translating English to Hindi: {english_text}")
            r2 = requests.get(API_URL, params={"q": english_text, "langpair": "en|hi"}, timeout=30)
            if r2.status_code == 200:
                data2 = r2.json()
                final_hindi = data2.get("responseData", {}).get("translatedText", "No translation")
                
                msg = (f"✅ OK Translator Passed\n"
                       f"🇮🇳 Original: {hindi_text}\n"
                       f"🇬🇧 English: {english_text}\n"
                       f"🇮🇳 Back to Hindi: {final_hindi}")
                send_telegram(msg)
                return 0
            else:
                send_telegram(f"❌ FAIL Translator (English->Hindi): HTTP {r2.status_code}")
                return 1
        else:
            send_telegram(f"❌ FAIL Translator (Hindi->English): HTTP {r.status_code}")
            return 1
    except Exception as e:
        send_telegram(f"❌ ERR Translator: {e}")
        return 1

if __name__ == "__main__": sys.exit(test_translator())
