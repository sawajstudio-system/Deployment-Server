import os
import subprocess


def generate(text, output_path="temp/voice_edge.mp3"):
    print(f"[edge_tts] Generating voice for {len(text)} chars...")
    text = text[:900]
    tmp_txt = output_path + ".txt"

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(tmp_txt, "w", encoding="utf-8") as f:
            f.write(text)

        cmd = (
            f'edge-tts --file "{tmp_txt}" --write-media "{output_path}" '
            f'--voice hi-IN-MadhurNeural --rate=-20% --pitch=-2Hz --volume=+8%'
        )
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180)

        if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"[edge_tts] ✅ {output_path}")
            return output_path
        print(f"[edge_tts] ❌ rc={result.returncode}")
        return None
    except Exception as e:
        print(f"[edge_tts] ❌ {e}")
        return None
    finally:
        if os.path.exists(tmp_txt):
            os.remove(tmp_txt)
