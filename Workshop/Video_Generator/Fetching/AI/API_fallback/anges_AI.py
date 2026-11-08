#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/AI/API_fallback/anges_AI.py
# 🎯 PURPOSE: Anges AI API का उपयोग करके टेक्स्ट जनरेट करना
# ✅ SELF-CONTAINED: अगर API फेल होगी, तो None रिटर्न करेगा ताकि अगला AI ट्राई हो सके।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

def generate(prompt, max_tokens=500):
    """
    Anges AI API से टेक्स्ट जनरेट करेगा।
    """
    api_key = os.getenv("ANGES_API_KEY")
    if not api_key:
        print("[anges] ⚠️ ANGES_API_KEY missing")
        return None

    print(f"[anges] 🧠 Generating text for prompt (Length: {len(prompt)})...")
    
    # Anges AI का API URL (तुम्हारे पुराने कोड के हिसाब से)
    url = "https://apihub.agnes-ai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "agnes-2.5-flash", # पुराने कोड में यही मॉडल था
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if r.status_code == 200:
            data = r.json()
            # OpenAI फॉर्मेट से टेक्स्ट निकालना
            generated_text = data["choices"][0]["message"]["content"].strip()
            print("[anges] ✅ Success")
            return generated_text
        else:
            print(f"[anges] ❌ Failed: HTTP {r.status_code} — {r.text[:200]}")
            return None
            
    except Exception as e:
        print(f"[anges] ❌ Error: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🧪 Anges AI Test")
    print("═" * 50)
    res = generate("Say exactly: Anges is working!")
    if res:
        print("\n--- Result ---")
        print(res)
    print("═" * 50)
