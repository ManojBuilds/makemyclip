import pysubs2
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
import re

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
#  2026 VIRAL PRESET — OpusClip-inspired
# ─────────────────────────────────────────────
VIRAL_PRESET = {
    "font_family": "TikTok Sans",  # punchy, thick
    "font_size": 52,  # base at 1080p
    "font_color": "#FFFFFF",
    "stroke_color": "#000000",
    "stroke_width": 4.5,
    "shadow": True,
    "shadow_depth": 2,
    "highlight_color": "#00F5FF",  # electric cyan (OpusClip signature)
    "power_words": {
        # Money & Success
        "$100",
        "$1,000",
        "$10,000",
        "$100,000",
        "million",
        "billion",
        "rich",
        "broke",
        "wealth",
        "money",
        "cash",
        "profit",
        "revenue",
        # Business & Career
        "ceo",
        "startup",
        "founder",
        "hired",
        "fired",
        "quit",
        "promoted",
        "6 figures",
        "7 figures",
        "8 figures",
        # High Emotion & Curiosity
        "secret",
        "never",
        "always",
        "insane",
        "crazy",
        "wild",
        "mind-blowing",
        "shocking",
        "unbelievable",
        "hidden",
        "forbidden",
        "dangerous",
        # Exaggeration & Power Words
        "best",
        "worst",
        "epic",
        "ultimate",
        "massive",
        "huge",
        "tiny",
        "stupid",
        "dumbest",
        "smartest",
        "easiest",
        "hardest",
        # Results & Speed
        "instantly",
        "overnight",
        "in 30 days",
        "in 7 days",
        "fast",
        "quick",
        "effortless",
        "simple",
        "hack",
        "trick",
        # Exclusivity & Urgency
        "only",
        "rare",
        "limited",
        "now",
        "today",
        "before",
        "after",
        "stop",
        "start",
        "finally",
        "revealed",
        # Controversy & Relatability
        "controversial",
        "nobody tells you",
        "they don't want you to know",
        "everyone is lying",
        "the truth is",
        "what they hid from you",
        # Viral Boosters
        "viral",
        "exploded",
        "blew up",
        "went viral",
        "changed everything",
        "game changer",
        "life changing",
        "you need this",
        "this changes everything",
    },
    "power_color": "#FFE600",  # yellow for $ / big claims
    "highlight_scale": 1.18,  # 18% pop on active word
    "power_scale": 1.30,  # 30% pop for power words
    "pop_duration_ms": 80,  # scale animation speed
    "window_size": 3,
    "position_y": 0.80,  # 80% down the frame (safe zone)
    "uppercase": True,
    "letter_spacing": 1.5,
    "background": False,
}


def hex_to_ass_color(hex_color: str, alpha: int = 0) -> pysubs2.Color:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 6:
        r, g, b = (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )
        return pysubs2.Color(r, g, b, alpha)
    elif len(hex_color) == 8:
        r, g, b = (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )
        a = int(hex_color[6:8], 16)
        return pysubs2.Color(r, g, b, 255 - a)
    return pysubs2.Color(255, 255, 255, 0)


def hex_to_ass_tag(hex_color: str) -> str:
    """#RRGGBB → \\c&HBBGGRR& (ASS is BGR order)"""
    h = hex_color.lstrip("#")
    if len(h) >= 6:
        r, g, b = h[0:2], h[2:4], h[4:6]
        return f"\\c&H{b}{g}{r}&"
    return "\\c&HFFFFFF&"


def _is_power_word(text: str, power_words: set) -> bool:
    clean = re.sub(r"[^\w$]", "", text.lower())
    return clean in power_words


def _build_karaoke_line(
    words: List[Dict[str, Any]],
    lo: int,
    hi: int,
    active_idx: int,
    style_fontsize: int,
    preset: Dict[str, Any],
) -> str:
    """
    Build a single dialogue line with OpusClip-style word-by-word highlight.
    Active word gets: color change + scale-pop animation.
    Power words get an even bigger yellow pop.
    """
    highlight_tag = hex_to_ass_tag(preset["highlight_color"])
    power_tag = hex_to_ass_tag(preset["power_color"])
    pieces = []

    for j in range(lo, hi):
        raw = words[j]["text"].strip()
        text = raw.upper() if preset.get("uppercase") else raw
        is_active = j == active_idx
        is_power = _is_power_word(raw, preset.get("power_words", set()))

        if is_active:
            color = power_tag if is_power else highlight_tag
            scale = preset["power_scale"] if is_power else preset["highlight_scale"]
            fs_active = int(style_fontsize * scale)
            dur = preset["pop_duration_ms"]
            # \t(0,dur,\fscx…\fscy…) — quick punch-in, stays scaled
            anim = f"\\t(0,{dur},\\fscx{int(scale*100)}\\fscy{int(scale*105)})"
            piece = f"{{{color}{anim}\\fs{fs_active}}}{text}{{\\r}}"
        else:
            # Dimmed context words — slightly transparent white
            piece = f"{{\\c&H99FFFFFF&\\fs{int(style_fontsize * 0.88)}}}{text}{{\\r}}"

        pieces.append(piece)

    return "  ".join(pieces)  # double-space for breathing room


