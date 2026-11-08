import os
def get_logo_filter(logo_path="assets/logo.png", logo_width=150, opacity=0.8, margin=40):
    if not os.path.exists(logo_path): return "", ""
    return f"scale={logo_width}:-1,format=rgba,colorchannelmixer=aa={opacity}", logo_path
