#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/AI/API_fallback/nvidia_AI.py
# 🎯 PURPOSE: NVIDIA API का उपयोग करके टेक्स्ट जनरेट करना
# ✅ SELF-CONTAINED: अगर API फेल होगी, तो None रिटर्न करेगा ताकि अगला AI ट्राई हो सके।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

def generate(prompt, max_tokens=500):
    """
    NVIDIA API से टेक्स्ट जनरेट करेगा।
    """
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        print("[nvidia] ⚠️ NVIDIA_API_KEY missing")
        return None

    print(f"[nvidia] 🧠 Generating text for prompt (Length: {len(prompt)})...")
    
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta/llama3-70b-instruct", # NVIDIA का फास्ट और पावरफुल मॉडल
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "top_p": 1.0
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if r.status_code == 200:
            data = r.json()
            # OpenAI फॉर्मेट से टेक्स्ट निकालना
            generated_text = data["choices"][0]["message"]["content"].strip()
            print("[nvidia] ✅ Success")
            return generated_text
        else:
            print(f"[nvidia] ❌ Failed: HTTP {r.status_code} — {r.text[:200]}")
            return None
            
    except Exception as e:
        print(f"[nvidia] ❌ Error: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🧪 NVIDIA AI Test")
    print("═" * 50)
    res = generate("Write a short beautiful line about nature in Hindi.")
    if res:
        print("\n--- Result ---")
        print(res)
    print("═" * 50)
