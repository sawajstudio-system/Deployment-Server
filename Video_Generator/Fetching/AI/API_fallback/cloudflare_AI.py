import os, requests, random

def generate(prompt, max_tokens=500):
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.getenv("CLOUDFLARE_API_TOKEN")

    if not account_id or not api_token: return None

    styles = ["emotional and heart-touching", "motivational and energetic", "calm and peaceful", "storytelling and engaging", "deep and philosophical"]
    random_style = random.choice(styles)
    enhanced_prompt = f"Write in a {random_style} tone. Make it unique.\n\n{prompt}"

    print(f"[cloudflare] 🧠 Generating with style: {random_style}...")
    
    model = "@cf/meta/llama-3.3-70b-instruct-fp8-fast" # 🟢 लेटेस्ट मॉडल
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
    
    headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
    
    payload = {
        "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": enhanced_prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.9
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            if data.get("success"):
                return data.get("result", {}).get("response", "").strip()
            else:
                print(f"[cloudflare] ❌ API Error: {data.get('errors')}")
                return None
        else:
            print(f"[cloudflare] ❌ Failed: HTTP {r.status_code}")
            return None
    except Exception as e:
        return None
