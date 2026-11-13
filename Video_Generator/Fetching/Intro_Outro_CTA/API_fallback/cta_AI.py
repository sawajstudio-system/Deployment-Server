# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Intro_Outro_CTA/API_fallback/cta_AI.py
# 🎯 PURPOSE: AI का उपयोग करके वीडियो के लिए एक छोटा सा CTA (Call to Action) बनाना
# ══════════════════════════════════════════════════════════════════════════════

import os
import sys

def generate_cta():
    """
    AI का उपयोग करके एक छोटा सा CTA टेक्स्ट बनाएगा।
    """
    print("[cta_AI] ✨ Generating Call To Action Text...")
    
    # AI फोल्डर का रास्ता सेट करो (ताकि ai_fallback इम्पोर्ट हो सके)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ai_path = os.path.join(base_dir, "AI", "API_fallback")
    
    if ai_path not in sys.path:
        sys.path.insert(0, ai_path)
        
    try:
        # हमारे मास्टर AI फॉलबैक सिस्टम को इम्पोर्ट करना
        from ai_fallback import generate_text
        
        # AI को प्रॉम्प्ट (आदेश) देना
        prompt = "Write a very short 3 to 5 word Call to Action for a short Islamic video (like 'Follow for more', 'Share this video', or 'Like and Subscribe'). Only output the phrase, no quotes."
        text = generate_text(prompt, max_tokens=20)
        
        if text:
            # साफ-सफाई (अगर AI ने quotes लगा दिए हों)
            text = text.replace('"', '').replace("'", "").strip()
            print(f"[cta_AI] ✅ AI CTA Generated: {text}")
            return text
            
    except Exception as e:
        print(f"[cta_AI] ❌ AI Error: {e}")

    # अगर सारे AI फेल हो जाएं, तो यह डिफ़ॉल्ट टेक्स्ट इस्तेमाल होगा
    default_text = "Follow for Daily Hadith"
    print(f"[cta_AI] 🔄 Using Default CTA: {default_text}")
    return default_text

# ══════════════════════════════════════════════════════════════════════════════
# TEST (Standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("✨ CTA AI Test")
    print("═" * 50)
    
    cta_text = generate_cta()
    
    print("\n--- Final Result ---")
    print(f"CTA Text: {cta_text}")
    print("═" * 50)
