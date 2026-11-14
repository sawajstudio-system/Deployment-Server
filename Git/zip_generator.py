import os
import io
import shutil
import zipfile
import requests

TOKEN = os.getenv("TELEGRAM_API_REPORT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")
GITHUB_TOKEN = os.getenv("TOKEN_GITHUB")

PUBLIC_REPO = "sawajstudio-system/hosting_sarvar"
PRIVATE_REPO = "sawajstudio-system/Deployment-Server"
TEMP_DIR = "/tmp/repo_files"

def fetch_repo_zip(repo_name, out_zip):
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(f"https://api.github.com/repos/{repo_name}", headers=headers, timeout=30)
    if r.status_code != 200: return False
    branch = r.json().get("default_branch", "main")
    r_zip = requests.get(f"https://api.github.com/repos/{repo_name}/zipball/{branch}", headers=headers, allow_redirects=True, timeout=120)
    if r_zip.status_code == 200:
        os.makedirs(out_zip, exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(r_zip.content)) as z: z.extractall(out_zip)
        return True
    return False

def main():
    out = "Output.zip"
    TARGET = os.getenv("REPO_TARGET", "Public + Private")
    if os.path.exists(TEMP_DIR): shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR + "/pub", exist_ok=True)
    os.makedirs(TEMP_DIR + "/priv", exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        if TARGET in ("Public + Private", "Public Only", "Hosting Only"):
            if fetch_repo_zip(PUBLIC_REPO, TEMP_DIR + "/pub"):
                for root, dirs, files in os.walk(TEMP_DIR + "/pub"):
                    for f in files:
                        p = os.path.join(root, f)
                        z.write(p, os.path.join("Public_Repo", os.path.relpath(p, TEMP_DIR + "/pub")))
        if TARGET in ("Public + Private", "Private Only", "Deployment-Server Only"):
            if fetch_repo_zip(PRIVATE_REPO, TEMP_DIR + "/priv"):
                for root, dirs, files in os.walk(TEMP_DIR + "/priv"):
                    for f in files:
                        p = os.path.join(root, f)
                        z.write(p, os.path.join("Private_Repo", os.path.relpath(p, TEMP_DIR + "/priv")))
    if TOKEN and CHAT_ID and os.path.exists(out):
        with open(out, "rb") as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument", data={"chat_id": CHAT_ID, "caption": f"📦 ZIP Ready ({TARGET})"}, files={"document": f}, timeout=120)
    if os.path.exists(out): os.remove(out)
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    print("✅ ZIP Generated and Sent!")

if __name__ == "__main__": main()
