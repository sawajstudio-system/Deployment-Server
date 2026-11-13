def get_logo_filter(logo_width=400, logo_height=160):
    fb_blue_filter = (
        f"scale={logo_width}:{logo_height},format=rgba,"
        f"colorchannelmixer=rr=0.094:gg=0.466:bb=0.949:aa=1.0,"
        f"split[logo][shadow];"
        f"[shadow]colorchannelmixer=rr=0:gg=0:bb=0:aa=0.9,boxblur=10:2[shadow_blur];"   
        f"[shadow_blur][logo]overlay=6:6"
    )
    return fb_blue_filter
