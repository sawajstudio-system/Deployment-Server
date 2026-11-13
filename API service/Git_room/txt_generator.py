#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 SAVE THIS FILE AT:
#    Deployment-Server/System_room/Git_room/txt_generator.py
#
# 💪 FULL DUMP VERSION — TEENO REPOS KA SAB KUCH EK TXT MEIN
# ══════════════════════════════════════════════════════════════════════════════
import os
import sys
import time
import base64
import logging
import requests
from datetime import datetime, timezone

# ── CONFIG ──────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN   = os.getenv("TELEGRAM_API_REPORT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")
GITHUB_TOKEN     = os.getenv("TOKEN_GITHUB")

# 🟢 तीनों रेपो के नए नाम यहाँ तय किए गए हैं
PUBLIC_REPO   = "sawajstudio-system/hosting"
BACKEND_REPO  = "sawajstudio-system/Deployment-Server"
WORKSHOP_REPO = "sawajstudio-system/Development"

TARGET       = os.getenv("REPO_TARGET", "All 3 Repos").strip()

OUTPUT_FILE       = "Combined.txt"
TELEGRAM_MAX_BYTES = 49 * 1024 * 1024   # ~49 MB (safe margin under 50 MB)
DRY_RUN            = os.getenv("DRY_RUN", "0") == "1"

# ── SIRF YE JUNK SKIP HOGA ─────────────────
SKIP_SEGMENTS = {
    ".git", ".github/workflows/.gitkeep",
    "node_modules", ".venv", "venv", "env",
    "__pycache__", ".pytest_cache", ".mypy_cache",
    ".tox", ".idea", ".vscode",
    "dist", "build", "target", "bin", "obj",
    "site-packages", ".next", ".nuxt",
    ".terraform", ".cache",
}

# ── BINARY EXTENSIONS ───────────
BINARY_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp", ".svg",
    ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z", ".jar", ".war",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".dat",
    ".mp3", ".mp4", ".wav", ".avi", ".mov", ".mkv", ".webm", ".flac",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".pyc", ".pyo", ".class", ".o", ".a",
    ".db", ".sqlite", ".sqlite3",
    ".lock",
}

# ── LOGGING ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-7s │ %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("txtgen")


# ══════════════════════════════════════════════════════════════════════════════
# 🔧 UTILITIES
# ══════════════════════════════════════════════════════════════════════════════
def gh_headers():
    if not GITHUB_TOKEN:
        raise RuntimeError("TOKEN_GITHUB missing!")
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "txt-generator-full/3.0",
    }

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
            if attempt == retries:
                log.error(f"❌ Request failed after {retries} tries: {e}")
                return None
            backoff = 2 ** attempt
            log.warning(f"⚠️ Retry {attempt}/{retries} in {backoff}s: {e}")
            time.sleep(backoff)
    return None

def should_skip(path):
    parts = path.replace("\\", "/").split("/")
    return any(seg in SKIP_SEGMENTS for seg in parts)

def is_binary(path):
    lower = path.lower()
    return any(lower.endswith(ext) for ext in BINARY_EXTS)

def safe_decode(b64_content):
    try:
        raw = base64.b64decode(b64_content)
    except Exception:
        return None
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return None

def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


# ══════════════════════════════════════════════════════════════════════════════
# 📡 GITHUB API
# ══════════════════════════════════════════════════════════════════════════════
def get_repo_info(repo):
    r = gh_get(f"https://api.github.com/repos/{repo}")
    if not r or r.status_code != 200:
        log.error(f"❌ Repo info failed for {repo}: {r.status_code if r else 'no-response'}")
        return None
    return r.json()

def get_tree(repo, branch):
    log.info(f"🌳 Fetching tree for {repo}@{branch}...")
    url = f"https://api.github.com/repos/{repo}/git/trees/{branch}"
    r = gh_get(url, params={"recursive": "1"})
    if not r or r.status_code != 200:
        log.error(f"❌ Tree fetch failed for {repo}")
        return []
    data = r.json()
    tree = data.get("tree", [])
    return [item["path"] for item in tree if item.get("type") == "blob"]

