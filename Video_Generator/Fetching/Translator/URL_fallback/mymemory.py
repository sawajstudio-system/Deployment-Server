# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Translator/URL_fallback/mymemory.py
# 🎯 PURPOSE: English से Hindi में ट्रांसलेट करना (MyMemory API + AI Fallback)
# ══════════════════════════════════════════════════════════════════════════════

import os
import sys
import requests

def translate(text, target_lang="hi"):
    """
    अंग्रेजी टेक्स्ट को हिंदी में बदलेगा।
    """
    if not text or len(text.strip()) < 2:
        return ""

    print(f"[mymemory] 🌐 Translating English to Hindi (Length: {len(text)})...")

    # ── 1. पहले MyMemory (Free API) ट्राई करो ────────────────────────────────
    try:
        url = "https://api.mymemory.translated.net/get"
        # MyMemory की लिमिट होती है, इसलिए हम टेक्स्ट के सिर्फ पहले 500 अक्षर भेजते हैं
        params = {"q": text[:500], "langpair": f"en|{target_lang}"}
        
        r = requests.get(url, params=params, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            translated = data.get("responseData", {}).get("translatedText", "")
            
            # कभी-कभी MyMemory गलत रिस्पॉन्स देता है (जैसे "MYMEMORY WARNING")
            # हमें यह सुनिश्चित करना है कि रिस्पॉन्स सही हो
            if translated and "MYMEMORY WARNING" not in translated.upper():
                print("[mymemory] ✅ Success with MyMemory API")
                return translated
        else:
            print(f"[mymemory] ❌ MyMemory HTTP {r.status_code}")
            
    except Exception as e:
        print(f"[mymemory] ❌ MyMemory Error: {e}")

    # ── 2. अगर MyMemory फेल हो जाए -> AI Fallback (हमारा मास्टर AI सिस्टम) ───
    print("[mymemory] 🔄 Switching to AI Fallback for translation...")
    try:
        # AI फोल्डर का रास्ता सेट करना (ताकि ai_fallback इम्पोर्ट हो सके)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        ai_path = os.path.join(base_dir, "AI", "API_fallback")
        
        if ai_path not in sys.path:
            sys.path.insert(0, ai_path)
            
        from ai_fallback import generate_text
        
        # AI को ट्रांसलेट करने का प्रॉम्प्ट देना
        prompt = f"Translate the following English text to Hindi. Only output the translation, do not write anything else:\n\n{text}"
        translated = generate_text(prompt, max_tokens=500)
        
        if translated:
            print("[mymemory] ✅ Success with AI Fallback")
            return translated.strip()
            
    except Exception as e:
        print(f"[mymemory] ❌ AI Fallback Error: {e}")

    # ── 3. आखिरी बैकअप (ताकि वीडियो कभी न रुके) ──────────────────────────────
    print("[mymemory] ⚠️ All translation failed. Returning original English text.")
    print("[mymemory] All failed. Returning empty.")
    return ""

# ══════════════════════════════════════════════════════════════════════════════
# TEST (Standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🌐 Translator Test (MyMemory + AI)")
    print("═" * 50)
    
    test_text = "The reward of deeds depends upon the intentions."
    result = translate(test_text)
    
    print("\n--- Final Result ---")
    print(f"Original: {test_text}")
    print(f"Hindi   : {result}")
    print("═" * 50)
