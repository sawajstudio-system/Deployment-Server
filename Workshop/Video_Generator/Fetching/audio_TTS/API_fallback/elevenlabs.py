# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/audio_TTS/API_fallback/elevenlabs.py
# 🎯 PURPOSE: ElevenLabs API का उपयोग करके टेक्स्ट को आवाज़ में बदलना (TTS)
# ══════════════════════════════════════════════════════════════════════════════

import os
import requests

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
API_KEY_ENV = "ELEVENLABS_API_KEY"
# 'Adam' की आवाज़ (Deep male voice), जो इस्लामिक स्टोरीज़ के लिए बहुत अच्छी लगती है
VOICE_ID = "pNInz6obpgDQGcFmaJgB" 
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

# ══════════════════════════════════════════════════════════════════════════════
# CORE FUNCTION
# ══════════════════════════════════════════════════════════════════════════════
def generate(text, output_path="temp/voice.mp3"):
    """
    Text को Voice में बदलकर output_path पर सेव करेगा।
    """
    api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        print(f"[elevenlabs] ⚠️ {API_KEY_ENV} missing in secrets.")
        return None

    print(f"[elevenlabs] 🎙️ Generating premium voice for {len(text)} characters...")
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    # वॉइस सेटिंग्स (स्टेबिलिटी और क्लैरिटी के लिए)
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2", # बहुभाषी मॉडल (हिंदी के लिए बेस्ट)
        "voice_settings": {
            "stability": 0.42,
            "similarity_boost": 0.82,
            "style": 0.35,
            "use_speaker_boost": True
        }
    }

    try:
        r = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        
        # अगर सफल रहा और ऑडियो डेटा मिला (कम से कम 1KB का होना चाहिए)
        if r.status_code == 200 and len(r.content) > 1000:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "wb") as f:
                f.write(r.content)
                
            print(f"[elevenlabs] ✅ Premium Voice saved to {output_path}")
            return output_path
        else:
            print(f"[elevenlabs] ❌ Failed: HTTP {r.status_code} — {r.text[:200]}")
            return None # यह None लौटाएगा ताकि main.py अगली फाइल (edge_tts) ट्राई कर सके
            
    except Exception as e:
        print(f"[elevenlabs] ❌ Error: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
# TEST (Standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🎙️ ElevenLabs TTS Test")
    print("═" * 50)
    
    test_text = "नमस्ते, यह सवाज स्टूडियो की तरफ से एक टेस्ट है।"
    result = generate(test_text, "temp/test_voice.mp3")
    
    if result:
        print(f"Success! Audio file created at: {result}")
    else:
        print("Test failed. (Check API Key or Internet)")
    print("═" * 50)
