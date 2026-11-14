import os
import sys
import time
import base64
import logging
import requests
from datetime import datetime, timezone

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_API_REPORT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")
GITHUB_TOKEN     = os.getenv("TOKEN_GITHUB")

PUBLIC_REPO   = "sawajstudio-system/hosting_sarvar"
BACKEND_REPO  = "sawajstudio-system/Deployment-Server"
WORKSHOP_REPO = "sawajstudio-system/Development"

TARGET       = os.getenv("REPO_TARGET", "All 3 Repos").strip()
OUTPUT_FILE       = "Combined.txt"
TELEGRAM_MAX_BYTES = 49 * 1024 * 1024
DRY_RUN            = os.getenv("DRY_RUN", "0") == "1"

SKIP_SEGMENTS = {".git", ".github/workflows/.gitkeep", "node_modules", ".venv", "venv", "env", "__pycache__", ".pytest_cache", ".mypy_cache", ".tox", ".idea", ".vscode", "dist", "build", "target", "bin", "obj", "site-packages", ".next", ".nuxt", ".terraform", ".cache"}
BINARY_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp", ".svg", ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z", ".jar", ".war", ".exe", ".dll", ".so", ".dylib", ".bin", ".dat", ".mp3", ".mp4", ".wav", ".avi", ".mov", ".mkv", ".webm", ".flac", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".pyc", ".pyo", ".class", ".o", ".a", ".db", ".sqlite", ".sqlite3", ".lock"}

