"""
widgets — 共用 GUI 元件與主題設定
Modern & Clean 風格，使用 CustomTkinter
"""

import customtkinter as ctk
import tkinter as tk
import subprocess
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ── 色彩主題 ──
COLORS = {
    "bg":             "#F0F2F8",
    "bg_card":        "#FFFFFF",
    "bg_dark":        "#1E1B4B",
    "bg_dark_card":   "#2D2A6B",
    "primary":        "#4F46E5",
    "primary_hover":  "#4338CA",
    "primary_light":  "#EEF2FF",
    "secondary":      "#0EA5E9",
    "success":        "#22C55E",
    "success_light":  "#DCFCE7",
    "error":          "#EF4444",
    "error_light":    "#FEE2E2",
    "warning":        "#F59E0B",
    "text":           "#1E1B4B",
    "text_muted":     "#64748B",
    "text_light":     "#FFFFFF",
    "text_dim":       "#A5B4FC",
    "border":         "#E2E8F0",
    "border_dark":    "#3D3A7A",
    "option_bg":      "#F8FAFC",
    "option_hover":   "#EEF2FF",
    "accent_pink":    "#EC4899",
    "accent_purple":  "#8B5CF6",
    "accent_mint":    "#14B8A6",
    "white":          "#FFFFFF",
    # backward compat
    "gradient_top":   "#EEF2FF",
    "gradient_bot":   "#E0E7FF",
    "shadow":         "#C7D2FE",
}

# ── 字型 ──
FONTS = {
    "title":       ("Hiragino Maru Gothic ProN", 30, "bold"),
    "subtitle":    ("Hiragino Maru Gothic ProN", 16),
    "heading":     ("Hiragino Maru Gothic ProN", 22, "bold"),
    "body":        ("Hiragino Maru Gothic ProN", 14),
    "body_bold":   ("Hiragino Maru Gothic ProN", 14, "bold"),
    "small":       ("Hiragino Maru Gothic ProN", 11),
    "tiny":        ("Hiragino Maru Gothic ProN", 10),
    "japanese_lg": ("Hiragino Maru Gothic ProN", 36, "bold"),
    "japanese_md": ("Hiragino Maru Gothic ProN", 22),
    "japanese_sm": ("Hiragino Maru Gothic ProN", 16),
    "button":      ("Hiragino Maru Gothic ProN", 14, "bold"),
    "score":       ("Hiragino Maru Gothic ProN", 52, "bold"),
}


# ── 音效管理器 ──
class SoundManager:
    _SOUNDS = {
        "click":    "/System/Library/Sounds/Tink.aiff",
        "correct":  "/System/Library/Sounds/Glass.aiff",
        "wrong":    "/System/Library/Sounds/Basso.aiff",
        "unlock":   "/System/Library/Sounds/Hero.aiff",
        "complete": "/System/Library/Sounds/Purr.aiff",
        "pop":      "/System/Library/Sounds/Pop.aiff",
    }

    def __init__(self):
        self.enabled = True

    def play(self, name: str):
        if not self.enabled:
            return
        path = self._SOUNDS.get(name)
        if path and os.path.exists(path):
            try:
                subprocess.Popen(["afplay", path],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
            except Exception:
                pass


sound = SoundManager()


# ── 動畫工具 ──
def count_up_animation(label, target: int, root, duration_ms=800):
    steps = 20
    delay = duration_ms // steps

    def _step(current):
        if current > target:
            current = target
        label.configure(text=str(current))
        if current < target:
            root.after(delay, _step, current + max(1, (target - current) // 4))

    _step(0)


def animate_progress_bar(bar, root, duration_ms=2200, steps=60, on_done=None):
    delay = duration_ms // steps

    def _step(i):
        bar.set(i / steps)
        if i < steps:
            root.after(delay, _step, i + 1)
        elif on_done:
            root.after(200, on_done)

    root.after(100, _step, 0)


# ── 漸層背景 Canvas (保留給解鎖全螢幕用) ──
def create_gradient_canvas(parent, width=900, height=650,
                           color1=None, color2=None):
    color1 = color1 or COLORS["gradient_top"]
    color2 = color2 or COLORS["gradient_bot"]

    canvas = tk.Canvas(parent, width=width, height=height,
                       highlightthickness=0, bd=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    r1, g1, b1 = _hex_to_rgb(color1)
    r2, g2, b2 = _hex_to_rgb(color2)
    steps = height // 4
    for i in range(steps):
        ratio = i / steps
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        canvas.create_line(0, i * 4, width, i * 4,
                           fill=f"#{r:02x}{g:02x}{b:02x}", width=4)
    return canvas


def _hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


# ── 進度條 ──
class ProgressBar(ctk.CTkProgressBar):
    def __init__(self, parent, width=780, height=8, **kwargs):
        super().__init__(
            parent, width=width, height=height, corner_radius=4,
            progress_color=COLORS["primary"], fg_color=COLORS["border"],
            **kwargs,
        )
        self.set(0)

    def set_progress(self, value: float):
        self.set(max(0.0, min(1.0, value)))


# ── 向後相容 KawaiiButton shim (CTkButton 包裝) ──
class KawaiiButton(ctk.CTkButton):
    def __init__(self, parent, text="", command=None,
                 width=240, height=50, bg_color=None, fg_color=None,
                 hover_color=None, font=None, corner_radius=16,
                 shadow=True, **kwargs):
        _bg = bg_color or COLORS["primary"]
        _fg = fg_color or COLORS["text_light"]
        _hov = hover_color or COLORS["primary_hover"]
        super().__init__(
            parent, text=text, command=command,
            width=width, height=height,
            fg_color=_bg, hover_color=_hov, text_color=_fg,
            font=font or FONTS["button"], corner_radius=corner_radius,
        )

    def set_text(self, text: str):
        self.configure(text=text)

    def set_bg(self, color: str):
        self.configure(fg_color=color)

    def set_state(self, enabled: bool):
        self.configure(state="normal" if enabled else "disabled")

    def set_font(self, font):
        """設定按鈕字型"""
        self.configure(font=font)
