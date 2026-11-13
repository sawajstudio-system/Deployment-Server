# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/builders/main_sub_builder.py
# 🎯 PURPOSE: मुख्य (कराओके) सबटाइटल बनाना — अरबी + हिंदी + इंग्लिश के लिए
#            हर शब्द अपने टाइम पर हाइलाइट (कराओके) होता है
# ══════════════════════════════════════════════════════════════════════════════

from ..assembler import get_ass_header, get_all_styles, save_ass
from ..timing import ts, compute_word_timings
from ..languages import build_arabic_text, build_hindi_text, build_english_text
from ...config.colors import get_color_tag


# ══════════════════════════════════════════════════════════════════════════════
# 🎬 MAIN FUNCTION
# ══════════════════════════════════════════════════════════════════════════════
def create_main_subtitles(hadith, hindi_text, duration, output_path="temp/main_subtitles.ass"):
    """
    मुख्य सबटाइटल फाइल बनाता है जिसमें तीनों भाषाएँ कराओके-स्टाइल में दिखती हैं।

    Args:
        hadith (dict): जिसमें "arabic" और "english" keys हों
        hindi_text (str): हिंदी अनुवाद
        duration (float): वीडियो की कुल लंबाई (सेकंड में)
        output_path (str): कहाँ सेव करना है

    Returns:
        str: बनी हुई ASS फाइल का path
    """
    print("✍️ [main_sub_builder] Building Left-Aligned Smooth Subtitles...")

    # ── 1. टेक्स्ट तैयार करो (तीनों भाषाओं में) ─────────────────────────────
    ara_text = build_arabic_text(hadith.get("arabic", ""))
    hin_text = build_hindi_text(hindi_text)
    eng_text = build_english_text(hadith.get("english", ""))

    # ── 2. ASS फाइल का हेडर + स्टाइल ───────────────────────────────────────
    content = get_ass_header()
    content += "\n[V4+ Styles]\n"
    content += get_all_styles()
    content += "\n[Events]\n"
    content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    # ── 3. टाइम रेंज (शुरुआत में 4s इंट्रो, आखिर में 5.5s आउट्रो/CTA) ──────
    start_t = 4.0
    end_t = max(duration - 5.5, start_t + 1.0)
    total_dur = end_t - start_t

    # ══════════════════════════════════════════════════════════════════════════
    # 🎯 INTERNAL FUNCTION: एक भाषा के लिए कराओके लाइनें बनाना
    # ══════════════════════════════════════════════════════════════════════════
    def process_language(text, style_name, lang_idx):
        """
        एक भाषा के हर शब्द के लिए एक Dialogue लाइन बनाता है।
        - पिछले 3 शब्द ही स्क्रीन पर दिखते हैं (window sliding)
        - हर शब्द अपने टाइम पर हाइलाइट होता है
        - हर 3 शब्दों पर डॉट (●) का रंग बदलता है
        """
        words = text.split()
        if not words:
            return ""

        # हर शब्द का समय निकालो (विराम चिह्नों के हिसाब से वज़न)
        timings = compute_word_timings(words, total_dur)

        window_size = 3   # स्क्रीन पर एक बार में कितने शब्द दिखें
        lines = ""

        for i in range(len(words)):
            w_start = start_t + timings[i][0]
            w_end = start_t + timings[i][1]

            start_idx = max(0, i - window_size + 1)
            visible_words = words[start_idx:i + 1]

            # डॉट का रंग हर 3 शब्दों पर बदलता है
            dot_color = get_color_tag(i // 3 + (lang_idx * 3))

            # अरबी के लिए RTL मार्क, बाकी के लिए सीधा डॉट
            if lang_idx == 0:   # अरबी
                karaoke_text = f"\u202B{{\\c{dot_color}}}●  "
            else:
                karaoke_text = f"{{\\c{dot_color}}}●  "

            # सभी visible शब्द जोड़ो (current word highlight के साथ)
            for j, word in enumerate(visible_words):
                global_idx = start_idx + j
                color = get_color_tag(global_idx)

                if global_idx == i:
                    # Current word — कराओके हाइलाइट (k tag)
                    cs = int((w_end - w_start) * 100)
                    karaoke_text += f"{{\\c{color}\\k{cs}}}{word} "
                else:
                    # पिछले शब्द — सामान्य रंग
                    karaoke_text += f"{{\\c{color}}}{word} "

            # अरबी RTL बंद करो
            if lang_idx == 0:
                karaoke_text += "\u202C"

            lines += f"Dialogue: 0,{ts(w_start)},{ts(w_end)},{style_name},,,0,0,,{karaoke_text.strip()}\n"

        return lines

    # ── 4. तीनों भाषाओं की लाइनें जोड़ो ────────────────────────────────────
    if ara_text:
        content += process_language(ara_text, "Arabic", 0)
    if hin_text:
        content += process_language(hin_text, "Hindi", 1)
    if eng_text:
        content += process_language(eng_text, "English", 2)

    # ── 5. फाइल सेव करो ─────────────────────────────────────────────────────
    return save_ass(content, output_path)
