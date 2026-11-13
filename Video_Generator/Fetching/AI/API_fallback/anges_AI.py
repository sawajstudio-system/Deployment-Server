import os, requests, random

def generate(prompt, max_tokens=500):
    api_key = os.getenv("ANGES_API_KEY")
    if not api_key: return None

    styles = ["emotional and heart-touching", "motivational and energetic", "calm and peaceful", "storytelling and engaging", "deep and philosophical"]
    random_style = random.choice(styles)
    enhanced_prompt = f"Write in a {random_style} tone. Make it unique.\n\n{prompt}"

    print(f"[anges] 🧠 Generating with style: {random_style}...")
    url = "https://apihub.agnes-ai.com/v1/chat/completions"
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    payload = {
        "model": "agnes-2.5-flash",
        "messages": [{"role": "user", "content": enhanced_prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.9
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
        else:
            print(f"[anges] ❌ Failed: HTTP {r.status_code}")
            return None
    except Exception as e:
        return None