def fetch_file(repo, path, ref):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    r = gh_get(url, params={"ref": ref})
    if not r or r.status_code != 200:
        return ("fail", None)
    data = r.json()
    if data.get("type") != "file" or data.get("encoding") != "base64":
        return ("fail", None)
    content = safe_decode(data.get("content", ""))
    if content is None:
        return ("binary", None)
    if not content.strip():
        return ("empty", None)
    return ("text", content)


# ══════════════════════════════════════════════════════════════════════════════
# 📝 WRITE ONE REPO
# ══════════════════════════════════════════════════════════════════════════════
def write_repo_section(fo, label, repo):
    stats = {"text": 0, "binary": 0, "empty": 0, "fail": 0}
    info = get_repo_info(repo)
    if not info:
        return stats

    branch = info.get("default_branch", "main")
    pushed = (info.get("pushed_at") or "")[:19].replace("T", " ")
    desc   = info.get("description") or "—"

    fo.write(f"\n\n{'#'*70}\n")
    fo.write(f"# REPO: {label}\n")
    fo.write(f"# URL    : https://github.com/{repo}\n")
    fo.write(f"# Branch : {branch}\n")
    fo.write(f"# Pushed : {pushed}\n")
    fo.write(f"# Desc   : {desc}\n")
    fo.write(f"{'#'*70}\n\n")

    files = get_tree(repo, branch)
    log.info(f"📋 {repo}: {len(files)} total blobs found")
    selected = [f for f in files if not should_skip(f)]
    log.info(f"🎯 {repo}: {len(selected)} after skip filters")

    binary_paths = []
    for idx, path in enumerate(selected, 1):
        if DRY_RUN:
            fo.write(f"\n\n{'='*60}\nFILE: {label}/{path}\n{'='*60}\n[DRY RUN]\n")
            stats["text"] += 1
            continue

        if is_binary(path):
            binary_paths.append(path)
            stats["binary"] += 1
            continue

        status, content = fetch_file(repo, path, branch)
        if status == "text":
            fo.write(f"\n\n{'='*60}\nFILE: {label}/{path}\n{'='*60}\n")
            fo.write(content)
            stats["text"] += 1
        elif status == "binary":
            binary_paths.append(path)
            stats["binary"] += 1
        elif status == "empty":
            stats["empty"] += 1
        else:
            stats["fail"] += 1

        if idx % 25 == 0 or idx == len(selected):
            log.info(f"  {idx}/{len(selected)} (text: {stats['text']}, binary: {stats['binary']}, fail: {stats['fail']})")

    if binary_paths:
        fo.write(f"\n\n{'─'*60}\n# BINARY FILES IN {label}\n{'─'*60}\n")
        for bp in binary_paths:
            fo.write(f"#   [BINARY] {bp}\n")

    return stats


# ══════════════════════════════════════════════════════════════════════════════
# 📤 TELEGRAM UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
def split_file_for_telegram(path, max_bytes=TELEGRAM_MAX_BYTES):
    parts = []
    if os.path.getsize(path) <= max_bytes:
        return [path]
    log.warning(f"⚠️ File > {human_size(max_bytes)}. Splitting...")
    part_num, buf, buf_size = 1, [], 0
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line_b = len(line.encode("utf-8"))
            if buf_size + line_b > max_bytes and buf:
                part_path = f"/tmp/part_{part_num}.txt"
                with open(part_path, "w", encoding="utf-8") as pf:
                    pf.writelines(buf)
                parts.append(part_path)
                part_num += 1
                buf, buf_size = [], 0
            buf.append(line)
            buf_size += line_b
    if buf:
        part_path = f"/tmp/part_{part_num}.txt"
        with open(part_path, "w", encoding="utf-8") as pf:
            pf.writelines(buf)
        parts.append(part_path)
    return parts

def send_to_telegram(file_path, caption):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        log.warning("⚠️ Telegram not configured.")
        return
    parts = split_file_for_telegram(file_path)
    total = len(parts)
    for i, part in enumerate(parts, 1):
        cap = caption if total == 1 else f"{caption} [Part {i}/{total}]"
        try:
            with open(part, "rb") as f:
                r = requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument",
                    data={"chat_id": TELEGRAM_CHAT_ID, "caption": cap[:1024]},
                    files={"document": (os.path.basename(part), f)},
                    timeout=300,
                )
            if r.status_code == 200:
                log.info(f"✅ Telegram part {i}/{total} sent")
            else:
                log.error(f"❌ Telegram part {i}/{total} failed: {r.status_code}")
        except Exception as e:
            log.error(f"❌ Telegram error: {e}")
        finally:
            if part != file_path and os.path.exists(part):
                os.remove(part)


# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    start = time.time()
    log.info("═" * 60)
    log.info(f"📄 TXT Generator — 3 REPOS  |  Target: {TARGET}")
    log.info("═" * 60)

    # 🟢 अपडेटेड टारगेट लिस्ट (YML file se aane wale naye naam)
    valid_targets = {
        "All 3 Repos", "Hosting Only", "Deployment-Server Only", "Development Only",
        "Hosting + Deployment-Server", "Hosting + Development", "Deployment-Server + Development"
    }
    
    if TARGET not in valid_targets:
        log.error(f"❌ Invalid REPO_TARGET: {TARGET!r}.")
        sys.exit(1)

    if not GITHUB_TOKEN:
        log.error("❌ TOKEN_GITHUB missing!")
        sys.exit(1)

    stats = {
        "Hosting":           {"text": 0, "binary": 0, "empty": 0, "fail": 0},
        "Deployment-Server": {"text": 0, "binary": 0, "empty": 0, "fail": 0},
        "Development":       {"text": 0, "binary": 0, "empty": 0, "fail": 0},
    }

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as fo:
            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            fo.write("╔" + "═" * 68 + "╗\n")
            fo.write(f"║  COMBINED CODE EXPORT (3 REPOS){' ' * 37}║\n")
            fo.write("╚" + "═" * 68 + "╝\n")
            fo.write(f"Generated : {now}\n")
            fo.write(f"Target    : {TARGET}\n")
            fo.write("═" * 70 + "\n")

            # 🟢 तीनों रेपो को चेक करके कोड फेच करने का लॉजिक
            if "Hosting" in TARGET or TARGET == "All 3 Repos":
                log.info("▶️  HOSTING repo...")
                stats["Hosting"] = write_repo_section(fo, "Hosting", PUBLIC_REPO)

            if "Deployment-Server" in TARGET or TARGET == "All 3 Repos":
                log.info("▶️  DEPLOYMENT-SERVER repo...")
                stats["Deployment-Server"] = write_repo_section(fo, "Deployment-Server", BACKEND_REPO)

            if "Development" in TARGET or TARGET == "All 3 Repos":
                log.info("▶️  DEVELOPMENT repo...")
                stats["Development"] = write_repo_section(fo, "Development", WORKSHOP_REPO)

            # ── Footer ──
            fo.write(f"\n\n{'#'*70}\n# EXPORT SUMMARY\n{'#'*70}\n")
            for label, s in stats.items():
                fo.write(
                    f"# {label:17s} → text: {s['text']:4d}  "
                    f"binary: {s['binary']:4d}  "
                    f"empty: {s['empty']:4d}  "
                    f"fail: {s['fail']:4d}\n"
                )
            fo.write(f"# Total time: {time.time() - start:.1f}s\n")
            fo.write(f"{'#'*70}\n")

    except Exception as e:
        log.error(f"❌ Write failed: {e}")
        sys.exit(1)

    if os.path.exists(OUTPUT_FILE):
        size = os.path.getsize(OUTPUT_FILE)
        log.info(f"✅ Combined.txt ready: {human_size(size)}")

        if not DRY_RUN:
            caption = (
                f"📄 FULL DUMP ({TARGET})\n"
                f"📦 Size: {human_size(size)}\n"
                f"📊 Hosting: {stats['Hosting']['text']} txt + {stats['Hosting']['binary']} bin\n"
                f"📊 Deployment-Server: {stats['Deployment-Server']['text']} txt + {stats['Deployment-Server']['binary']} bin\n"
                f"📊 Development: {stats['Development']['text']} txt + {stats['Development']['binary']} bin"
            )
            send_to_telegram(OUTPUT_FILE, caption)

        os.remove(OUTPUT_FILE)
        log.info("🧹 Temp file removed")

    log.info(f"🏁 Done in {time.time() - start:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
