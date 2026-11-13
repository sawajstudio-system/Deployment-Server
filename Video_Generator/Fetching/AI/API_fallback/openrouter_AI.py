import os, requests, random

def generate(prompt, max_tokens=500):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key: return None

    styles = ["emotional and heart-touching", "motivational and energetic", "calm and peaceful", "storytelling and engaging", "deep and philosophical"]
    random_style = random.choice(styles)
    enhanced_prompt = f"Write in a {random_style} tone. Make it unique.\n\n{prompt}"

    print(f"[openrouter] 🧠 Generating with style: {random_style}...")
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/sawajstudio-system",
        "X-Title": "Sawaj Studio Video Generator"
    }
    
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": enhanced_prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.9
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
        else:
            print(f"[openrouter] ❌ Failed: HTTP {r.status_code}")
            return None
    except Exception as e:
        return None
