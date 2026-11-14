#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FOLDER: Islamic
# 📄 FILE  : quran_tafsir.py
# 📍 PATH  : Backend/System_room/URL_room/Islamic/quran_tafsir.py
# ══════════════════════════════════════════════════════════════════════════════
import os, sys, requests

TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"

# Quran.com API v4 (Tafsir fetch karne ke liye)
# 169 = Tafsir Ibn Kathir (English)
API_URL = "https://api.quran.com/api/v4/tafsirs/169/by_ayah/2:255"

def send_telegram(text):
    tok, chat = os.getenv(TG_TOKEN_ENV), os.getenv(TG_CHAT_ENV)
    if not tok or not chat: return
    try: requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": chat, "text": text[:4000]}, timeout=15)
    except Exception: pass

def test_tafsir():
    print(f"[quran_tafsir] calling: {API_URL}")
    try:
        r = requests.get(API_URL, timeout=30)
        if r.status_code == 200:
            data = r.json()
            tafsir_text = data.get("tafsir", {}).get("text", "No tafsir found")
            
            # HTML tags hata kar clean text banate hain
            import re
            clean_text = re.sub('<[^<]+?>', '', tafsir_text).strip()
            
            msg = f"✅ OK Quran Tafsir Passed\n📖 Tafsir Ibn Kathir (2:255)\n📜 {clean_text[:400]}..."
            send_telegram(msg)
            return 0
        else:
            send_telegram(f"❌ FAIL Quran Tafsir: HTTP {r.status_code}")
            return 1
    except Exception as e:
        send_telegram(f"❌ ERR Quran Tafsir: {e}")
        return 1

if __name__ == "__main__": sys.exit(test_tafsir())
