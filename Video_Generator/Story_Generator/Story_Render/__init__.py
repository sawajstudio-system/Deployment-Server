# ══════════════════════════════════════════════════════════════════════════════
# 📁 FILE: Story_Render/__init__.py
# 🎯 PURPOSE: Story_Render package का मुख्य entry point
#            बाहर से सिर्फ `build_and_render_story` import करने की सुविधा
# ══════════════════════════════════════════════════════════════════════════════

from .main_render import build_and_render_story

__version__ = "2.0.0"
__author__  = "Sawaj Studio"

__all__ = ["build_and_render_story"]
