#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/AI/API_fallback/cloudflare_AI.py
# 🎯 PURPOSE: Cloudflare Workers AI का उपयोग करके टेक्स्ट जनरेट करना
# ✅ SELF-CONTAINED: अगर API फेल होगी, तो None रिटर्न करेगा ताकि अगला AI ट्राई हो सके।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

def generate(prompt, max_tokens=500):
    """
    Cloudflare Workers AI से टेक्स्ट जनरेट करेगा।
    """
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.getenv("CLOUDFLARE_API_TOKEN")

    if not account_id or not api_token:
        print("[cloudflare] ⚠️ CLOUDFLARE_ACCOUNT_ID या CLOUDFLARE_API_TOKEN missing")
        return None

    print(f"[cloudflare] 🧠 Generating text for prompt (Length: {len(prompt)})...")
    
    # Cloudflare Workers AI का मॉडल (Llama 3 8B)
    model = "@cf/meta/llama-3-8b-instruct"
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if r.status_code == 200:
            data = r.json()
            # Cloudflare के रिस्पॉन्स फॉर्मेट से टेक्स्ट निकालना
            if data.get("success"):
                generated_text = data.get("result", {}).get("response", "").strip()
                print("[cloudflare] ✅ Success")
                return generated_text
            else:
                print(f"[cloudflare] ❌ API Error: {data.get('errors')}")
                return None
        else:
            print(f"[cloudflare] ❌ Failed: HTTP {r.status_code} — {r.text[:200]}")
            return None
            
    except Exception as e:
        print(f"[cloudflare] ❌ Error: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🧪 Cloudflare AI Test")
    print("═" * 50)
    res = generate("Write a short motivational quote.")
    if res:
        print("\n--- Result ---")
        print(res)
    print("═" * 50)
