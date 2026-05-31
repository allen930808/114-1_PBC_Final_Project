"""
簡化版背景處理：完全移除圖片增強，測試是否解決白屏問題
"""
import os
import tkinter as tk
from PIL import Image, ImageTk
from models.config_manager import ConfigManager

# 全域快取
_background_cache = {}


def create_background_canvas(parent, width=900, height=650,
                             default_top="#EEF2FF", default_bot="#E0E7FF"):
    """
    超簡化背景處理（測試用）
    """
    canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
    bg_image_ref = None

    try:
        config = ConfigManager()
        custom_bg = config.get_custom_background()

        if custom_bg:
            cache_key = f"{custom_bg}_{width}x{height}"

            if cache_key in _background_cache:
                bg_image_ref = _background_cache[cache_key]
                canvas.create_image(0, 0, anchor=tk.NW, image=bg_image_ref)
                return canvas, bg_image_ref

            bg_path = f"assets/backgrounds/{custom_bg}.png"

            if os.path.exists(bg_path):
                # 最簡化處理：只 resize，不做任何增強
                img = Image.open(bg_path)
                img = img.resize((width, height), Image.BILINEAR)  # 快速且品質好

                # 直接轉換
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                bg_image_ref = ImageTk.PhotoImage(img)
                canvas.create_image(0, 0, anchor=tk.NW, image=bg_image_ref)

                _background_cache[cache_key] = bg_image_ref
                return canvas, bg_image_ref
    except Exception as e:
        print(f"背景載入失敗（使用漸層）：{e}")

    # 使用漸層背景
    _draw_gradient_background(canvas, width, height, default_top, default_bot)
    return canvas, bg_image_ref


def _draw_gradient_background(canvas, width, height, top_color, bot_color):
    """簡化版漸層（更少步驟）"""
    steps = 20  # 減少步驟，加快渲染
    for i in range(steps):
        y1 = int(height * i / steps)
        y2 = int(height * (i + 1) / steps)

        ratio = i / steps
        r = int(int(top_color[1:3], 16) * (1 - ratio) + int(bot_color[1:3], 16) * ratio)
        g = int(int(top_color[3:5], 16) * (1 - ratio) + int(bot_color[3:5], 16) * ratio)
        b = int(int(top_color[5:7], 16) * (1 - ratio) + int(bot_color[5:7], 16) * ratio)

        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_rectangle(0, y1, width, y2, fill=color, outline="")
