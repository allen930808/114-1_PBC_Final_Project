"""
UnlockView — 背景解鎖畫面 (Unlock View) — 可愛風 (Kawaii Style)
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
from views.widgets import (COLORS, FONTS, KawaiiButton,
                           create_gradient_canvas, sound)


class UnlockView:
    def __init__(self, parent: tk.Widget):
        self._parent = parent
        self.frame = tk.Frame(parent, bg=COLORS["bg"])
        self._images = {} # 防止被 GC 垃圾回收
        # 背景名稱對應（若 trivia.json 中沒有 background 欄位時使用）
        self._bg_names = {
            0: "tokyo", 1: "osaka", 2: "kyoto", 3: "tokyo",
            4: "osaka", 5: "tokyo", 6: "nara", 7: "tokyo",
            8: "osaka", 9: "kyoto", 10: "nara", 11: "fuji", 12: "tokyo"
        }

    def render(self, unit_ids: list, unlocked: set,
               trivia_path: str, on_back=None):
        self.frame.pack(fill=tk.BOTH, expand=True)

        canvas = create_gradient_canvas(self.frame, 900, 650,
                                       "#FFF0F5", "#E8D5FF")

        # Header
        canvas.create_text(
            450, 40, text="🔓 解鎖背景與日本小知識",
            font=FONTS["heading"], fill=COLORS["text"],
        )
        canvas.create_text(
            450, 70, text="完成各課測驗（正確率 ≥ 80%）即可解鎖！",
            font=FONTS["small"], fill=COLORS["text_muted"],
        )

        trivia = {}
        if os.path.exists(trivia_path):
            try:
                with open(trivia_path, "r", encoding="utf-8") as f:
                    trivia = json.load(f)
            except Exception:
                pass

        # Card grid
        grid = tk.Frame(self.frame, bg=COLORS["bg_card"])
        canvas.create_window(450, 310, window=grid)

        # 顯示 3 個卡片一行
        for i, uid in enumerate(unit_ids):
            is_unlocked = uid in unlocked
            self._create_card(grid, uid, is_unlocked, trivia,
                              row=i // 3, col=i % 3)

        # Back button
        btn_f = tk.Frame(self.frame, bg=COLORS["gradient_bot"])
        canvas.create_window(450, 580, window=btn_f)
        KawaiiButton(
            btn_f, text="🏠 返回主選單",
            width=220, height=50, corner_radius=16,
            bg_color=COLORS["accent_pink"], font=FONTS["button"],
            command=on_back,
        ).pack()

    def _create_card(self, parent, unit_id: int, unlocked: bool,
                     trivia: dict, row: int, col: int):
        
        card_bg = COLORS["white"] if unlocked else "#F5F5F5"
        card = tk.Frame(parent, bg=card_bg, width=250, height=180,
                        highlightbackground=COLORS["border"], highlightthickness=2)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.pack_propagate(False) # 固定大小

        label = f"L{unit_id}"
        
        # 標題列
        header_f = tk.Frame(card, bg=card_bg)
        header_f.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        icon = "🌸" if unlocked else "🔒"
        fg_color = COLORS["text"] if unlocked else COLORS["text_muted"]
        
        tk.Label(
            header_f, text=f"{icon} {label}",
            font=FONTS["body_bold"], fg=fg_color, bg=card_bg,
        ).pack(side=tk.LEFT)

        if unlocked:
            # 優先從 trivia.json 讀取背景名稱，否則使用預設對應
            unit_trivia = trivia.get(str(unit_id), {})
            bg_name = unit_trivia.get("background", self._bg_names.get(unit_id, "fuji"))

            # 建立預覽圖和按鈕
            btn_f = tk.Frame(card, bg=card_bg)
            btn_f.pack(expand=True)

            KawaiiButton(
                btn_f, text="觀看小知識與背景",
                width=160, height=36, corner_radius=8,
                bg_color=COLORS["accent_mint"], fg_color=COLORS["text"],
                font=FONTS["small"], shadow=False,
                command=lambda: self._show_fullscreen_bg(unit_id, trivia, bg_name)
            ).pack(pady=10)
        else:
            tk.Label(
                card, text="尚未解鎖\n(需 ≥ 80%)",
                font=FONTS["small"], fg=COLORS["text_muted"], bg=card_bg,
            ).pack(expand=True)

    def _show_fullscreen_bg(self, unit_id, trivia, bg_name):
        """顯示全螢幕背景與小知識。"""
        sound.play("pop")
        top = tk.Toplevel(self._parent)
        top.title("解鎖畫廊")
        top.geometry("900x650")
        top.resizable(False, False)
        
        canvas = tk.Canvas(top, width=900, height=650, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # 載入背景圖
        bg_path = f"assets/backgrounds/{bg_name}.png"
        try:
            img = Image.open(bg_path)
            img = img.resize((900, 650), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self._images[f"bg_{bg_name}"] = photo # 保持參考
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        except Exception as e:
            print(f"背景載入失敗: {e}")
            canvas.create_rectangle(0, 0, 900, 650, fill=COLORS["bg"])

        # 顯示小知識對話框 (半透明白色背景)
        t_data = trivia.get(str(unit_id), {})
        title = t_data.get("title", "")
        desc = t_data.get("description", "")
        
        if title:
            # 繪製半透明矩形
            canvas.create_rectangle(150, 450, 750, 600, fill="#FFFFFF", stipple="gray50", outline="")
            canvas.create_text(450, 480, text=f"✨ {title} ✨", font=FONTS["heading"], fill=COLORS["accent_pink"])
            canvas.create_text(450, 530, text=desc, font=FONTS["small"], fill=COLORS["text"], width=560)

        # 返回按鈕
        btn_window = tk.Frame(top, bg=COLORS["white"])
        canvas.create_window(450, 610, window=btn_window)
        KawaiiButton(
            btn_window, text="關閉", width=120, height=36, corner_radius=8,
            bg_color=COLORS["white"], fg_color=COLORS["text"],
            font=FONTS["body_bold"], shadow=False, command=top.destroy
        ).pack()

    def destroy(self):
        self.frame.destroy()
