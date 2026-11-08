import os

BASE_DIR = "Video_Generator/Story_Generator/Story_Render"

# --- यहाँ हमने हर फाइल का कोड सेट किया है ---
FILES = {
    # CONFIG - FONTS
    "config/fonts/arabic_fonts.py": """ARABIC_FONTS = ["Amiri", "Reem Kufi", "Scheherazade"]""",
    "config/fonts/hindi_fonts.py": """HINDI_FONTS = ["Yatra One", "Rozha One", "Eczar"]""",
    "config/fonts/english_fonts.py": """ENGLISH_FONTS = ["Playfair Display", "Cinzel", "Montserrat", "Lora"]""",

    # CONFIG - SIZES
    "config/sizes/font_sizes.py": """ARABIC_SIZE = 85\nHINDI_SIZE = 75\nENGLISH_SIZE = 60""",
    "config/sizes/screen_size.py": """PLAY_RES_X = 1080\nPLAY_RES_Y = 1920""",
    "config/sizes/margins.py": """ARABIC_MARGIN_V = 700\nHINDI_MARGIN_V = 550\nENGLISH_MARGIN_V = 400""",

    # CONFIG - COLORS
    "config/colors/hex_colors.py": """WHITE = "&H00FFFFFF&"\nGOLD = "&H0000D7FF&"\nBLACK = "&H00000000&"""" ,
    "config/colors/base_color.py": """from .hex_colors import WHITE\nBASE_COLOR = WHITE""",
    "config/colors/highlight_color.py": """from .hex_colors import GOLD\nHIGHLIGHT_COLOR = GOLD""",

    # SUBTITLE - ASSEMBLER
    "subtitle/assembler/ass_header.py": """def get_header():\n    return "[Script Info]\\nScriptType: v4.00+\\nPlayResX: 1080\\nPlayResY: 1920\\nWrapStyle: 2\\n" """,
    "subtitle/assembler/ass_style.py": """def get_style():\n    return "[V4+ Styles]\\nFormat: Name, Fontname...\\n" """,
    "subtitle/assembler/ass_saver.py": """import os\ndef save_ass(content, path):\n    os.makedirs(os.path.dirname(path), exist_ok=True)\n    with open(path, 'w', encoding='utf-8') as f:\n        f.write(content)""",

    # SUBTITLE - BUILDERS
    "subtitle/builders/main_sub_builder.py": """def build_main_sub():\n    return "Main Subtitle Content" """,
    "subtitle/builders/cta_sub_builder.py": """def build_cta_sub():\n    return "CTA Subtitle Content" """,
    "subtitle/builders/intro_sub_builder.py": """def build_intro_sub():\n    return "Intro Subtitle Content" """,
    "subtitle/builders/outro_sub_builder.py": """def build_outro_sub():\n    return "Outro Subtitle Content" """,

    # SUBTITLE - TIMING
    "subtitle/timing/word_weight.py": """def get_weights(words):\n    return [1.0 for _ in words]""",
    "subtitle/timing/time_format.py": """def format_time(seconds):\n    return f"0:00:{int(seconds):02d}.00" """,

    # SUBTITLE - LANGUAGES
    "subtitle/languages/hindi_vendor.py": """def process_hindi(text):\n    return text""",
    "subtitle/languages/english_vendor.py": """def process_english(text):\n    return text""",
    "subtitle/languages/arabic_vendor.py": """def process_arabic(text):\n    return f'\\\\u202B{text}\\\\u202C'""",

    # TOOLS
    "tools/duration_checker.py": """import subprocess\ndef get_duration(path):\n    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{path}"'\n    return float(subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip())""",
    "tools/cta_img_drawer.py": """from PIL import Image\ndef draw_cta(path):\n    img = Image.new('RGB', (1080, 1920), (10, 10, 15))\n    img.save(path)""",
    "tools/cta_text_placer.py": """def place_text(img_path, text):\n    pass""",

    # VIDEO ENGINE
    "video_engine/ffmpeg_builder.py": """def build_cmd(inputs, output):\n    return f"ffmpeg -y {inputs} {output}" """,
    "video_engine/ffmpeg_runner.py": """import subprocess\ndef run_cmd(cmd):\n    return subprocess.run(cmd, shell=True, capture_output=True, text=True)""",
    "video_engine/logo_processor.py": """def process_logo(path, w=420, h=150):\n    return path""",
    "video_engine/logo_placer.py": """def place_logo(cmd, x, y):\n    return cmd""",
    "video_engine/audio_mixer.py": """def mix_audio(voice, music):\n    return voice""",
    "video_engine/video_filter.py": """def get_filters():\n    return "scale=1080:1920" """,

    # MAIN RENDER FILES
    "render_main.py": """from subtitle.builders.main_sub_builder import build_main_sub\nfrom subtitle.assembler.ass_saver import save_ass\ndef build_and_render_story(**kwargs):\n    print("Rendering Story...")\n    return True""",
}

def create_files():
    print("🏗️ Starting Project Generation...")
    for rel_path, content in FILES.items():
        file_path = os.path.join(BASE_DIR, rel_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Created: {file_path}")

    # Create empty __init__.py files for Python packages
    init_dirs = [
        "config", "config/fonts", "config/sizes", "config/colors",
        "subtitle", "subtitle/assembler", "subtitle/builders", "subtitle/timing", "subtitle/languages",
        "tools", "video_engine"
    ]
    for d in init_dirs:
        init_path = os.path.join(BASE_DIR, d, "__init__.py")
        with open(init_path, "w") as f:
            f.write("")
        print(f"✅ Created: {init_path}")

if __name__ == "__main__":
    create_files()
    print("🎉 All files generated successfully!")
