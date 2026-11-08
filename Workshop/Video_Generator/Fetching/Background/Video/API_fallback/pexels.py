import os, requests
def fetch(query="islamic mosque night", duration=60, output_path="temp/bg_video.mp4"):
    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key: return None
    headers = {"Authorization": api_key}
    url = f"https://api.pexels.com/videos/search?query={query}&orientation=portrait&per_page=5"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            videos = r.json().get("videos", [])
            if videos:
                video_files = sorted(videos[0].get("video_files", []), key=lambda x: x.get("width", 0), reverse=True)
                if not video_files: return None
                best_file = video_files[0]
                for vf in video_files:
                    if 1000 <= vf.get("width", 0) <= 1400: best_file = vf; break
                vid_data = requests.get(best_file["link"], timeout=30).content
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as f: f.write(vid_data)
                return output_path
        return None
    except Exception: return None
