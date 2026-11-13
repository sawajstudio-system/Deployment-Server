#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/AI/API_fallback/magic_AI.py
# 🎯 PURPOSE: MagicHour API का उपयोग करना (Image/Video Generation)
# ✅ SELF-CONTAINED: अगर API फेल होगी, तो None रिटर्न करेगा।
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

def generate(prompt, max_tokens=500):
    """
    MagicHour API का उपयोग करके प्रॉम्प्ट भेजेगा।
    (चूँकि यह मुख्य रूप से इमेज/वीडियो के लिए है, यह प्रोजेक्ट ID या URL रिटर्न करेगा)
    """
    api_key = os.getenv("MAGICHOUR_API_KEY")
    if not api_key:
        print("[magic] ⚠️ MAGICHOUR_API_KEY missing")
        return None

    print(f"[magic] 🪄 Generating via MagicHour for prompt (Length: {len(prompt)})...")
    
    url = "https://api.magichour.ai/v1/ai-image-generator"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": "API Test Generation",
        "image_count": 1,
        "model": "z-image-turbo",
        "aspect_ratio": "1:1",
        "resolution": "640px",
        "style": {
            "prompt": prompt[:500], # MagicHour की लिमिट के हिसाब से
            "tool": "ai-anime-generator"
        }
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if r.status_code in (200, 201, 202):
            data = r.json()
            project_id = data.get("id", "unknown")
            print("[magic] ✅ Success")
            # चूँकि यह टेक्स्ट नहीं देता, हम एक स्टेटस स्ट्रिंग रिटर्न कर रहे हैं
            return f"MagicHour Project Created: {project_id}"
        else:
            print(f"[magic] ❌ Failed: HTTP {r.status_code} — {r.text[:200]}")
            return None
            
    except Exception as e:
        print(f"[magic] ❌ Error: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🧪 MagicHour AI Test")
    print("═" * 50)
    res = generate("A beautiful sunset over a mosque.")
    if res:
        print("\n--- Result ---")
        print(res)
    print("═" * 50)
