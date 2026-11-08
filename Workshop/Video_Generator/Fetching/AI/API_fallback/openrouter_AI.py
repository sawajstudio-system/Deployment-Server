#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/AI/API_fallback/openrouter_AI.py
# 🎯 PURPOSE: OpenRouter API का उपयोग करके टेक्स्ट जनरेट करना
# ✅ SELF-CONTAINED: अगर API फेल होगी, तो None रिटर्न करेगा ताकि अगला AI ट्राई हो सके।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

def generate(prompt, max_tokens=500):
    """
    OpenRouter API से टेक्स्ट जनरेट करेगा।
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("[openrouter] ⚠️ OPENROUTER_API_KEY missing")
        return None

    print(f"[openrouter] 🧠 Generating text for prompt (Length: {len(prompt)})...")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # OpenRouter में ये हेडर्स देना अच्छा होता है (लेकिन ज़रूरी नहीं)
        "HTTP-Referer": "https://github.com/sawajstudio-system",
        "X-Title": "Sawaj Studio Video Generator"
    }
    
    payload = {
        "model": "openai/gpt-4o-mini", # एक बहुत ही फास्ट और सस्ता मॉडल
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if r.status_code == 200:
            data = r.json()
            # OpenAI फॉर्मेट से टेक्स्ट निकालना
            generated_text = data["choices"][0]["message"]["content"].strip()
            print("[openrouter] ✅ Success")
            return generated_text
        else:
            print(f"[openrouter] ❌ Failed: HTTP {r.status_code} — {r.text[:200]}")
            return None
            
    except Exception as e:
        print(f"[openrouter] ❌ Error: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🧪 OpenRouter AI Test")
    print("═" * 50)
    res = generate("Write a short motivational quote in Hindi.")
    if res:
        print("\n--- Result ---")
        print(res)
    print("═" * 50)
