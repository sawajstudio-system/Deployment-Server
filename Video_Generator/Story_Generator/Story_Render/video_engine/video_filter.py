from .logo_processor import get_logo_filter
from .logo_placer import get_moving_logo_expr, get_fixed_logo_pos

def build_video_filter(has_logo, logo_idx, cta_idx, cta_start_time):
    # ✅ ORIGINAL: scale + crop + vignette (Background clearly visible)
    filters = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,vignette=PI/4[bg];"
    )
    current_v_out = "bg"

    if has_logo and logo_idx != -1:
        logo_filter_moving = get_logo_filter(logo_width=400, logo_height=160)
        logo_filter_fixed = get_logo_filter(logo_width=600, logo_height=240)

        filters += f"[{logo_idx}:v]split[logo_mov][logo_fix];"
        filters += f"[logo_mov]{logo_filter_moving}[logo_mov_scaled];"
        filters += f"[logo_fix]{logo_filter_fixed}[logo_fix_scaled];"

        x_expr, y_expr = get_moving_logo_expr()
        filters += (
            f"[{current_v_out}][logo_mov_scaled]"
            f"overlay=x='{x_expr}':y='{y_expr}':enable='lt(t,{cta_start_time})'"
            f"[bg_with_moving_logo];"
        )

        fx, fy = get_fixed_logo_pos()
        filters += (
            f"[bg_with_moving_logo][logo_fix_scaled]"
            f"overlay=x='{fx}':y='{fy}':enable='gte(t,{cta_start_time})'"
            f"[bg_with_logo];"
        )
        current_v_out = "bg_with_logo"

    return filters, current_v_out
