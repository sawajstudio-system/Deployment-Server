# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Intro_Outro_CTA/API_fallback/intro_AI.py
# 🎯 PURPOSE: AI का उपयोग करके वीडियो के लिए एक आकर्षक Intro टेक्स्ट बनाना
# ══════════════════════════════════════════════════════════════════════════════

import os
import sys

def generate_intro():
    """
    AI का उपयोग करके एक छोटा सा इंट्रो टेक्स्ट बनाएगा।
    """
    print("[intro_AI] ✨ Generating Intro Text...")
    
    # AI फोल्डर का रास्ता सेट करो (ताकि ai_fallback इम्पोर्ट हो सके)
    # यह 3 स्टेप पीछे जाकर Fetching फोल्डर ढूंढेगा
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ai_path = os.path.join(base_dir, "AI", "API_fallback")
    
    if ai_path not in sys.path:
        sys.path.insert(0, ai_path)
        
    try:
        # हमारे मास्टर AI फॉलबैक सिस्टम को इम्पोर्ट करना
        from ai_fallback import generate_text
        
        # AI को प्रॉम्प्ट (आदेश) देना
        prompt = "Write a very short, beautiful, and engaging 3 to 5 word intro phrase for a morning Islamic video. Only output the phrase, no quotes."
        text = generate_text(prompt, max_tokens=20)
        
        if text:
            # साफ-सफाई (अगर AI ने quotes लगा दिए हों)
            text = text.replace('"', '').replace("'", "").strip()
            print(f"[intro_AI] ✅ AI Intro Generated: {text}")
            return text
            
    except Exception as e:
        print(f"[intro_AI] ❌ AI Error: {e}")

    # अगर सारे AI फेल हो जाएं, तो यह डिफ़ॉल्ट टेक्स्ट इस्तेमाल होगा
    default_text = "SAWAJ STUDIO Presents"
    print(f"[intro_AI] 🔄 Using Default Intro: {default_text}")
    return default_text

# ══════════════════════════════════════════════════════════════════════════════
# TEST (Standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("✨ Intro AI Test")
    print("═" * 50)
    
    intro_text = generate_intro()
    
    print("\n--- Final Result ---")
    print(f"Intro Text: {intro_text}")
    print("═" * 50)
