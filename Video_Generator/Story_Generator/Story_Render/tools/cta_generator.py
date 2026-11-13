import os, random
from PIL import Image, ImageDraw, ImageFont

def generate_cta_image(output_path="temp/cta_image.png"):
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font_top = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", 55)
        font_btn = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", 65)
        font_bottom = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", 45)
    except IOError:
        font_top = font_btn = font_bottom = ImageFont.load_default()

    colors = ["#FFD700", "#00FFFF", "#FF007F", "#39FF14", "#FFBF00", "#9D00FF", "#00FF7F", "#FF4500"]
    random.shuffle(colors)

    # 🟢 ग्लास इफेक्ट (Glass Card) - बटन्स के पीछे एक सुंदर ट्रांसपेरेंट बॉक्स
    glass_fill = (15, 15, 15, 150)      # डार्क ट्रांसपेरेंट
    glass_border = (255, 255, 255, 80)  # वाइट बॉर्डर
    draw.rounded_rectangle([250, 1200, 830, 1700], radius=30, fill=glass_fill, outline=glass_border, width=3)

    # 1. हेडर टेक्स्ट
    header_texts = ["Like • Share • Follow", "Support the Channel", "Join Our Community", "Spread the Knowledge"]
    draw.text((540, 1280), random.choice(header_texts), font=font_top, fill=colors[0], anchor="mm", stroke_width=4, stroke_fill="black")

    # 2. बटन्स
    btn_texts = [["LIKE", "SUBSCRIBE", "COMMENT", "SHARE"], ["FOLLOW", "SHARE", "LIKE", "SUBSCRIBE"], ["SUBSCRIBE", "LIKE", "FOLLOW", "COMMENT"]]
    texts = random.choice(btn_texts)
    
    buttons = [
        {"text": texts[0], "color": colors[1], "y": 1350}, 
        {"text": texts[1], "color": colors[2], "y": 1430}, 
        {"text": texts[2], "color": colors[3], "y": 1510}, 
        {"text": texts[3], "color": colors[4], "y": 1590}
    ]
    
    for btn in buttons:
        # बटन के अंदर का ग्लास कलर
        draw.rounded_rectangle([310, btn["y"], 770, btn["y"] + 65], radius=10, outline=btn["color"], width=4)
        draw.text((540, btn["y"] + 32), btn["text"], font=font_btn, fill=btn["color"], anchor="mm", stroke_width=3, stroke_fill="black")
    
    # 3. स्टूडियो का नाम
    draw.text((540, 1780), "Sawajstudio", font=font_bottom, fill=colors[5], anchor="mm", stroke_width=3, stroke_fill="black")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    return output_path
