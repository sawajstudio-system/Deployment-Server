# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/config/fonts/english_fonts.py
# 🎯 PURPOSE: इंग्लिश टेक्स्ट के लिए फॉन्ट चुनना (हर बार रैंडम)
# ══════════════════════════════════════════════════════════════════════════════

import random

# 🟢 इंग्लिश के प्रीमियम फॉन्ट्स (fonts फोल्डर में .ttf फाइलें मौजूद होनी चाहिए)
ENGLISH_FONTS = ["Playfair Display", "Cinzel", "Montserrat", "Lora"]

# 🎲 हर बार वीडियो बनने पर एक अलग फॉन्ट चुनेगा (ताकि हर वीडियो यूनिक लगे)
SELECTED_ENGLISH = random.choice(ENGLISH_FONTS)
