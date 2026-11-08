#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/AI/API_fallback/cohere_AI.py
# 🎯 PURPOSE: Cohere API का उपयोग करके टेक्स्ट जनरेट करना
# ✅ SELF-CONTAINED: अगर API फेल होगी, तो None रिटर्न करेगा ताकि अगला AI ट्राई हो सके।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

def generate(prompt, max_tokens=500):
    """
    Cohere API से टेक्स्ट जनरेट करेगा।
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        print("[cohere] ⚠️ COHERE_API_KEY missing")
        return None

    print(f"[cohere] 🧠 Generating text for prompt (Length: {len(prompt)})...")
    
    url = "https://api.cohere.com/v1/chat"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "command-r-plus-08-2024", # Cohere का पावरफुल मॉडल
        "message": prompt,
        "max_tokens": max_tokens
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if r.status_code == 200:
            data = r.json()
            # Cohere v1 चैट API के रिस्पॉन्स से टेक्स्ट निकालना
            generated_text = data.get("text", "").strip()
            print("[cohere] ✅ Success")
            return generated_text
        else:
            print(f"[cohere] ❌ Failed: HTTP {r.status_code} — {r.text[:200]}")
            return None
            
    except Exception as e:
        print(f"[cohere] ❌ Error: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🧪 Cohere AI Test")
    print("═" * 50)
    res = generate("Write a short dua for peace in one line.")
    if res:
        print("\n--- Result ---")
        print(res)
    print("═" * 50)
