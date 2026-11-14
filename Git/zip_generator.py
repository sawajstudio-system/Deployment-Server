#!/usr/bin/env python3
import os
import zipfile
import requests
import base64
import io

TOKEN = os.getenv("TELEGRAM_API_REPORT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")
GITHUB_TOKEN = os.getenv("TOKEN_GITHUB")
PUBLIC_REPO = "sawajstudio-system/Firent"
PRIVATE_REPO = "sawajstudio-system/Backend"

def fetch_repo_zip(repo_name, out_zip):
    print(f"📥 Fetching {repo_name}...")
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    # Get default branch
    r = requests.get(f"https://api.github.com/repos/{repo_name}", headers=headers)
    if r.status_code != 200:
        print(f"❌ Failed to get repo info: {r.status_code}")
        return False
    
    branch = r.json().get("default_branch", "main")
    
    # Download zipball
    zip_url = f"https://api.github.com/repos/{repo_name}/zipball/{branch}"
    print(f"📥 Downloading zipball for {repo_name}...")
    r_zip = requests.get(zip_url, headers=headers, allow_redirects=True)
    
    if r_zip.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(r_zip.content)) as z:
            z.extractall(out_zip)
        return True
    else:
        print(f"❌ Failed to download zipball: {r_zip.status_code}")
        return False

def main():
    out = "Output.zip"
    TARGET = os.getenv("REPO_TARGET", "Public + Private")
    TEMP_DIR = "/tmp/repo_files"

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        if TARGET in ("Public + Private", "Public Only"):
            if fetch_repo_zip(PUBLIC_REPO, TEMP_DIR + "/pub"):
                for root, dirs, files in os.walk(TEMP_DIR + "/pub"):
                    for f in files:
                        p = os.path.join(root, f)
                        z.write(p, os.path.join("Public_Repo", os.path.relpath(p, TEMP_DIR + "/pub")))
        
        if TARGET in ("Public + Private", "Private Only"):
            if fetch_repo_zip(PRIVATE_REPO, TEMP_DIR + "/priv"):
                for root, dirs, files in os.walk(TEMP_DIR + "/priv"):
                    for f in files:
                        p = os.path.join(root, f)
                        z.write(p, os.path.join("Private_Repo", os.path.relpath(p, TEMP_DIR + "/priv")))

    if TOKEN and CHAT_ID and os.path.exists(out):
        with open(out, "rb") as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument",
                          data={"chat_id": CHAT_ID, "caption": f"📦 ZIP Ready ({TARGET})"},
                          files={"document": f}, timeout=120)

    if os.path.exists(out): os.remove(out)
    print(f"✅ ZIP Generated and Sent!")

if __name__ == "__main__":
    main()
