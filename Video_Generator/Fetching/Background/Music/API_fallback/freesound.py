#!/usr/bin/env python3
import os
import random
import subprocess
import requests

def fetch(query="soft ambient meditation islamic peaceful", duration=60, output_path="temp/music.mp3"):
    api_key = os.getenv("FREESOUND_API_KEY")
    if not api_key:
        print("[freesound] ⚠️ FREESOUND_API_KEY missing.")
        return _generate_fallback(duration, output_path)

    print(f"[freesound] 🔍 Searching music for: '{query}'...")
    url = "https://freesound.org/apiv2/search/text/"
    params = {
        "query": query,
        "token": api_key,
        "fields": "id,name,previews",
        "filter": f"duration:[10 TO {max(30, int(duration))}]",
        "page_size": 10
    }

    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            results = r.json().get("results", [])
            if results:
                track = results[0]
                previews = track.get("previews", {})
                audio_url = previews.get("preview-hq-mp3") or previews.get("preview-lq-mp3")
                
                if audio_url:
                    print(f"[freesound] 📥 Downloading track...")
                    audio_data = requests.get(audio_url, timeout=30).content
                    
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    raw_music = "temp/raw_music.mp3"
                    with open(raw_music, "wb") as f:
                        f.write(audio_data)

                    fade_out_start = max(duration - 3.0, 1.0)
                    cmd = (
                        f'ffmpeg -y -stream_loop -1 -i {raw_music} -af '
                        f'"volume=0.20,afade=t=in:st=0:d=2,afade=t=out:st={fade_out_start:.2f}:d=3" '
                        f'-t {duration:.2f} -c:a libmp3lame -b:a 192k {output_path}'
                    )
                    subprocess.run(cmd, shell=True, check=True, capture_output=True)
                    
                    if os.path.exists(raw_music): os.remove(raw_music)
                    print(f"[freesound] ✅ Music saved to {output_path}")
                    return output_path
    except Exception as e:
        print(f"[freesound] ❌ Error: {e}")

    # अगर ऊपर का सब फेल हो जाए
    return _generate_fallback(duration, output_path)

def _generate_fallback(duration, output_path):
    print("[freesound] 🔄 Generating Fallback Sine Wave Music...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cmd = (
        f'ffmpeg -y -f lavfi -i "sine=frequency=110:duration={duration:.2f}" -af '
        f'"afade=t=in:st=0:d=2,afade=t=out:st={max(duration-3.0, 1.0):.2f}:d=3,volume=0.12" '
        f'-c:a libmp3lame -b:a 192k {output_path}'
    )
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        print(f"[freesound] ✅ Fallback music saved.")
        return output_path
    except Exception as e:
        print(f"[freesound] ❌ Fallback failed: {e}")
        return None
