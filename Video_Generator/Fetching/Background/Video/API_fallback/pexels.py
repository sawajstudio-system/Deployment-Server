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
                video_files = videos[0].get("video_files", [])
                if not video_files: return None
                
                # 🟢 FIX: 4K की जगह 1080p वीडियो चुनें ताकि रेंडर फास्ट हो
                best_file = video_files[0] 
                for vf in video_files:
                    if 720 <= vf.get("width", 0) <= 1080: 
                        best_file = vf
                        break
                
                print(f"[pexels] Downloading video width: {best_file.get('width')}p...")
                vid_data = requests.get(best_file["link"], timeout=30).content
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as f: f.write(vid_data)
                return output_path
        return None
    except Exception: return None
