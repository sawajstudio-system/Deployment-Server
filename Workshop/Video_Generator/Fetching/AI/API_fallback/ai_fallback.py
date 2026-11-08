#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/AI/API_fallback/ai_fallback.py
# 🎯 PURPOSE: सभी AI को एक-एक करके ट्राई करना (Smart Fallback System)
# ✅ SELF-CONTAINED: अगर एक AI फेल होता है, तो अपने आप दूसरे पर स्विच हो जाएगा।
# ══════════════════════════════════════════════════════════════════════════════

import sys
import os

# पाथ सेट करो ताकि यह इसी फोल्डर की बाकी AI फाइलों को इम्पोर्ट कर सके
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# सारी AI फाइलों को इम्पोर्ट करो
try:
    import gemini_AI
    import openrouter_AI
    import groq_AI
    import cohere_AI
    import nvidia_AI
    import cloudflare_AI
    import anges_AI
    # Magic और Tanvo को हम फिलहाल टेक्स्ट जनरेशन चेन में नहीं रख रहे क्योंकि वो इमेज जनरेटर हैं
except ImportError as e:
    print(f"[ai_fallback] ⚠️ Warning: Missing AI module - {e}")


def generate_text(prompt, max_tokens=500):
    """
    यह फंक्शन एक-एक करके सारे AI को ट्राई करेगा।
    जो सबसे पहले सक्सेस होगा, उसका रिजल्ट रिटर्न कर देगा।
    """
    print(f"\n[ai_fallback] 🧠 Starting AI Generation Chain...")
    print(f"[ai_fallback] Prompt length: {len(prompt)} chars")

    # 1. Gemini
    try:
        print("[ai_fallback] 🔄 Trying Gemini...")
        res = gemini_AI.generate(prompt, max_tokens)
        if res:
            print("[ai_fallback] ✅ Gemini Succeeded!")
            return res
    except Exception as e:
        print(f"[ai_fallback] ❌ Gemini failed: {e}")

    # 2. OpenRouter
    try:
        print("[ai_fallback] 🔄 Trying OpenRouter...")
        res = openrouter_AI.generate(prompt, max_tokens)
        if res:
            print("[ai_fallback] ✅ OpenRouter Succeeded!")
            return res
    except Exception as e:
        print(f"[ai_fallback] ❌ OpenRouter failed: {e}")

    # 3. Groq
    try:
        print("[ai_fallback] 🔄 Trying Groq...")
        res = groq_AI.generate(prompt, max_tokens)
        if res:
            print("[ai_fallback] ✅ Groq Succeeded!")
            return res
    except Exception as e:
        print(f"[ai_fallback] ❌ Groq failed: {e}")

    # 4. Cohere
    try:
        print("[ai_fallback] 🔄 Trying Cohere...")
        res = cohere_AI.generate(prompt, max_tokens)
        if res:
            print("[ai_fallback] ✅ Cohere Succeeded!")
            return res
    except Exception as e:
        print(f"[ai_fallback] ❌ Cohere failed: {e}")

    # 5. NVIDIA
    try:
        print("[ai_fallback] 🔄 Trying NVIDIA...")
        res = nvidia_AI.generate(prompt, max_tokens)
        if res:
            print("[ai_fallback] ✅ NVIDIA Succeeded!")
            return res
    except Exception as e:
        print(f"[ai_fallback] ❌ NVIDIA failed: {e}")

    # 6. Cloudflare
    try:
        print("[ai_fallback] 🔄 Trying Cloudflare...")
        res = cloudflare_AI.generate(prompt, max_tokens)
        if res:
            print("[ai_fallback] ✅ Cloudflare Succeeded!")
            return res
    except Exception as e:
        print(f"[ai_fallback] ❌ Cloudflare failed: {e}")

    # 7. Anges AI
    try:
        print("[ai_fallback] 🔄 Trying Anges AI...")
        res = anges_AI.generate(prompt, max_tokens)
        if res:
            print("[ai_fallback] ✅ Anges AI Succeeded!")
            return res
    except Exception as e:
        print(f"[ai_fallback] ❌ Anges AI failed: {e}")

    # अगर सब फेल हो जाएँ
    print("[ai_fallback] 🚨 WARNING: All AI models failed to generate text.")
    return "Allah is the best of planners." # आखिरी बैकअप (ताकि सिस्टम क्रैश न हो)


# ══════════════════════════════════════════════════════════════════════════════
# TEST (Standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🧠 AI Fallback System Test")
    print("═" * 50)
    
    test_prompt = "Write a one-line quote about peace."
    result = generate_text(test_prompt)
    
    if result:
        print("\n--- Final Result ---")
        print(result)
    else:
        print("\n❌ Generation completely failed.")
    print("═" * 50)
