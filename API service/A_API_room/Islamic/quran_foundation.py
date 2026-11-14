#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FOLDER: Islamic
# 📄 FILE  : quran_foundation.py
# 📍 PATH  : Backend/System_room/A_API_room/Islamic/quran_foundation.py
# ══════════════════════════════════════════════════════════════════════════════
import os, sys, requests

TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"
QF_ID_ENV    = "QF_CLIENT_ID"
QF_SEC_ENV   = "QF_CLIENT_SECRET"
QF_ENV       = "QF_ENV"

def send_telegram(text):
    tok, chat = os.getenv(TG_TOKEN_ENV), os.getenv(TG_CHAT_ENV)
    if not tok or not chat: return
    try: requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": chat, "text": text[:4000]}, timeout=15)
    except Exception: pass

def test_quran_foundation():
    client_id = os.getenv(QF_ID_ENV)
    client_secret = os.getenv(QF_SEC_ENV)
    env = os.getenv(QF_ENV, "production")

    if not client_id or not client_secret:
        send_telegram("⚠️ WARN: QF_CLIENT_ID ya QF_CLIENT_SECRET missing")
        return 2

    if env == "prelive":
        auth_url = "https://prelive-oauth2.quran.foundation/oauth2/token"
        api_base = "https://apis-prelive.quran.foundation/content/api/v4"
    else:
        auth_url = "https://oauth2.quran.foundation/oauth2/token"
        api_base = "https://apis.quran.foundation/content/api/v4"

    print(f"[quran_foundation] Getting OAuth2 token from {env}...")
    try:
        token_res = requests.post(
            auth_url,
            auth=(client_id, client_secret),
            data={"grant_type": "client_credentials", "scope": "content"},
            timeout=30
        )
        if token_res.status_code != 200:
            send_telegram(f"❌ FAIL Auth: HTTP {token_res.status_code} — {token_res.text[:200]}")
            return 1

        access_token = token_res.json().get("access_token")
        
        api_url = f"{api_base}/chapters/1"
        headers = {
            "x-auth-token": access_token,
            "x-client-id": client_id
        }

        print(f"[quran_foundation] Calling API: {api_url}")
        r = requests.get(api_url, headers=headers, timeout=30)
        if r.status_code == 200:
            data = r.json().get("chapter", {})
            name = data.get("name_simple", "Unknown")
            english_name = data.get("name_english", "Unknown")
            verses_count = data.get("verses_count", "Unknown")
            
            msg = f"✅ OK Quran Foundation Passed\n📖 Surah: {name} ({english_name})\n📜 Total Verses: {verses_count}"
            send_telegram(msg)
            return 0
        else:
            send_telegram(f"❌ FAIL API: HTTP {r.status_code} — {r.text[:200]}")
            return 1

    except Exception as e:
        send_telegram(f"❌ ERR Quran Foundation: {e}")
        return 1

if __name__ == "__main__": sys.exit(test_quran_foundation())
