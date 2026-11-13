import os, requests, random

def generate(prompt, max_tokens=500):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    # 🟢 हर बार कहानी का टोन (मूड) बदलने के लिए (ताकि स्क्रिप्ट रिपीट न हो)
    styles = [
        "emotional and heart-touching", 
        "motivational and energetic", 
        "calm and peaceful", 
        "storytelling and engaging", 
        "deep and philosophical", 
        "simple and easy to understand"
    ]
    random_style = random.choice(styles)

    # 🟢 AI को सख्त हिदायत कि वो बिल्कुल नए अंदाज में लिखे
    enhanced_prompt = f"Write the following in a {random_style} tone. Make sure the wording is completely unique, fresh, and engaging. Do not use repetitive sentences.\n\n{prompt}"

    print(f"[gemini] 🧠 Generating with style: {random_style}...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": enhanced_prompt}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.9, # 🟢 हाई क्रिएटिविटी (0.0 = रिपीट, 1.0 = बहुत ज्यादा नया)
            "topP": 0.95,
            "topK": 40
        }
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
