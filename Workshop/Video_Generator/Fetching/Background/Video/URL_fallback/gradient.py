#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Fetching/Background/Video/URL_fallback/gradient.py
# 🎯 PURPOSE: अगर सारे API फेल हो जाएँ, तो FFmpeg से रंगीन बैकग्राउंड बनाना
# ✅ SELF-CONTAINED: इसे किसी इंटरनेट या API की ज़रूरत नहीं होती।
# ══════════════════════════════════════════════════════════════════════════════

import os
import subprocess
import random

def fetch(duration=60, output_path="temp/bg_video.mp4"):
    """
    FFmpeg का उपयोग करके एक स्मूथ Gradient वीडियो बनाता है।
    """
    print(f"[gradient] 🎨 Generating Gradient Background for {duration}s...")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # रैंडम डार्क कलर्स (ताकि हर बार नया बैकग्राउंड दिखे)
    c0 = f"{random.randint(10,40):02x}{random.randint(10,40):02x}{random.randint(30,60):02x}"
    c1 = f"{random.randint(10,40):02x}{random.randint(10,40):02x}{random.randint(30,60):02x}"
    
    try:
        cmd = (
            f'ffmpeg -y -f lavfi -i "gradients=s=1080x1920:c0=0x{c0}:c1=0x{c1}:speed=0.005" '
            f'-t {duration:.2f} -c:v libx264 -preset veryfast -crf 20 {output_path}'
        )
        
        # FFmpeg कमांड रन करो
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        
        print(f"[gradient] ✅ Gradient video saved to {output_path}")
        return output_path
        
    except subprocess.CalledProcessError as e:
        print(f"[gradient] ❌ FFmpeg Error: {e}")
        return None
    except Exception as e:
        print(f"[gradient] ❌ Error: {e}")
        return None
