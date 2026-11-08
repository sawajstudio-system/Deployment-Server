#!/usr/bin/env python3
import os, sys, requests, subprocess
from concurrent.futures import ThreadPoolExecutor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
from Fetching.Islamic.Hadis.URL_fallback import fawaz
from Fetching.Translator.URL_fallback import mymemory
from Fetching.Intro_Outro_CTA.API_fallback import intro_AI, outro_AI, cta_AI
from Fetching.audio_TTS.API_fallback import elevenlabs
from Fetching.audio_TTS.URL_fallback import edge_tts
from Fetching.Background.Video.API_fallback import pexels, pixabay, coverr
from Fetching.Background.Video.URL_fallback import gradient
from Fetching.Background.Music.API_fallback import freesound
from Fetching.Background.Music.URL_fallback import pixabay_music
from Uploader.Drive.story_upload import upload_to_drive
from Story_Render import build_and_render_story
from Story_Render.tools.audio_helper import get_audio_duration
from Fetching.AI.API_fallback import ai_fallback 

def send_telegram(message):
    token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")
    if not token or not chat_id: return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"}, timeout=10)
    except Exception: pass

def download_single_video(args):
    i, query, clip_duration, clip_path = args
    print(f"📥 Fetching Video {i+1} for: {query}")
    success = pexels.fetch(query=query, duration=clip_duration, output_path=clip_path)
    if not success: success = pixabay.fetch(query=query, duration=clip_duration, output_path=clip_path)
    if not success: success = coverr.fetch(query=query, duration=clip_duration, output_path=clip_path)
    if not success: success = gradient.fetch(duration=clip_duration, output_path=clip_path)
    return success

def run_pipeline():
    print("═" * 60)
    print("🎬 STARTING STORY VIDEO PIPELINE (FAST MODE)")
    send_telegram("🚀 <b>Story Video Pipeline Started!</b>")
    os.makedirs("temp", exist_ok=True)

    hadith = fawaz.fetch()
    if not hadith: return
    english_text = hadith.get("english", "")

    # 🟢 AI से 40-55 सेकंड की स्क्रिप्ट (100-130 words)
    prompt = f"Translate to Hindi and add a short moral lesson. Total 100-130 words. Only Hindi text.\n\nHadith: {english_text}"
    hindi_text = ai_fallback.generate_text(prompt, max_tokens=350)
    if not hindi_text: hindi_text = mymemory.translate(english_text)

    intro_text = intro_AI.generate_intro()
    outro_text = outro_AI.generate_outro()
    cta_text = cta_AI.generate_cta()

    send_telegram("4. Voice (आवाज़) बन रही है...")
    voice_path = "temp/voice.mp3"
    tts_text = f"हदीस शरीफ। {hindi_text}"
    success = elevenlabs.generate(tts_text, voice_path)
    if not success: success = edge_tts.generate(tts_text, voice_path)
    if not success: return
    duration = get_audio_duration(voice_path)
    
    send_telegram("5. 3 अलग-अलग Islamic Videos डाउनलोड हो रहे हैं...")
    final_bg_video = "temp/bg_video.mp4"
    concat_list = "temp/concat_list.txt"
    
    queries = ["islamic mosque architecture", "holy quran book pages", "islamic calligraphy nature"]
    clip_duration = (duration + 2) / 3 
    
    download_tasks = [(i, q, clip_duration, f"temp/bg_clip_{i}.mp4") for i, q in enumerate(queries)]
    clip_paths = []
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(download_single_video, download_tasks))
        
    with open(concat_list, "w") as f:
        for i, res in enumerate(results):
            if res:
                clip_path = f"temp/bg_clip_{i}.mp4"
                clip_paths.append(clip_path)
                f.write(f"file '{os.path.abspath(clip_path)}'\n")

    if clip_paths:
        print("🔗 Merging videos (Ultrafast)...")
        # 🟢 सुपरफास्ट मर्जिंग
        merge_cmd = f'ffmpeg -y -f concat -safe 0 -i "{concat_list}" -c:v libx264 -preset ultrafast -crf 30 -threads 0 "{final_bg_video}"'
        subprocess.run(merge_cmd, shell=True, capture_output=True)
    else:
        final_bg_video = None

    send_telegram("6. Background Music लाया जा रहा है...")
    music_path = "temp/music.mp3"
    success_music = freesound.fetch(duration=duration, output_path=music_path)
    if not success_music: pixabay_music.fetch(duration=duration, output_path=music_path)

    send_telegram("7. Final Video Render हो रही है...")
    final_video_path = "temp/Final_Story.mp4"
    
    render_success = build_and_render_story(
        bg_video=final_bg_video, music_path=music_path, voice_path=voice_path,
        hadith=hadith, hindi_text=hindi_text, intro_text=intro_text,
        outro_text=outro_text, cta_text=cta_text, output_path=final_video_path
    )
    if not render_success: return

    send_telegram("8. Google Drive पर Upload हो रही है...")
    drive_link = upload_to_drive(final_video_path)
    if drive_link:
        send_telegram(f"🎉 <b>Video Ready!</b>\n📥 <a href='{drive_link}'>Click here to view</a>")

    try:
        for file in os.listdir("temp"):
            file_path = os.path.join("temp", file)
            if os.path.isfile(file_path): os.remove(file_path)
    except Exception: pass

if __name__ == "__main__":
    run_pipeline()
