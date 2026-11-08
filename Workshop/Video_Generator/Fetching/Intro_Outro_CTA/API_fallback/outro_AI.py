# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Intro_Outro_CTA/API_fallback/outro_AI.py
# 🎯 PURPOSE: AI का उपयोग करके वीडियो के लिए एक प्यारा सा Outro (धन्यवाद) बनाना
# ══════════════════════════════════════════════════════════════════════════════

import os
import sys

def generate_outro():
    """
    AI का उपयोग करके एक छोटा सा आउट्रो (Thank You) टेक्स्ट बनाएगा।
    """
    print("[outro_AI] ✨ Generating Outro Text...")
    
    # AI फोल्डर का रास्ता सेट करो (ताकि ai_fallback इम्पोर्ट हो सके)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ai_path = os.path.join(base_dir, "AI", "API_fallback")
    
    if ai_path not in sys.path:
        sys.path.insert(0, ai_path)
        
    try:
        # हमारे मास्टर AI फॉलबैक सिस्टम को इम्पोर्ट करना
        from ai_fallback import generate_text
        
        # AI को प्रॉम्प्ट (आदेश) देना
        prompt = "Write a very short, polite 2 to 4 word outro phrase in English or Hindi for an Islamic video (like 'JazakAllah Khair' or 'Thanks for watching'). Only output the phrase, no quotes."
        text = generate_text(prompt, max_tokens=20)
        
        if text:
            # साफ-सफाई (अगर AI ने quotes लगा दिए हों)
            text = text.replace('"', '').replace("'", "").strip()
            print(f"[outro_AI] ✅ AI Outro Generated: {text}")
            return text
            
    except Exception as e:
        print(f"[outro_AI] ❌ AI Error: {e}")

    # अगर सारे AI फेल हो जाएं, तो यह डिफ़ॉल्ट इस्लामिक टेक्स्ट इस्तेमाल होगा
    default_text = "JazakAllah Khair"
    print(f"[outro_AI] 🔄 Using Default Outro: {default_text}")
    return default_text

# ══════════════════════════════════════════════════════════════════════════════
# TEST (Standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("✨ Outro AI Test")
    print("═" * 50)
    
    outro_text = generate_outro()
    
    print("\n--- Final Result ---")
    print(f"Outro Text: {outro_text}")
    print("═" * 50)
