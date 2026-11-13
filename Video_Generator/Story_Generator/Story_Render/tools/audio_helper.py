# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/tools/audio_helper.py
# 🎯 PURPOSE: ऑडियो (MP3) की लंबाई (Duration) सेकंड में निकालना
# ══════════════════════════════════════════════════════════════════════════════

import subprocess
import os

def get_audio_duration(audio_path):
    """
    यह फंक्शन किसी भी ऑडियो फाइल की लंबाई सेकंड में बताता है।
    उदाहरण के लिए: 25.4 (मतलब 25.4 सेकंड)
    """
    print(f"⏱️ [audio_helper] Checking duration for: {audio_path}")
    
    # अगर फाइल ही मौजूद नहीं है
    if not os.path.exists(audio_path):
        print(f"❌ [audio_helper] File not found: {audio_path}")
        return 15.0 # अगर फाइल न मिले तो डिफ़ॉल्ट 15 सेकंड मान लो

    try:
        # FFprobe का इस्तेमाल करके ऑडियो की लंबाई निकालना (यह FFmpeg के साथ ही आता है)
        cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{audio_path}"'
        
        # कमांड रन करो और आउटपुट लो
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # आउटपुट को नंबर (float) में बदलो
        duration = float(result.stdout.strip())
        
        print(f"✅ [audio_helper] Audio length is: {duration:.2f} seconds")
        return duration
        
    except Exception as e:
        print(f"⚠️ [audio_helper] Error: {e}. Using default 15.0 seconds.")
        return 15.0

# ══════════════════════════════════════════════════════════════════════════════
# TEST (Standalone)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("⏱️ Audio Helper Test")
    print("═" * 50)
    
    # (इसे टेस्ट करने के लिए आपके पास 'temp/voice.mp3' फाइल होनी चाहिए)
    test_audio = "temp/voice.mp3" 
    
    duration = get_audio_duration(test_audio)
    print(f"Final Duration: {duration} seconds")
    print("═" * 50)
