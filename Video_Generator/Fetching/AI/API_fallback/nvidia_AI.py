import os, requests, random

def generate(prompt, max_tokens=500):
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key: return None

    styles = ["emotional and heart-touching", "motivational and energetic", "calm and peaceful", "storytelling and engaging", "deep and philosophical"]
    random_style = random.choice(styles)
    enhanced_prompt = f"Write in a {random_style} tone. Make it unique.\n\n{prompt}"

    print(f"[nvidia] 🧠 Generating with style: {random_style}...")
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    payload = {
        "model": "nvidia/nemotron-3-ultra-550b-a55b", # 🟢 पावरफुल मॉडल
        "messages": [{"role": "user", "content": enhanced_prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.9,
        "top_p": 1.0
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            msg_obj = r.json()["choices"][0]["message"]
            # NVIDIA में कभी-कभी content की जगह reasoning_content आता है
            return (msg_obj.get("content") or msg_obj.get("reasoning_content") or "").strip()
        else:
            print(f"[nvidia] ❌ Failed: HTTP {r.status_code}")
            return None
    except Exception as e:
        return None
