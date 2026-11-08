import os, requests

def generate(prompt, max_tokens=500):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None

    print(f"[groq] 🧠 Generating...")
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 🟢 अपडेटेड मॉडल: llama-3.1-70b-versatile
    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            return data["choices"][0]["message"]["content"].strip()
        else:
            print(f"[groq] ❌ Failed: HTTP {r.status_code}")
            return None
    except Exception as e:
        return None
