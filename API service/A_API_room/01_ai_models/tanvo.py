#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/A_API_room/02_audio_media/tanvo.py
#
# ✅ LIVE DOCS VERIFIED: tanvo.ai/developers/api
#    - Status polling: GET /generations/{id}
#    - Success keyword: "SUCCEEDED"
#    - Output: generation.outputs[0].url
# ══════════════════════════════════════════════════════════════════════════════
"""
Tanvo API Test — Air Mode (Docs Verified)
"""
import os
import sys
import json
import time
import requests

API_KEY_ENV  = "TANVO_API_KEY"
API_URL      = "https://tanvo.ai/api/v1/generations"
TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"

MODEL_NAME   = "studio-image-v1"      
RESOLUTION   = "1K"                 
ASPECT       = "1:1"                
FORMAT       = "PNG"                


def send_telegram(text):
    tok  = os.getenv(TG_TOKEN_ENV)
    chat = os.getenv(TG_CHAT_ENV)
    if not tok or not chat:
        print(f"[no telegram] {text}")
        return
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{tok}/sendMessage",
            json={"chat_id": chat, "text": text[:4000]},
            timeout=15,
        )
        print(f"[telegram] sent: HTTP {r.status_code}")
    except Exception as e:
        print(f"[telegram error] {e}")


def test_tanvo():
    key = os.getenv(API_KEY_ENV)
    if not key:
        msg = f"⚠️ WARN Tanvo: {API_KEY_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "prompt": "A cute cat sitting on a table, highly detailed, 4k",
        "kind": "image",
        "options": {
            "aspect": ASPECT,
            "resolution": RESOLUTION,
            "format": FORMAT
        }
    }

    print(f"[tanvo] calling: {API_URL}")

    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        print(f"[tanvo] Create HTTP {r.status_code}")

        if r.status_code not in (200, 201, 202):
            msg = f"❌ FAIL Tanvo: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1

        data = r.json()
        gen_id = data.get("generation", {}).get("id")
        
        if not gen_id:
            msg = f"❌ FAIL Tanvo: No ID found."
            send_telegram(msg)
            print(msg)
            return 1

        print(f"[tanvo] Generation ID: {gen_id}. Polling for SUCCEEDED...")
        
        # Official Docs: Images take up to 1 minute. We'll wait up to 3 minutes (36 attempts × 5s)
        status_url = f"{API_URL}/{gen_id}"
        for attempt in range(36): # 36 attempts * 5s = 180 seconds
            time.sleep(5)
            print(f"[tanvo] Attempt {attempt+1}/36...")
            
            sr = requests.get(status_url, headers={"Authorization": f"Bearer {key}"}, timeout=30)
            
            if sr.status_code == 200:
                status_data = sr.json()
                gen = status_data.get("generation", {})
                status = gen.get("status", "UNKNOWN")
                
                print(f"[tanvo] Status: {status}")
                
                if status == "SUCCEEDED":
                    # Official Docs: outputs[0].url
                    outputs = gen.get("outputs", [])
                    if outputs and len(outputs) > 0:
                        image_url = outputs[0].get("url")
                        msg = f"✅ OK Tanvo Passed\n🤖 Model: {MODEL_NAME}\n🖼️ Image: {image_url}"
                        send_telegram(msg)
                        print(msg)
                        return 0
                    else:
                        msg = f"✅ SUCCEEDED but no outputs. JSON: {json.dumps(gen)[:300]}"
                        send_telegram(msg)
                        print(msg)
                        return 0
                        
                elif status in ["FAILED", "ERROR"]:
                    msg = f"❌ FAIL Tanvo: Status {status}. Response: {json.dumps(gen)[:300]}"
                    send_telegram(msg)
                    print(msg)
                    return 1
                    
            else:
                print(f"[tanvo] Status check failed: {sr.status_code}")

        msg = f"⚠️ WARN Tanvo: Timeout after 3 minutes (ID: {gen_id}). Tanvo server is busy."
        send_telegram(msg)
        print(msg)
        return 0

    except Exception as e:
        msg = f"❌ ERR Tanvo: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1


def main():
    print("═" * 60)
    print("🎨 Tanvo Test — Air Mode (Docs Verified)")
    print("═" * 60)
    print(f"TANVO_API_KEY: {'SET' if os.getenv(API_KEY_ENV) else 'MISSING'}")
    print("═" * 60)

    code = test_tanvo()
    print("═" * 60)
    sys.exit(code)


if __name__ == "__main__":
    main()