logging.basicConfig(level=logging.INFO, format="%(asctime)s │ %(levelname)-7s │ %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("txtgen")

def gh_headers():
    if not GITHUB_TOKEN: raise RuntimeError("TOKEN_GITHUB missing!")
    return {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json", "User-Agent": "txt-generator-full/3.0"}

def gh_get(url, params=None, retries=4, timeout=60):
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, headers=gh_headers(), params=params, timeout=timeout)
            if r.status_code in (403, 429):
                reset = r.headers.get("X-RateLimit-Reset")
                wait = max(0, int(reset) - int(time.time())) + 2 if reset else min(int(r.headers.get("Retry-After", "30")), 300)
                log.warning(f"⏳ Rate limited ({r.status_code}). Sleep {wait}s...")
                time.sleep(wait)
                continue
            return r
        except requests.exceptions.RequestException as e:
            if attempt == retries: return None
            time.sleep(2 ** attempt)
    return None

def should_skip(path): return any(seg in SKIP_SEGMENTS for seg in path.replace("\\", "/").split("/"))
def is_binary(path): return any(path.lower().endswith(ext) for ext in BINARY_EXTS)

def safe_decode(b64_content):
    try: raw = base64.b64decode(b64_content)
    except Exception: return None
    for enc in ("utf-8", "latin-1", "cp1252"):
        try: return raw.decode(enc)
        except UnicodeDecodeError: continue
    return None

def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024: return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"

def get_repo_info(repo):
    r = gh_get(f"https://api.github.com/repos/{repo}")
    return r.json() if r and r.status_code == 200 else None

def get_tree(repo, branch):
    r = gh_get(f"https://api.github.com/repos/{repo}/git/trees/{branch}", params={"recursive": "1"})
    return [item["path"] for item in r.json().get("tree", []) if item.get("type") == "blob"] if r and r.status_code == 200 else []

def fetch_file(repo, path, ref):
    r = gh_get(f"https://api.github.com/repos/{repo}/contents/{path}", params={"ref": ref})
    if not r or r.status_code != 200: return ("fail", None)
    data = r.json()
    if data.get("type") != "file" or data.get("encoding") != "base64": return ("fail", None)
    content = safe_decode(data.get("content", ""))
    if content is None: return ("binary", None)
    if not content.strip(): return ("empty", None)
    return ("text", content)

def write_repo_section(fo, label, repo):
    stats = {"text": 0, "binary": 0, "empty": 0, "fail": 0}
    info = get_repo_info(repo)
    if not info: return stats
    branch = info.get("default_branch", "main")
    pushed = (info.get("pushed_at") or "")[:19].replace("T", " ")
    desc   = info.get("description") or "—"
    fo.write(f"\n\n{'#'*70}\n# REPO: {label}\n# URL    : https://github.com/{repo}\n# Branch : {branch}\n# Pushed : {pushed}\n# Desc   : {desc}\n{'#'*70}\n\n")
    files = get_tree(repo, branch)
    selected = [f for f in files if not should_skip(f)]
    binary_paths = []
    for idx, path in enumerate(selected, 1):
        if is_binary(path):
            binary_paths.append(path)
            stats["binary"] += 1
            continue
        status, content = fetch_file(repo, path, branch)
        if status == "text":
            fo.write(f"\n\n{'='*60}\nFILE: {label}/{path}\n{'='*60}\n{content}")
            stats["text"] += 1
        elif status == "binary": binary_paths.append(path); stats["binary"] += 1
        elif status == "empty": stats["empty"] += 1
        else: stats["fail"] += 1
    if binary_paths:
        fo.write(f"\n\n{'─'*60}\n# BINARY FILES IN {label}\n{'─'*60}\n")
        for bp in binary_paths: fo.write(f"#   [BINARY] {bp}\n")
    return stats

def split_file_for_telegram(path, max_bytes=TELEGRAM_MAX_BYTES):
    parts = []
    if os.path.getsize(path) <= max_bytes: return [path]
    part_num, buf, buf_size = 1, [], 0
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line_b = len(line.encode("utf-8"))
            if buf_size + line_b > max_bytes and buf:
                part_path = f"/tmp/part_{part_num}.txt"
                with open(part_path, "w", encoding="utf-8") as pf: pf.writelines(buf)
                parts.append(part_path)
                part_num += 1
                buf, buf_size = [], 0
            buf.append(line)
            buf_size += line_b
    if buf:
        part_path = f"/tmp/part_{part_num}.txt"
        with open(part_path, "w", encoding="utf-8") as pf: pf.writelines(buf)
        parts.append(part_path)
    return parts

def send_to_telegram(file_path, caption):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID: return
    parts = split_file_for_telegram(file_path)
    for i, part in enumerate(parts, 1):
        cap = caption if len(parts) == 1 else f"{caption} [Part {i}/{len(parts)}]"
        try:
            with open(part, "rb") as f:
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument", data={"chat_id": TELEGRAM_CHAT_ID, "caption": cap[:1024]}, files={"document": (os.path.basename(part), f)}, timeout=300)
        except Exception: pass
        finally:
            if part != file_path and os.path.exists(part): os.remove(part)

def main():
    start = time.time()
    valid_targets = {"All 3 Repos", "Hosting Only", "Deployment-Server Only", "Development Only", "Hosting + Deployment-Server", "Hosting + Development", "Deployment-Server + Development"}
    if TARGET not in valid_targets or not GITHUB_TOKEN: sys.exit(1)
    stats = {"Hosting": {"text": 0, "binary": 0, "empty": 0, "fail": 0}, "Deployment-Server": {"text": 0, "binary": 0, "empty": 0, "fail": 0}, "Development": {"text": 0, "binary": 0, "empty": 0, "fail": 0}}
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fo:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        fo.write(f"╔{'═'*68}╗\n║  COMBINED CODE EXPORT (3 REPOS){' '*37}║\n╚{'═'*68}╝\nGenerated : {now}\nTarget    : {TARGET}\n{'═'*70}\n")
        if "Hosting" in TARGET or TARGET == "All 3 Repos": stats["Hosting"] = write_repo_section(fo, "Hosting", PUBLIC_REPO)
        if "Deployment-Server" in TARGET or TARGET == "All 3 Repos": stats["Deployment-Server"] = write_repo_section(fo, "Deployment-Server", BACKEND_REPO)
        if "Development" in TARGET or TARGET == "All 3 Repos": stats["Development"] = write_repo_section(fo, "Development", WORKSHOP_REPO)
        fo.write(f"\n\n{'#'*70}\n# EXPORT SUMMARY\n{'#'*70}\n")
        for label, s in stats.items(): fo.write(f"# {label:17s} → text: {s['text']:4d}  binary: {s['binary']:4d}  empty: {s['empty']:4d}  fail: {s['fail']:4d}\n")
        fo.write(f"# Total time: {time.time() - start:.1f}s\n{'#'*70}\n")
    if os.path.exists(OUTPUT_FILE):
        size = os.path.getsize(OUTPUT_FILE)
        if not DRY_RUN:
            caption = f"📄 FULL DUMP ({TARGET})\n📦 Size: {human_size(size)}\n📊 Hosting: {stats['Hosting']['text']} txt\n📊 Deployment: {stats['Deployment-Server']['text']} txt\n📊 Development: {stats['Development']['text']} txt"
            send_to_telegram(OUTPUT_FILE, caption)
        os.remove(OUTPUT_FILE)

if __name__ == "__main__": sys.exit(main())
