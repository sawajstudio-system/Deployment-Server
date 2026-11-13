# ══════════════════════════════════════════════════════════════════════════════
# 📁 FOLDER: Story_Generator/
# 📄 FILE  : main.py
# 🎯 PURPOSE: यह पूरे वीडियो का मैनेजर है। यह डेटा लाता है और रेंडरिंग शुरू करता है।
# ══════════════════════════════════════════════════════════════════════════════

#!/usr/bin/env python3
import os, sys, requests, subprocess, random, shutil, traceback
from concurrent.futures import ThreadPoolExecutor

# पाथ सेट करना ताकि फोल्डर्स मिल सकें
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# सारे जरूरी मॉड्यूल्स इम्पोर्ट करना
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
from Fetching.AI.API_fallback import ai_fallback


def send_telegram(message):
    token = os.getenv("TELEGRAM_API_REPORT_TOKEN")
    chat_id = os.getenv("TELEGRAM_API_REPORT_CHAT_ID")
    if not token or not chat_id:
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": message[:4000], "parse_mode": "HTML"}, timeout=10)
    except Exception:
        pass

def download_and_normalize(args):
    i, query, clip_duration, clip_path = args
    temp_raw = f"temp/raw_clip_{i}.mp4"
    api_used = "Failed"

    try:
        if pexels.fetch(query=query, duration=clip_duration, output_path=temp_raw):
            api_used = "Pexels"
        elif pixabay.fetch(query=query, duration=clip_duration, output_path=temp_raw):
            api_used = "Pixabay"
        elif coverr.fetch(query=query, duration=clip_duration, output_path=temp_raw):
            api_used = "Coverr"
        elif gradient.fetch(duration=clip_duration, output_path=temp_raw):
            api_used = "Gradient"
    except Exception:
        pass

    if not os.path.exists(temp_raw):
        return (False, "Failed")

    norm_cmd = (
        f'ffmpeg -y -i "{temp_raw}" '
        f'-vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=24,setsar=1" '
        f'-an -c:v libx264 -preset ultrafast -crf 30 -threads 0 "{clip_path}"'
    )
    try:
        subprocess.run(norm_cmd, shell=True, capture_output=True, timeout=180)
    except Exception:
        pass

    if os.path.exists(temp_raw):
        os.remove(temp_raw)

    ok = os.path.exists(clip_path) and os.path.getsize(clip_path) > 10000
    return (ok, api_used)

