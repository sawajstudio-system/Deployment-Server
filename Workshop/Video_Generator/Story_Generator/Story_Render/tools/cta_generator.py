import os
from PIL import Image, ImageDraw, ImageFont
def generate_cta_image(output_path="temp/cta_image.png"):
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font_top = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", 55)
        font_btn = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", 75)
        font_bottom = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", 45)
    except IOError:
        font_top = font_btn = font_bottom = ImageFont.load_default()
    draw.text((540, 650), "Like • Subscribe • Comment • Follow", font=font_top, fill="white", anchor="mm", stroke_width=3, stroke_fill="black")
    buttons = [{"text": "LIKE", "color": "#00FF00", "y": 800}, {"text": "SUBSCRIBE", "color": "#FF0000", "y": 930}, {"text": "COMMENT", "color": "#00BFFF", "y": 1060}, {"text": "FOLLOW", "color": "#FFD700", "y": 1190}]
    for btn in buttons:
        draw.rectangle([310, btn["y"], 770, btn["y"] + 90], outline=btn["color"], width=6)
        draw.text((540, btn["y"] + 45), btn["text"], font=font_btn, fill=btn["color"], anchor="mm", stroke_width=3, stroke_fill="black")
    draw.text((540, 1750), "Sawajstudio", font=font_bottom, fill="white", anchor="mm", stroke_width=3, stroke_fill="black")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    return output_path
