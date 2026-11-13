import os

def get_logo_filter(logo_width=250, logo_height=80):
    """
    यह फंक्शन Logo को प्रोसेस करने के लिए FFmpeg फिल्टर देता है।
    - Facebook Blue रंग और पीछे हल्की परछाई (Shadow)।
    """
    fb_blue_filter = (
        f"scale={logo_width}:{logo_height},format=rgba,"
        f"colorchannelmixer=rr=0.094:gg=0.466:bb=0.949:aa=1.0," # Facebook Blue Color
        f"split[logo][shadow];"
        f"[shadow]colorchannelmixer=rr=0:gg=0:bb=0:aa=0.7,boxblur=8:2[shadow_blur];" # Soft shadow
        f"[shadow_blur][logo]overlay=5:5"
    )
    return fb_blue_filter
