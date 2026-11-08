#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Background/Photo/URL_fallback/pollinations_AI.py
# 🎯 PURPOSE: Pollinations AI का उपयोग करके AI Image जनरेट करना
# ✅ SELF-CONTAINED: यह बिना किसी API Key के सीधे URL से इमेज लाता है।
# ══════════════════════════════════════════════════════════════════════════════

import os
import urllib.parse
import requests

def fetch(prompt="islamic mosque beautiful sunset 4k", output_path="temp/bg_photo.jpg"):
    """
    Pollinations AI से एक इमेज जनरेट करके डाउनलोड करेगा।
    """
    print(f"[pollinations] 🎨 Generating AI Image for: '{prompt}'...")
    
    # URL के लिए प्रॉम्प्ट को एनकोड करो
    encoded_prompt = urllib.parse.quote(prompt)
    
    # 1080x1920 (Portrait) साइज़ में इमेज जनरेट करने का URL
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true"
    
    try:
        # इमेज को जनरेट होने में थोड़ा समय लग सकता है, इसलिए timeout 60s रखा है
        r = requests.get(url, timeout=60)
        
        if r.status_code == 200 and len(r.content) > 5000: # कम से कम 5KB की इमेज होनी चाहिए
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(r.content)
                
            print(f"[pollinations] ✅ AI Photo saved to {output_path}")
            return output_path
        else:
            print(f"[pollinations] ❌ Failed: HTTP {r.status_code}")
            return None
            
    except Exception as e:
        print(f"[pollinations] ❌ Error: {e}")
        return None
