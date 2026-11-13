#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/AI/API_fallback/ai_fallback.py
# 🎯 PURPOSE: Master AI Fallback Chain (Gemini → OpenRouter → Groq → ...)
# ✅ UPGRADED: अब पूरी तरह फेल होने पर None return करता है (गलत string नहीं)
# ══════════════════════════════════════════════════════════════════════════════

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 🟢 हर module को अलग try में import करें (एक फेल हो तो बाकी चलें)
gemini_AI = None
openrouter_AI = None
groq_AI = None
cohere_AI = None
nvidia_AI = None
cloudflare_AI = None
anges_AI = None

try:
    import gemini_AI
except ImportError as e:
    print(f"[ai_fallback] ⚠️ gemini_AI missing: {e}")

try:
    import openrouter_AI
except ImportError as e:
    print(f"[ai_fallback] ⚠️ openrouter_AI missing: {e}")

try:
    import groq_AI
except ImportError as e:
    print(f"[ai_fallback] ⚠️ groq_AI missing: {e}")

try:
    import cohere_AI
except ImportError as e:
    print(f"[ai_fallback] ⚠️ cohere_AI missing: {e}")

try:
    import nvidia_AI
except ImportError as e:
    print(f"[ai_fallback] ⚠️ nvidia_AI missing: {e}")

try:
    import cloudflare_AI
except ImportError as e:
    print(f"[ai_fallback] ⚠️ cloudflare_AI missing: {e}")

try:
    import anges_AI
except ImportError as e:
    print(f"[ai_fallback] ⚠️ anges_AI missing: {e}")


# 🟢 ट्रैकर वेरिएबल्स
LAST_USED_AI = "None"
FAILED_AIS = []


def generate_text(prompt, max_tokens=500):
    """
    AI Fallback Chain.
    ✅ Success → text (str)
    ❌ पूरी तरह fail → None (main.py इसे fallback के रूप में use करेगा)
    """
    global LAST_USED_AI, FAILED_AIS
    LAST_USED_AI = "None"
    FAILED_AIS = []

    print(f"\n[ai_fallback] 🧠 Starting AI Generation Chain...")

    # ── 1. Gemini ─────────────────────────────────────────────────────────────
    if gemini_AI:
        try:
            res = gemini_AI.generate(prompt, max_tokens)
            if res and res.strip():
                LAST_USED_AI = "Gemini"
                print("[ai_fallback] ✅ Gemini Succeeded!")
                return res.strip()
        except Exception as e:
            print(f"[ai_fallback] ❌ Gemini error: {e}")
        FAILED_AIS.append("Gemini")

    # ── 2. OpenRouter ────────────────────────────────────────────────────────
    if openrouter_AI:
        try:
            res = openrouter_AI.generate(prompt, max_tokens)
            if res and res.strip():
                LAST_USED_AI = "OpenRouter"
                print("[ai_fallback] ✅ OpenRouter Succeeded!")
                return res.strip()
        except Exception as e:
            print(f"[ai_fallback] ❌ OpenRouter error: {e}")
        FAILED_AIS.append("OpenRouter")

    # ── 3. Groq ──────────────────────────────────────────────────────────────
    if groq_AI:
        try:
            res = groq_AI.generate(prompt, max_tokens)
            if res and res.strip():
                LAST_USED_AI = "Groq"
                print("[ai_fallback] ✅ Groq Succeeded!")
                return res.strip()
        except Exception as e:
            print(f"[ai_fallback] ❌ Groq error: {e}")
        FAILED_AIS.append("Groq")

    # ── 4. Cohere ────────────────────────────────────────────────────────────
    if cohere_AI:
        try:
            res = cohere_AI.generate(prompt, max_tokens)
            if res and res.strip():
                LAST_USED_AI = "Cohere"
                print("[ai_fallback] ✅ Cohere Succeeded!")
                return res.strip()
        except Exception as e:
            print(f"[ai_fallback] ❌ Cohere error: {e}")
        FAILED_AIS.append("Cohere")

    # ── 5. NVIDIA ────────────────────────────────────────────────────────────
    if nvidia_AI:
        try:
            res = nvidia_AI.generate(prompt, max_tokens)
            if res and res.strip():
                LAST_USED_AI = "NVIDIA"
                print("[ai_fallback] ✅ NVIDIA Succeeded!")
                return res.strip()
        except Exception as e:
            print(f"[ai_fallback] ❌ NVIDIA error: {e}")
        FAILED_AIS.append("NVIDIA")

    # ── 6. Cloudflare ────────────────────────────────────────────────────────
    if cloudflare_AI:
        try:
            res = cloudflare_AI.generate(prompt, max_tokens)
            if res and res.strip():
                LAST_USED_AI = "Cloudflare"
                print("[ai_fallback] ✅ Cloudflare Succeeded!")
                return res.strip()
        except Exception as e:
            print(f"[ai_fallback] ❌ Cloudflare error: {e}")
        FAILED_AIS.append("Cloudflare")

    # ── 7. Anges AI ──────────────────────────────────────────────────────────
    if anges_AI:
        try:
            res = anges_AI.generate(prompt, max_tokens)
            if res and res.strip():
                LAST_USED_AI = "Anges AI"
                print("[ai_fallback] ✅ Anges AI Succeeded!")
                return res.strip()
        except Exception as e:
            print(f"[ai_fallback] ❌ Anges AI error: {e}")
        FAILED_AIS.append("Anges AI")

    # ── सब फेल ───────────────────────────────────────────────────────────────
    print("[ai_fallback] 🚨 WARNING: All AI models failed to generate text.")
    LAST_USED_AI = "None"
    return None   # ✅ None return करें, न कि अंग्रेजी string
