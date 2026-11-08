#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/AI/API_fallback/tanvo_AI.py
# 🎯 PURPOSE: Tanvo AI API का उपयोग करना (Image Generation)
# ✅ SELF-CONTAINED: अगर API फेल होगी, तो None रिटर्न करेगा।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

def generate(prompt, max_tokens=500):
    """
    Tanvo API से इमेज जनरेट करेगा।
    """
    api_key = os.getenv("TANVO_API_KEY")
    if not api_key:
        print("[tanvo] ⚠️ TANVO_API_KEY missing")
        return None

    print(f"[tanvo] 🎨 Generating image via Tanvo for prompt (Length: {len(prompt)})...")
    
    url = "https://tanvo.ai/api/v1/generations"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "studio-image-v1",
        "prompt": prompt[:500],
        "kind": "image",
        "options": {
            "aspect": "1:1",
            "resolution": "1K",
            "format": "PNG"
        }
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if r.status_code in (200, 201, 202):
            data = r.json()
            gen_id = data.get("generation", {}).get("id")
            print("[tanvo] ✅ Image Generation Started")
            # चूँकि इमेज बनने में समय लगता है, हम जनरेशन ID रिटर्न कर रहे हैं
            return f"Tanvo Generation ID: {gen_id}"
        else:
            print(f"[tanvo] ❌ Failed: HTTP {r.status_code} — {r.text[:200]}")
            return None
            
    except Exception as e:
        print(f"[tanvo] ❌ Error: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🧪 Tanvo AI Test")
    print("═" * 50)
    res = generate("A beautiful islamic art.")
    if res:
        print("\n--- Result ---")
        print(res)
    print("═" * 50)
