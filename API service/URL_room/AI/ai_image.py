#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FOLDER: AI
# 📄 FILE  : ai_image.py
# 📍 PATH  : Backend/System_room/URL_room/AI/ai_image.py
# ══════════════════════════════════════════════════════════════════════════════
import os, sys, urllib.parse, requests

TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"

def send_telegram_photo(image_url, caption):
    tok, chat = os.getenv(TG_TOKEN_ENV), os.getenv(TG_CHAT_ENV)
    if not tok or not chat: 
        print("⚠️ Telegram token ya chat ID missing hai")
        return
    
    print("📤 Telegram par photo bheji ja rahi hai...")
    try:
        # Image ko pehle download karein
        img_data = requests.get(image_url, timeout=60).content
        
        # Fir use Telegram par photo ki tarah bhejein
        r = requests.post(
            f"https://api.telegram.org/bot{tok}/sendPhoto", 
            data={"chat_id": chat, "caption": caption[:1024]}, 
            files={"photo": ("image.jpg", img_data)}, 
            timeout=60
        )
        print(f"[telegram] Response: HTTP {r.status_code}")
        if r.status_code != 200:
            print(f"[telegram error] {r.text}")
    except Exception as e:
        print(f"[telegram error] {e}")

def test_ai_image():
    prompt = "A beautiful Islamic mosque at sunset, 4k"
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
    
    print(f"[ai_image] Generating: {prompt}")
    try:
        # Image ko generate hone ka time dein
        r = requests.get(url, timeout=90)
        if r.status_code == 200:
            print("✅ Image generate ho gayi!")
            send_telegram_photo(url, f"✅ OK AI Image Passed\n🖼️ Prompt: {prompt}")
            return 0
        else:
            print(f"❌ FAIL AI Image: HTTP {r.status_code}")
            return 1
    except Exception as e:
        print(f"❌ ERR AI Image: {e}")
        return 1

if __name__ == "__main__": sys.exit(test_ai_image())