from ..font_registry import find_font_path


def _build_default_style(
    subs: pysubs2.SSAFile,
    preset: Dict[str, Any],
    video_width: int,
    video_height: int,
    template: Dict[str, Any],
) -> pysubs2.SSAStyle:
    style = pysubs2.SSAStyle()

    # Font
    font_family = template.get("font_family", preset.get("font_family", "Montserrat ExtraBold"))
    resolved_path = find_font_path(font_family)
    # Even if we find a local path, we use the font_family name in the ASS file.
    # FFmpeg's fontsdir will scan the directory for a font with this Family Name.
    style.fontname = font_family
    base_fs = template.get("font_size", preset["font_size"])
    style.fontsize = max(20, int(base_fs * (video_height / 1920) * 1.8))

    # Colors
    style.primarycolor = hex_to_ass_color(
        template.get("font_color", preset["font_color"])
    )
    style.outlinecolor = hex_to_ass_color(
        template.get("stroke_color", preset["stroke_color"])
    )
    style.backcolor = hex_to_ass_color(
        template.get("background_color", "#00000080")
        if template.get("background")
        else "#00000000"
    )

    # Weight / decoration
    style.bold = True
    style.outline = template.get("stroke_width", preset["stroke_width"]) * (
        video_height / 1080
    )
    style.shadow = preset["shadow_depth"] if preset.get("shadow") else 0
    style.spacing = preset.get("letter_spacing", 1.5)

    # Border style
    style.borderstyle = 3 if template.get("background") else 1

    # Position — bottom-center safe zone
    style.alignment = 2
    pos_y = template.get("position_y", preset["position_y"])
    style.marginv = int(video_height * (1.0 - pos_y))
    style.marginl = int(video_width * 0.08)
    style.marginr = int(video_width * 0.08)

    subs.styles["Default"] = style
    return style


def generate_ass_file(
    words: List[Dict[str, Any]],
    output_path: Path,
    template: Dict[str, Any],
    video_width: int,
    video_height: int,
    preset: Optional[Dict[str, Any]] = None,
) -> Path:
    """
    Generate an OpusClip-style .ass subtitle file.

    Args:
        words:        List of {"text": str, "start": float, "end": float}
        output_path:  Where to save the .ass file
        template:     User/app overrides (font_size, highlight_color, etc.)
        video_width:  Frame width  (e.g. 606 for 9:16 short-form)
        video_height: Frame height (e.g. 1080)
        preset:       Override the default VIRAL_PRESET (optional)
    """
    p = {**VIRAL_PRESET, **(preset or {})}  # merge presets
    p = {**p, **{k: v for k, v in template.items() if v is not None}}  # template wins

    subs = pysubs2.SSAFile()
    subs.info["PlayResX"] = str(video_width)
    subs.info["PlayResY"] = str(video_height)
    subs.info["WrapStyle"] = "0"
    subs.info["ScaledBorderAndShadow"] = "yes"

    style = _build_default_style(subs, p, video_width, video_height, template)

    animation = template.get("animation", "karaoke")
    window_size = int(p.get("window_size", 3))
    n = len(words)

    # ── KARAOKE (OpusClip default) ───────────────────────────────────────────
    if animation == "karaoke":
        for i, word in enumerate(words):
            half = window_size // 2
            lo = max(0, i - half)
            hi = min(n, lo + window_size)
            lo = max(0, hi - window_size)  # re-clamp lo after hi adjustment

            line = _build_karaoke_line(words, lo, hi, i, style.fontsize, p)
            start = int(word["start"] * 1000)
            end = int(word["end"] * 1000)
            if i == n - 1:
                end += 250  # hold last word slightly longer

            subs.append(pysubs2.SSAEvent(start=start, end=end, text=line))

    # ── POP (groups, no word-level highlight) ────────────────────────────────
    elif animation in ("pop", "none"):
        for i in range(0, n, window_size):
            group = words[i : i + window_size]
            if not group:
                continue
            text = "  ".join(
                w["text"].upper() if p.get("uppercase") else w["text"] for w in group
            )
            start = int(group[0]["start"] * 1000)
            end = int(group[-1]["end"] * 1000)
            # Tiny scale-in punch for the whole block
            text = f"{{\\t(0,100,\\fscx105\\fscy108)}}{text}"
            subs.append(pysubs2.SSAEvent(start=start, end=end, text=text))

    # ── FADE ────────────────────────────────────────────────────────────────
    elif animation == "fade":
        for i in range(0, n, window_size):
            group = words[i : i + window_size]
            if not group:
                continue
            text = "  ".join(
                w["text"].upper() if p.get("uppercase") else w["text"] for w in group
            )
            text = f"{{\\fad(150,150)}}{text}"
            start = int(group[0]["start"] * 1000)
            end = int(group[-1]["end"] * 1000)
            subs.append(pysubs2.SSAEvent(start=start, end=end, text=text))

    subs.save(str(output_path), format_="ass")
    logger.info(f"Saved ASS file → {output_path}  ({len(subs)} events)")
    return output_path
