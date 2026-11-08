import os, requests

def generate(prompt, max_tokens=500):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    print(f"[gemini] 🧠 Generating...")
    # 🟢 अपडेटेड मॉडल: gemini-2.0-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens}
    }

    try:
        r = requests.post(url, json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            print(f"[gemini] ❌ Failed: HTTP {r.status_code}")
            return None
    except Exception as e:
        return None
