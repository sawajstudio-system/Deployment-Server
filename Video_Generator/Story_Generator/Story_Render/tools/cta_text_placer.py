# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/tools/cta_text_placer.py
# 🎯 PURPOSE: CTA इमेज पर हेडर, बटन और स्टूडियो का नाम लिखना
# ══════════════════════════════════════════════════════════════════════════════

import os
import random
from PIL import Image, ImageDraw, ImageFont


def place_cta_text(base_png, output_path="temp/cta_image.png"):
    img = Image.open(base_png).convert("RGBA")
    draw = ImageDraw.Draw(img)

    try:
        font_top = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", 60)
        font_btn = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", 75) # 🟢 फॉन्ट बड़ा किया
        font_bottom = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", 45)
    except IOError:
        font_top = font_btn = font_bottom = ImageFont.load_default()

    colors = ["#FFD700", "#00FFFF", "#FF007F", "#39FF14",
              "#FFBF00", "#9D00FF", "#00FF7F", "#FF4500"]
    random.shuffle(colors)

    # 1. हेडर टेक्स्ट
    header_texts = [
        "Like • Share • Follow",
        "Support the Channel",
        "Join Our Community",
        "Spread the Knowledge"
    ]
    draw.text(
        (540, 1250),
        random.choice(header_texts),
        font=font_top,
        fill=colors[0],
        anchor="mm",
        stroke_width=4,
        stroke_fill="black"
    )

    # 2. बटन्स (मोटे और बड़े)
    btn_texts = [
        ["LIKE", "SUBSCRIBE", "COMMENT", "SHARE"],
        ["FOLLOW", "SHARE", "LIKE", "SUBSCRIBE"],
        ["SUBSCRIBE", "LIKE", "FOLLOW", "COMMENT"]
    ]
    texts = random.choice(btn_texts)

    # 🟢 Y-axis बढ़ा दिया ताकि बटन्स मोटे और बड़े दिखें (हाइट 90px)
    ys = [1340, 1445, 1550, 1655] 
    
    for i, (text, y) in enumerate(zip(texts, ys)):
        # बटन का बॉक्स (चौड़ाई 480px, हाइट 90px, border मोटा 6px)
        draw.rounded_rectangle(
            [300, y, 780, y + 90], 
            radius=15,
            outline=colors[i + 1],
            width=6
        )
        # बटन का टेक्स्ट
        draw.text(
            (540, y + 45), 
            text,
            font=font_btn,
            fill=colors[i + 1],
            anchor="mm",
            stroke_width=4,
            stroke_fill="black"
        )

    # 3. स्टूडियो का नाम
    draw.text(
        (540, 1820),
        "Sawajstudio",
        font=font_bottom,
        fill=colors[5],
        anchor="mm",
        stroke_width=3,
        stroke_fill="black"
    )

    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    img.save(output_path, "PNG")
    return output_path


def generate_cta_image(output_path="temp/cta_image.png"):
    from .cta_img_drawer import draw_cta_base
    base = draw_cta_base("temp/cta_base.png")
    return place_cta_text(base, output_path)
