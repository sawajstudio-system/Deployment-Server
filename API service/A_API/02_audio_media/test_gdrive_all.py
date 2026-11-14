#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FOLDER: 02_audio_media
# 📄 FILE  : test_gdrive_all.py
# 📍 PATH  : Backend/System_room/A_API_room/02_audio_media/test_gdrive_all.py
# ══════════════════════════════════════════════════════════════════════════════
import os, sys, requests, json, time

TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"
CID_ENV      = "GDRIVE_CLIENT_ID"
CSEC_ENV     = "GDRIVE_CLIENT_SECRET"
RTOK_ENV     = "GDRIVE_REFRESH_TOKEN"

FOLDERS = {
    "Short": os.getenv("GDRIVE_F_SHORT_ID"),
    "Long":  os.getenv("GDRIVE_F_LONG_ID"),
    "Story": os.getenv("GDRIVE_F_STORY_ID")
}

def send_telegram(text):
    tok, chat = os.getenv(TG_TOKEN_ENV), os.getenv(TG_CHAT_ENV)
    if not tok or not chat: return
    try: requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": chat, "text": text[:4000]}, timeout=15)
    except Exception: pass

def test_all_gdrive():
    cid = os.getenv(CID_ENV)
    csec = os.getenv(CSEC_ENV)
    rtok = os.getenv(RTOK_ENV)

    if not cid or not csec or not rtok:
        send_telegram("⚠️ WARN: GDrive main credentials missing")
        return

    # 1. Get Access Token
    token_res = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": cid, "client_secret": csec, "refresh_token": rtok, "grant_type": "refresh_token"
    }, timeout=30)
    
    if token_res.status_code != 200:
        send_telegram(f"❌ FAIL Auth: HTTP {token_res.status_code}")
        return
        
    access_token = token_res.json().get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Final Message banane ke liye list
    report = ["📊 **GDrive Test Report**\n"]

    for folder_name, folder_id in FOLDERS.items():
        if not folder_id:
            report.append(f"⚠️ {folder_name}: Missing ID")
            continue
            
        test_file = f"/tmp/test_{folder_name.lower()}.txt"
        with open(test_file, "w") as f:
            f.write(f"Test file for {folder_name} at {time.ctime()}")
            
        # Upload file
        metadata = {"name": os.path.basename(test_file), "parents": [folder_id]}
        with open(test_file, "rb") as f:
            res = requests.post(
                "https://www.googleapis.com/upload/drive/v3/files",
                headers=headers, 
                params={"uploadType": "multipart"}, 
                data={"metadata": (None, json.dumps(metadata), "application/json"), "file": f},
                timeout=60
            )
        
        # Check Result
        if res.status_code in (200, 201):
            report.append(f"✅ {folder_name}: OK")
        else:
            report.append(f"❌ {folder_name}: Error ({res.status_code})")
            
        os.remove(test_file)

    final_msg = "\n".join(report)
    send_telegram(final_msg)
    print(final_msg)

if __name__ == "__main__":
    test_all_gdrive()
