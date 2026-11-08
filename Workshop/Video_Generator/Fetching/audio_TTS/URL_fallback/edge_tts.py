# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/audio_TTS/URL_fallback/edge_tts.py
# 🎯 PURPOSE: Microsoft Edge-TTS का उपयोग करके फ्री टेक्स्ट-टू-स्पीच (TTS) बनाना
# ══════════════════════════════════════════════════════════════════════════════

import os
import subprocess

# ══════════════════════════════════════════════════════════════════════════════
# CORE FUNCTION
# ══════════════════════════════════════════════════════════════════════════════
def generate(text, output_path="temp/voice_edge.mp3"):
    """
    edge-tts का इस्तेमाल करके टेक्स्ट को आवाज़ में बदलेगा।
    """
    print(f"[edge_tts] 🎙️ Generating FREE voice for {len(text)} characters...")
    
    # edge-tts एक कमांड-लाइन टूल है, इसलिए हमें टेक्स्ट को एक टेम्परेरी फाइल में सेव करना होगा
    tmp_txt = output_path + ".txt"
    
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # टेक्स्ट को फाइल में लिखना
        with open(tmp_txt, "w", encoding="utf-8") as f:
            f.write(text)

        # आवाज़ सेटिंग्स (Madhur - Hindi Male Voice)
        # rate=-7% (थोड़ा धीमा, ताकि समझने में आसानी हो), pitch=-2Hz (थोड़ी गहरी आवाज़)
        cmd = (
            f'edge-tts --file "{tmp_txt}" --write-media "{output_path}" '
            f'--voice hi-IN-MadhurNeural --rate=-7% --pitch=-2Hz --volume=+8%'
        )
        
        # कमांड रन करना
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # अगर कमांड सफल रहा और फाइल बन गई (कम से कम 1KB की होनी चाहिए)
        if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"[edge_tts] ✅ Free Voice saved to {output_path}")
            return output_path
        else:
            print(f"[edge_tts] ❌ Failed. Error: {result.stderr[:200]}")
            return None

    except Exception as e:
        print(f"[edge_tts] ❌ Error: {e}")
        return None
        
    finally:
        # काम खत्म होने के बाद टेम्परेरी टेक्स्ट फाइल को डिलीट कर देना
        if os.path.exists(tmp_txt):
            os.remove(tmp_txt)

# ══════════════════════════════════════════════════════════════════════════════
# TEST (Standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("🎙️ Edge-TTS (Free Fallback) Test")
    print("═" * 50)
    
    test_text = "नमस्ते, यह माइक्रोसॉफ्ट एज का फ्री टेस्ट है।"
    result = generate(test_text, "temp/test_edge_voice.mp3")
    
    if result:
        print(f"Success! Audio file created at: {result}")
    else:
        print("Test failed.")
    print("═" * 50)
