import random

PLAY_RES_X = 1080
PLAY_RES_Y = 1920

ARABIC_FONTS = ["Amiri", "Reem Kufi", "Scheherazade"]
HINDI_FONTS = ["Yatra One", "Rozha One", "Eczar"]
ENGLISH_FONTS = ["Playfair Display", "Cinzel", "Montserrat", "Lora"]

SELECTED_ARABIC = random.choice(ARABIC_FONTS)
SELECTED_HINDI = random.choice(HINDI_FONTS)
SELECTED_ENGLISH = random.choice(ENGLISH_FONTS)

# 🟢 Alignment: 1 का मतलब है Left-Align (बाईं तरफ)। 
# इससे डॉट्स एकदम सीध में रहेंगे और कभी नहीं हिलेंगे।
ARABIC_STYLE = {"font": SELECTED_ARABIC, "size": 85, "alignment": 1, "margin_l": 150, "margin_v": 700, "bold": -1}
HINDI_STYLE = {"font": SELECTED_HINDI, "size": 75, "alignment": 1, "margin_l": 150, "margin_v": 550, "bold": -1}
ENGLISH_STYLE = {"font": SELECTED_ENGLISH, "size": 60, "alignment": 1, "margin_l": 150, "margin_v": 400, "bold": -1}

INTRO_STYLE = {"font": SELECTED_ENGLISH, "size": 70, "alignment": 8, "margin_v": 200, "bold": -1}
OUTRO_STYLE = {"font": SELECTED_ENGLISH, "size": 80, "alignment": 8, "margin_v": 250, "bold": -1}
CTA_STYLE = {"font": SELECTED_ENGLISH, "size": 60, "alignment": 2, "margin_v": 600, "bold": -1}

def generate_ass_style_string(name, style_dict):
    primary_colour = "&H00FFFFFF&" 
    outline_colour = "&H00000000&"
    return (
        f"Style: {name},{style_dict['font']},{style_dict['size']},"
        f"{primary_colour},&H000000FF&,{outline_colour},&H80000000,"
        f"{style_dict['bold']},0,0,0,100,100,0,0,1,3,2,"
        f"{style_dict['alignment']},40,40,{style_dict['margin_v']},1"
    )
