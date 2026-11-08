#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Islamic/Quran/API_fallback/quran_foundation.py
# 🎯 PURPOSE: Quran Foundation API का उपयोग करके सूरह का डेटा लाना
# ✅ SELF-CONTAINED: अगर API फेल होगी, तो None रिटर्न करेगा ताकि URL_fallback चल सके।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

def fetch(chapter_id=1):
    """
    Quran Foundation से सूरह का डेटा लाएगा।
    """
    client_id = os.getenv("QF_CLIENT_ID")
    client_secret = os.getenv("QF_CLIENT_SECRET")
    qf_env = os.getenv("QF_ENV", "production")

    if not client_id or not client_secret:
        print("[quran_foundation] ⚠️ QF_CLIENT_ID या QF_CLIENT_SECRET missing")
        return None

    print(f"[quran_foundation] 📖 Fetching Surah {chapter_id} from {qf_env}...")

    # 1. Environment के हिसाब से URL सेट करो
    if qf_env.lower() == "prelive":
        auth_url = "https://prelive-oauth2.quran.foundation/oauth2/token"
        api_base = "https://apis-prelive.quran.foundation/content/api/v4"
    else:
        auth_url = "https://oauth2.quran.foundation/oauth2/token"
        api_base = "https://apis.quran.foundation/content/api/v4"

    try:
        # 2. पहले OAuth2 टोकन लो
        token_res = requests.post(
            auth_url,
            auth=(client_id, client_secret),
            data={"grant_type": "client_credentials", "scope": "content"},
            timeout=15
        )
        
        if token_res.status_code != 200:
            print(f"[quran_foundation] ❌ Auth Failed: HTTP {token_res.status_code}")
            return None

        access_token = token_res.json().get("access_token")
        
        # 3. टोकन का इस्तेमाल करके डेटा फेच करो
        api_url = f"{api_base}/chapters/{chapter_id}"
        headers = {
            "x-auth-token": access_token,
            "x-client-id": client_id
        }

        r = requests.get(api_url, headers=headers, timeout=15)
        
        if r.status_code == 200:
            chapter_data = r.json().get("chapter", {})
            print(f"[quran_foundation] ✅ Success: {chapter_data.get('name_simple')}")
            return chapter_data
        else:
            print(f"[quran_foundation] ❌ Failed: HTTP {r.status_code}")
            return None

    except Exception as e:
        print(f"[quran_foundation] ❌ Error: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("📖 Quran Foundation Test")
    print("═" * 50)
    res = fetch(1)
    if res:
        print(f"Name: {res.get('name_simple')}")
        print(f"Verses: {res.get('verses_count')}")
    print("═" * 50)