def run_pipeline():
    print("═" * 60)
    print("🎬 STARTING PREMIUM STORY PIPELINE")
    send_telegram("🚀 <b>Video Generation Started!</b>")
    os.makedirs("temp", exist_ok=True)

    # 1. हदीस लाना
    hadith = fawaz.fetch()
    if not hadith:
        send_telegram("❌ Hadith fetch failed.")
        return
    english_text = hadith.get("english", "")
    send_telegram("1. 📖 हदीस मिल गई...")

    # 2. AI से स्क्रिप्ट बनवाना
    send_telegram("2. 🧠 AI स्क्रिप्ट बना रहा है...")
    prompt = f"Translate to Hindi and add a short moral lesson. Total 70-80 words. Only Hindi text.\n\nHadith: {english_text}"
    hindi_text = ai_fallback.generate_text(prompt, max_tokens=250)

    if hindi_text:
        ai_used = ai_fallback.LAST_USED_AI
    else:
        hindi_text = mymemory.translate(english_text)
        ai_used = "MyMemory (AI failed)"

    # Devanagari script check
    if not hindi_text or not any('\u0900' <= ch <= '\u097F' for ch in hindi_text):
        send_telegram(f"❌ Hindi failed: {(hindi_text or '')[:60]!r}")
        return

    ai_failed = ", ".join(ai_fallback.FAILED_AIS) if ai_fallback.FAILED_AIS else "None"

    # 3. इंट्रो, आउट्रो, CTA
    send_telegram("3. ✨ Intro/Outro/CTA जनरेट हो रहे हैं...")
    base_intro = intro_AI.generate_intro()
    book_name = hadith.get("collection", "Hadith")
    hadith_num = hadith.get("number", "")
    intro_text = f"{base_intro}\\N{book_name} - Hadith #{hadith_num}"

    outro_text = outro_AI.generate_outro()
    cta_text = cta_AI.generate_cta()

    # 4. आवाज़ बनाना (TTS)
    send_telegram("4. 🎙️ आवाज़ बन रही है...")
    voice_path = "temp/voice.mp3"
    tts_text = f"हदीस शरीफ। {hindi_text}"

    voice_used = None
    if elevenlabs.generate(tts_text, voice_path):
        voice_used = "ElevenLabs"
    elif edge_tts.generate(tts_text, voice_path):
        voice_used = "Edge-TTS"

    if not voice_used or not os.path.exists(voice_path):
        send_telegram("❌ Voice generation failed completely.")
        return

    # 5. बैकग्राउंड वीडियो डाउनलोड करना
    send_telegram("5. 🎥 सिनेमैटिक वीडियो डाउनलोड हो रहे हैं...")
    final_bg_video = "temp/bg_video.mp4"
    concat_list = "temp/concat_list.txt"

    # 🟢 यहाँ हम duration नहीं निकाल रहे हैं, यह काम Story_Render (main_render.py) करेगा
    # इससे बैकग्राउंड काला होने की समस्या खत्म हो जाएगी

    all_queries = [
        "islamic mosque architecture", "holy quran book pages", "islamic calligraphy nature",
        "stars night sky", "ocean waves sunset", "desert sand dunes", "green mountains waterfall",
        "candle light warm", "rain on window", "clouds moving sky", "forest trees sunlight",
        "peaceful garden flowers", "old mosque minaret", "kaaba mecca", "madina green dome",
        "birds flying sky", "river flowing rocks", "snow falling winter", "lightning storm clouds",
        "lantern light dark", "prayer beads tasbih", "dates fruit bowl", "arabic tea coffee",
        "sunrise golden hour", "moon crescent night", "beautiful sunset landscape", "foggy morning forest"
    ]
    random.shuffle(all_queries)
    queries = all_queries[:3]

    # यहाँ क्लिप की लंबाई के लिए हम एक अनुमानित समय (जैसे 20 सेकंड) ले सकते हैं, 
    # या बेहतर होगा कि हम पहले वॉइस की लंबाई नाप लें। लेकिन अभी के लिए हम इसे 20 मान लेते हैं।
    # असली रेंडरिंग के समय duration अपने आप फिट हो जाएगा।
    clip_duration = 20.0  # डमी, ताकि 3 वीडियो डाउनलोड हो सकें

    download_tasks = [(i, q, clip_duration, f"temp/clip_{i}.mp4") for i, q in enumerate(queries)]

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(download_and_normalize, download_tasks))

    valid_clips = []
    video_apis_used = set()
    with open(concat_list, "w") as f:
        for i, (res, api) in enumerate(results):
            clip_path = f"temp/clip_{i}.mp4"
            if res and os.path.exists(clip_path):
                valid_clips.append(clip_path)
                video_apis_used.add(api)
                f.write(f"file '{os.path.abspath(clip_path)}'\n")

    video_api_str = ", ".join(video_apis_used) if video_apis_used else "None"

    if valid_clips:
        merge_cmd = f'ffmpeg -y -f concat -safe 0 -i "{concat_list}" -c copy "{final_bg_video}"'
        try: subprocess.run(merge_cmd, shell=True, capture_output=True, timeout=60)
        except Exception: pass

    if not os.path.exists(final_bg_video) or os.path.getsize(final_bg_video) < 10000:
        if valid_clips: 
            final_bg_video = valid_clips[0]
        else:
            send_telegram("❌ सभी बैकग्राउंड वीडियो सोर्स फेल हो गए!")
            return

    # 6. म्यूजिक और नेचर साउंड
    send_telegram("6. 🎵 म्यूजिक और प्राकृतिक आवाज़ें मिक्स हो रही हैं...")
    music_path = "temp/music.mp3"
    nature_path = "temp/nature.mp3"
    final_audio_path = "temp/final_bg_audio.mp3"

    if freesound.fetch(query="soft ambient meditation islamic peaceful", duration=60, output_path=music_path):
        music_used = "Freesound"
    elif pixabay_music.fetch(duration=60, output_path=music_path):
        music_used = "Pixabay"
    else:
        music_used = "None (silent)"
        music_path = "" 

    success_nature = freesound.fetch(query="rain soft ambience", duration=60, output_path=nature_path)

    if music_path and success_nature:
        mix_cmd = (
            f'ffmpeg -y -i "{music_path}" -i "{nature_path}" '
            f'-filter_complex "[0:a]volume=0.15[m];[1:a]volume=0.10[n];[m][n]amix=inputs=2:duration=first[out]" '
            f'-map "[out]" "{final_audio_path}"'
        )
        try:
            subprocess.run(mix_cmd, shell=True, capture_output=True, timeout=120)
            if os.path.exists(final_audio_path) and os.path.getsize(final_audio_path) > 1000:
                final_audio_path = final_audio_path
            else:
                final_audio_path = music_path
        except Exception:
            final_audio_path = music_path
    elif music_path:
        final_audio_path = music_path
    else:
        final_audio_path = ""

    # 7. फाइनल रेंडरिंग
    send_telegram("7. 🎬 Final Video Render हो रही है...")
    final_video_path = "temp/Final_Story.mp4"

    # 🟢 यहाँ हम Story_Render को कॉल कर रहे हैं। 
    # यह खुद duration निकालेगा और बैकग्राउंड को पूरा दिखाएगा।
    try:
        import io
        import contextlib
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            render_success = build_and_render_story(
                bg_video=final_bg_video, 
                music_path=final_audio_path, 
                voice_path=voice_path,
                hadith=hadith, 
                hindi_text=hindi_text, 
                intro_text=intro_text,
                outro_text=outro_text, 
                cta_text=cta_text, 
                output_path=final_video_path
            )
            
        ffmpeg_log = f.getvalue()
        if "❌ === FFMPEG ERROR START ===" in ffmpeg_log:
            error_msg = ffmpeg_log.split("❌ === FFMPEG ERROR START ===")[1].split("❌ === FFMPEG ERROR END ===")[0]
            send_telegram(f"❌ <b>FFmpeg Error:</b>\n<pre>{error_msg[:1000]}</pre>")
            return
    except Exception as e:
        render_success = None
        send_telegram(f"❌ Python Error in Render: {e}")
        return

    if not render_success or not os.path.exists(final_video_path):
        send_telegram("❌ Video Rendering Failed (Unknown Error).")
        return

    # 8. Google Drive पर अपलोड
    send_telegram("8. ☁️ Google Drive पर Upload हो रही है...")
    drive_link = upload_to_drive(final_video_path)

    # 9. फाइनल रिपोर्ट
    report = f"🎉 <b>Video Ready!</b>\n\n"
    report += f"📜 <b>Hadith:</b> {book_name} #{hadith_num}\n"
    report += f"🧠 <b>AI Script:</b> {ai_used} <i>(Failed: {ai_failed})</i>\n"
    report += f"🎙️ <b>Voice:</b> {voice_used}\n"
    report += f"🎥 <b>Video:</b> {video_api_str}\n"
    report += f"🎵 <b>Music:</b> {music_used}\n"

    if drive_link:
        report += f"\n📥 <a href='{drive_link}'>Click here to view</a>"
    else:
        report += f"\n❌ Google Drive Upload Failed."

    send_telegram(report)

    # 10. सफाई (Cleanup)
    try:
        shutil.rmtree("temp", ignore_errors=True)
    except Exception:
        pass

if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        send_telegram(f"💥 <b>Pipeline crashed!</b>\n<pre>{tb[-1500:]}</pre>")
        raise
