#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Backend/System_room/Git_room/github.py
# ══════════════════════════════════════════════════════════════════════════════
"""
GitHub API Test (Standalone) — Air Mode
"""
import os
import sys
import requests

# ── CONFIG ──────────────────────────────────────────────────────────────────
TOKEN_ENV    = "TOKEN_GITHUB"
API_URL      = "https://api.github.com/user"
TG_TOKEN_ENV = "TELEGRAM_API_REPORT_TOKEN"
TG_CHAT_ENV  = "TELEGRAM_API_REPORT_CHAT_ID"

# ── TELEGRAM (Self-contained, no helper file needed) ────────────────────────
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

# ── GITHUB TEST ─────────────────────────────────────────────────────────────
def test_github():
    key = os.getenv(TOKEN_ENV)
    if not key:
        msg = f"⚠️ WARN GitHub: {TOKEN_ENV} missing"
        send_telegram(msg)
        print(msg)
        return 2

    headers = {
        "Authorization": f"Bearer {key}",
        "Accept": "application/vnd.github+json"
    }

    print(f"[github] calling: {API_URL}")

    try:
        r = requests.get(API_URL, headers=headers, timeout=30)
        print(f"[github] HTTP {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            username = data.get("login", "unknown")
            user_id = data.get("id", "unknown")
            
            msg = f"✅ OK GitHub Passed\n👤 User: {username}\n🆔 ID: {user_id}"
            send_telegram(msg)
            print(msg)
            return 0
        else:
            msg = f"❌ FAIL GitHub: HTTP {r.status_code} — {r.text[:300]}"
            send_telegram(msg)
            print(msg)
            return 1
    except Exception as e:
        msg = f"❌ ERR GitHub: {type(e).__name__}: {e}"
        send_telegram(msg)
        print(msg)
        return 1

# ── MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("═" * 60)
    print("🐙 GitHub API Test — Air Mode (Standalone)")
    print("═" * 60)
    code = test_github()
    sys.exit(code)
