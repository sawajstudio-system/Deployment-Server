#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/Git_room/history_cleaner.py
# ══════════════════════════════════════════════════════════════════════════════
import os
import sys
import requests

TOKEN = os.getenv("TOKEN_GITHUB")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_REPORT_TOKEN")
TELEGRAM_CHAT = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")
REPO = os.getenv("GITHUB_REPOSITORY") # e.g. sawajstudio-system/Firent
RUN_ID = os.getenv("GITHUB_RUN_ID")

def send_telegram(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT: return
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      json={"chat_id": TELEGRAM_CHAT, "text": text}, timeout=15)
    except Exception: pass

def delete_old_runs():
    if not TOKEN or not REPO:
        print("❌ Missing TOKEN_GITHUB or GITHUB_REPOSITORY")
        return 1

    print(f"🗑️ Fetching workflow runs for {REPO}...")
    headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}
    
    try:
        r = requests.get(f"https://api.github.com/repos/{REPO}/actions/runs?per_page=100", headers=headers, timeout=30)
        runs = r.json().get("workflow_runs", []) if r.status_code == 200 else []
    except Exception as e:
        print(f"❌ Error fetching runs: {e}")
        return 1

    deleted = 0
    for wf_run in runs:
        rid = str(wf_run.get("id"))
        if rid != str(RUN_ID):
            dr = requests.delete(f"https://api.github.com/repos/{REPO}/actions/runs/{rid}", headers=headers, timeout=30)
            if dr.status_code == 204: 
                deleted += 1
                print(f"  ✓ Deleted run: {rid}")

    print(f"✅ Cleaner Done! Deleted {deleted} old runs.")
    send_telegram(f"✅ Cleaner Done! Old runs deleted: {deleted}")
    return 0

if __name__ == "__main__":
    sys.exit(delete_old_runs())
