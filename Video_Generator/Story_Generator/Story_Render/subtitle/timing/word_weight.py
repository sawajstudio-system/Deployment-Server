# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/subtitle/timing/word_weight.py
# 🎯 PURPOSE: हर शब्द के लिए समय (Timing) निकालना — विराम चिह्नों के हिसाब से
# ══════════════════════════════════════════════════════════════════════════════

def compute_word_timings(words, total_dur):
    """
    हर शब्द को उसके वज़न (weight) के हिसाब से समय देता है।
    - वाक्य खत्म करने वाले चिह्न (. ! ? ।) → 2x वज़न (ज्यादा रुकाव)
    - बीच के चिह्न (, ، ; :) → 1.5x वज़न (थोड़ा रुकाव)
    - सामान्य शब्द → 1x वज़न

    Args:
        words (list): शब्दों की सूची
        total_dur (float): कुल अवधि (सेकंड में)

    Returns:
        list of tuples: [(start, end), (start, end), ...] सेकंड में
    """
    if not words:
        return []

    # ── 1. हर शब्द का वज़न निकालो ───────────────────────────────────────────
    weights = []
    for w in words:
        if not w:
            weights.append(1.0)
            continue

        last_char = w[-1]
        if last_char in ['.', '!', '?', '।']:
            weights.append(2.0)
        elif last_char in [',', '،', ';', ':']:
            weights.append(1.5)
        else:
            weights.append(1.0)

    # ── 2. एक वज़न यूनिट का समय निकालो ─────────────────────────────────────
    total_weight = sum(weights) or 1.0
    time_per_weight = total_dur / total_weight

    # ── 3. हर शब्द का (start, end) टाइम बनाओ ───────────────────────────────
    timings = []
    current_time = 0.0
    for weight in weights:
        duration_w = weight * time_per_weight
        timings.append((current_time, current_time + duration_w))
        current_time += duration_w

    return timings
