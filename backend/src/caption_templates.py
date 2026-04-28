"""
Caption template definitions for animated subtitles.
2026 viral-optimized — OpusClip inspired.

Font size guide (for 1080p vertical / 9:16):
  - generate_ass.py multiplier: base_fs * (video_height / 1920) * 1.8
  - OpusClip sweet spot: 38–44 base → ~12–14% of frame height
  - Sports/hype styles: 48 max

RoyLee style:
  - hook_text fed separately (the big 3s opening statement)
  - hook renders center-frame in a bold rounded dark pill
  - subtitle renders bottom, small, lowercase, clean
"""

from typing import Dict, Any, Literal, Optional, List

AnimationType = Literal["none", "karaoke", "pop", "fade", "bounce", "roylee"]

CAPTION_TEMPLATES: Dict[str, Dict[str, Any]] = {
    # ──────────────────────────────────────────────────────────────────────────
    #  CORE / GENERAL
    # ──────────────────────────────────────────────────────────────────────────
    "default": {
        "name": "Default",
        "description": "Clean white text with black outline",
        "font_family": "Montserrat ExtraBold",
        "font_size": 38,
        "font_color": "#FFFFFF",
        "highlight_color": "#00F5FF",
        "stroke_color": "#000000",
        "stroke_width": 4.5,
        "background": False,
        "background_color": None,
        "animation": "karaoke",
        "shadow": True,
        "shadow_depth": 2,
        "letter_spacing": 1.5,
        "uppercase": True,
        "highlight_scale": 1.18,
        "power_color": "#FFE600",
        "position_y": 0.80,
    },
    "minimal": {
        "name": "Minimal",
        "description": "Elegant and subtle with a frosted dark background",
        "font_family": "Montserrat SemiBold",
        "font_size": 28,
        "font_color": "#FFFFFF",
        "highlight_color": "#FFD700",
        "stroke_color": None,
        "stroke_width": 0,
        "background": True,
        "background_color": "#000000AA",
        "animation": "fade",
        "shadow": False,
        "shadow_depth": 0,
        "letter_spacing": 1.0,
        "uppercase": False,
        "highlight_scale": 1.10,
        "power_color": "#FFD700",
        "position_y": 0.82,
    },
    # ──────────────────────────────────────────────────────────────────────────
    #  ROY LEE — Hook + Subtitle dual-layer style
    # ──────────────────────────────────────────────────────────────────────────
    "roylee": {
        "name": "Roy Lee",
        "description": "Big bold hook pill center-frame for 3s, then small clean subtitle at bottom",
        "animation": "roylee",
        # ── HOOK (top big pill) ─────────────────────────────────────────────
        "hook_font_family": "Montserrat ExtraBold",
        "hook_font_size": 46,  # large, fills center pill nicely
        "hook_font_color": "#FFFFFF",
        "hook_background_color": "#CC000000",  # dark semi-transparent pill
        "hook_stroke_color": None,
        "hook_stroke_width": 0,
        "hook_uppercase": False,  # sentence case like the screenshot
        "hook_bold_words": True,  # highlight caps words (NOT, NEVER etc.)
        "hook_bold_color": "#FFFFFF",  # stays white — weight carries emphasis
        "hook_duration_s": 3.0,  # how long the hook sits on screen
        "hook_position_y": 0.38,  # center-ish, just above midpoint
        "hook_max_chars_per_line": 22,  # forces natural 2-line wrap
        # ── SUBTITLE (bottom small) ─────────────────────────────────────────
        "font_family": "Montserrat SemiBold",
        "font_size": 22,  # intentionally small — supporting role
        "font_color": "#FFFFFF",
        "highlight_color": "#FFFFFF",  # no color pop — stays minimal
        "stroke_color": "#000000",
        "stroke_width": 2.5,
        "background": False,
        "background_color": None,
        "shadow": True,
        "shadow_depth": 1,
        "letter_spacing": 0.5,
        "uppercase": False,  # lowercase like the screenshot
        "highlight_scale": 1.0,  # no pop scale — clean and calm
        "power_color": "#FFFFFF",
        "position_y": 0.88,  # near bottom, above thumb zone
    },
    # ──────────────────────────────────────────────────────────────────────────
    #  CREATOR / INFLUENCER STYLES
    # ──────────────────────────────────────────────────────────────────────────
    "hormozi": {
        "name": "Hormozi",
        "description": "Ultra-bold, lime green word pop — high-energy business content",
        "font_family": "Montserrat ExtraBold",
        "font_size": 46,
        "font_color": "#FFFFFF",
        "highlight_color": "#00FF57",
        "stroke_color": "#000000",
        "stroke_width": 5.5,
        "background": False,
        "background_color": None,
        "animation": "karaoke",
        "shadow": True,
        "shadow_depth": 3,
        "letter_spacing": 2.0,
        "uppercase": True,
        "highlight_scale": 1.22,
        "power_color": "#FFE600",
        "position_y": 0.70,
    },
    "mrbeast": {
        "name": "MrBeast",
        "description": "Signature yellow-on-black with white active word — high-contrast hook style",
        "font_family": "Montserrat ExtraBold",
        "font_size": 44,
        "font_color": "#FFE600",
        "highlight_color": "#FFFFFF",
        "stroke_color": "#000000",
        "stroke_width": 5,
        "background": False,
        "background_color": None,
        "animation": "karaoke",
        "shadow": True,
        "shadow_depth": 3,
        "letter_spacing": 1.5,
        "uppercase": True,
        "highlight_scale": 1.20,
        "power_color": "#FF3A3A",
        "position_y": 0.68,
    },
    "tiktok": {
        "name": "TikTok",
        "description": "TikTok pink brand color with white active highlight",
        "font_family": "TikTok Sans",
        "font_size": 38,
        "font_color": "#FFFFFF",
        "highlight_color": "#FE2C55",
        "stroke_color": "#000000",
        "stroke_width": 4,
        "background": False,
        "background_color": None,
        "animation": "karaoke",
        "shadow": True,
        "shadow_depth": 2,
        "letter_spacing": 1.5,
        "uppercase": True,
        "highlight_scale": 1.15,
        "power_color": "#FFE600",
        "position_y": 0.75,
    },
    # ──────────────────────────────────────────────────────────────────────────
    #  PLATFORM / CLIP STYLES
    # ──────────────────────────────────────────────────────────────────────────
    "opus": {
        "name": "Opus",
        "description": "Premium clipping — electric cyan pop, heavy outline, yellow for power words",
        "font_family": "Montserrat ExtraBold",
        "font_size": 40,
        "font_color": "#FFFFFF",
        "highlight_color": "#00F5FF",
        "stroke_color": "#000000",
        "stroke_width": 5,
        "background": False,
        "background_color": None,
        "animation": "karaoke",
        "shadow": True,
        "shadow_depth": 2,
        "letter_spacing": 1.5,
        "uppercase": True,
        "highlight_scale": 1.20,
        "power_color": "#FFE600",
        "position_y": 0.80,
    },
    "viral": {
        "name": "Viral",
        "description": "Max readability — lime pop, extra-heavy outline, optimized for silent viewers",
        "font_family": "Montserrat ExtraBold",
        "font_size": 44,
        "font_color": "#FFFFFF",
        "highlight_color": "#39FF14",
        "stroke_color": "#000000",
        "stroke_width": 6,
        "background": False,
        "background_color": None,
        "animation": "karaoke",
        "shadow": True,
        "shadow_depth": 3,
        "letter_spacing": 2.0,
        "uppercase": True,
        "highlight_scale": 1.25,
        "power_color": "#FF3A3A",
        "position_y": 0.72,
    },
    "neon": {
        "name": "Neon",
        "description": "Cyberpunk cyan/magenta glow — edgy, nightlife, tech content",
        "font_family": "Montserrat ExtraBold",
        "font_size": 40,
        "font_color": "#00FFFF",
        "highlight_color": "#FF00FF",
        "stroke_color": "#000000",
        "stroke_width": 4,
        "background": False,
        "background_color": None,
        "animation": "karaoke",
        "shadow": True,
        "shadow_depth": 3,
        "letter_spacing": 2.0,
        "uppercase": True,
        "highlight_scale": 1.18,
        "power_color": "#FF3A3A",
        "position_y": 0.72,
    },
    # ──────────────────────────────────────────────────────────────────────────
    #  LONG-FORM / PODCAST
    # ──────────────────────────────────────────────────────────────────────────
    "podcast": {
        "name": "Podcast",
        "description": "Premium rounded box with generous padding — modern podcast look",
        "font_family": "Montserrat SemiBold",
        "font_size": 33,
        "font_color": "#F8F9FA",
        "highlight_color": "#F4A261",
        "stroke_color": None,
        "stroke_width": 0,
        "background": True,
        "background_color": "#1A1A1AEE",
        "background_padding_x": 32,
        "background_padding_y": 22,
        "background_radius": 24,  # Nicer roundness
        "background_width_multiplier": 1.10,
        "animation": "pop",
        "shadow": True,
        "shadow_depth": 6,
        "shadow_color": "#00000099",
        "letter_spacing": 0.6,
        "uppercase": False,
        "highlight_scale": 1.08,
        "power_color": "#FFCC33",
        "position_y": 0.80,
    },
    "interview": {
        "name": "Interview",
        "description": "Calm and readable — white on semi-transparent dark pill, subtle fade",
        "font_family": "Montserrat SemiBold",
        "font_size": 30,
        "font_color": "#FFFFFF",
        "highlight_color": "#FFD700",
        "stroke_color": None,
        "stroke_width": 0,
        "background": True,
        "background_color": "#00000099",
        "animation": "fade",
        "shadow": False,
        "shadow_depth": 0,
        "letter_spacing": 1.0,
        "uppercase": False,
        "highlight_scale": 1.08,
        "power_color": "#FFD700",
        "position_y": 0.80,
    },
    # ──────────────────────────────────────────────────────────────────────────
    #  NICHE / AESTHETIC
    # ──────────────────────────────────────────────────────────────────────────
    "cinema": {
        "name": "Cinema",
        "description": "Letterbox subtitle aesthetic — lowercase, centered, refined fade",
        "font_family": "EB Garamond",
        "font_size": 26,
        "font_color": "#F5F0E8",
        "highlight_color": "#F5F0E8",
        "stroke_color": "#000000",
        "stroke_width": 2,
        "background": False,
        "background_color": None,
        "animation": "fade",
        "shadow": True,
        "shadow_depth": 2,
        "letter_spacing": 0.5,
        "uppercase": False,
        "highlight_scale": 1.0,
        "power_color": "#F5F0E8",
        "position_y": 0.88,
    },
    "sports": {
        "name": "Sports",
        "description": "High-energy ESPN-style — red/white, thick outline, full caps",
        "font_family": "Montserrat ExtraBold",
        "font_size": 48,
        "font_color": "#FFFFFF",
        "highlight_color": "#FF3A3A",
        "stroke_color": "#000000",
        "stroke_width": 6,
        "background": False,
        "background_color": None,
        "animation": "karaoke",
        "shadow": True,
        "shadow_depth": 3,
        "letter_spacing": 2.5,
        "uppercase": True,
        "highlight_scale": 1.28,
        "power_color": "#FFE600",
        "position_y": 0.70,
    },
}


# ──────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────────────────────────────────────


def get_template(template_name: str) -> Dict[str, Any]:
    """Get a caption template by name, returns 'default' if not found."""
    return CAPTION_TEMPLATES.get(template_name, CAPTION_TEMPLATES["default"])


def get_all_templates() -> Dict[str, Dict[str, Any]]:
    """Get all available caption templates."""
    return CAPTION_TEMPLATES


def get_template_names() -> List[str]:
    """Get list of all template names."""
    return list(CAPTION_TEMPLATES.keys())


def get_template_info() -> List[Dict[str, Any]]:
    """Get list of template info dicts for API responses."""
    return [
        {
            "id": key,
            "name": t["name"],
            "description": t["description"],
            "animation": t["animation"],
            "font_family": t.get("font_family", t.get("hook_font_family")),
            "font_size": t.get("font_size", t.get("hook_font_size")),
            "font_color": t.get("font_color", t.get("hook_font_color")),
            "highlight_color": t.get("highlight_color"),
            "power_color": t.get("power_color"),
            "uppercase": t.get("uppercase", False),
            "highlight_scale": t.get("highlight_scale", 1.0),
        }
        for key, t in CAPTION_TEMPLATES.items()
    ]
