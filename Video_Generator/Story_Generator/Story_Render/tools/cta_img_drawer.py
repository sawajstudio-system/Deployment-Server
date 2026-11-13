# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/tools/cta_img_drawer.py
# ══════════════════════════════════════════════════════════════════════════════

import os
from PIL import Image, ImageDraw


def draw_cta_base(output_path="temp/cta_base.png"):
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    glass_fill = (15, 15, 15, 150)
    glass_border = (255, 255, 255, 80)

    # 🟢 कार्ड को बड़ा किया ताकि बड़े बटन्स फिट हो सकें
    draw.rounded_rectangle(
        [230, 1150, 850, 1750], # ऊपर और नीचे की जगह बढ़ा दी
        radius=30,
        fill=glass_fill,
        outline=glass_border,
        width=3
    )

    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    img.save(output_path, "PNG")
    return output_path
