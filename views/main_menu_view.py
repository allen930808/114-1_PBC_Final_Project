"""
MainMenuView — 主選單畫面 (Main Menu View) — 可愛風 (Kawaii Style)

漸層背景、圓角按鈕、裝飾性 emoji、柔和色調。
"""

import tkinter as tk
from PIL import Image, ImageTk
from views.widgets import (COLORS, FONTS, KawaiiButton,
                           create_gradient_canvas, sound)
from models.config_manager import ConfigManager


class MainMenuView:
    """主選單畫面的類別 (Class)。"""

    def __init__(self, parent: tk.Widget):
        self._parent = parent
        self.frame = tk.Frame(parent, bg=COLORS["bg"])
        self._selected_unit: int | None = None
        self._selected_mode: str = "zh_to_ja"
        self._on_start_quiz = None
        self._on_view_progress = None
        self._on_view_unlocks = None
        self._unit_buttons: dict = {}
        self._mode_buttons: dict = {}
        self._bg_image = None  # 保持背景圖片參考

    def render(self, unit_ids: list, on_start_quiz=None,
               on_view_progress=None, on_view_unlocks=None):
        self._on_start_quiz = on_start_quiz
        self._on_view_progress = on_view_progress
        self._on_view_unlocks = on_view_unlocks
        self.frame.pack(fill=tk.BOTH, expand=True)

        # ── 背景 Canvas ──
        # 檢查是否有自訂背景
        config = ConfigManager()
        custom_bg = config.get_custom_background()

        canvas = tk.Canvas(self.frame, width=900, height=650, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        if custom_bg:
            # 使用自訂背景圖片
            try:
                bg_path = f"assets/backgrounds/{custom_bg}.png"
                img = Image.open(bg_path)
                img = img.resize((900, 650), Image.Resampling.LANCZOS)

                # 增加亮度並加上半透明白色遮罩
                from PIL import ImageEnhance
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.5)  # 更亮一點

                # 創建半透明白色遮罩並混合
                white_overlay = Image.new('RGBA', (900, 650), (255, 255, 255, 100))
                img = img.convert('RGBA')
                img = Image.alpha_composite(img, white_overlay)

                self._bg_image = ImageTk.PhotoImage(img)
                canvas.create_image(0, 0, anchor=tk.NW, image=self._bg_image)

                print(f"✓ 已載入自訂背景：{custom_bg}")
            except Exception as e:
                print(f"✗ 自訂背景載入失敗：{e}")
                # 載入失敗時使用預設漸層
                self._draw_gradient_background(canvas)
        else:
            # 使用預設漸層背景
            self._draw_gradient_background(canvas)

        # ── Title ──
        canvas.create_text(
            450, 50, text="🐊", font=("Apple Color Emoji", 40),
        )
        canvas.create_text(
            450, 100, text="Wani-Doko!",
            font=FONTS["title"], fill=COLORS["accent_pink"],
        )
        canvas.create_text(
            450, 135, text="ワニどこ！",
            font=("Hiragino Maru Gothic ProN", 20),
            fill=COLORS["accent_purple"],
        )
        canvas.create_text(
            450, 165, text="✨ NTU Japanese 1 — Vocabulary Trainer ✨",
            font=FONTS["small"], fill=COLORS["text_muted"],
        )

        # ── 裝飾：櫻花花瓣 ──
        for x, y in [(80, 80), (820, 60), (750, 140), (130, 150)]:
            canvas.create_text(x, y, text="🌸",
                               font=("Apple Color Emoji", 16))

        # ── Unit Selection (課別選擇) ──
        canvas.create_text(
            450, 210, text="📖  選擇課別",
            font=FONTS["body_bold"], fill=COLORS["text"],
        )

        unit_frame = tk.Frame(self.frame, bg=COLORS["gradient_top"])
        canvas.create_window(450, 270, window=unit_frame)

        # 分成兩行顯示（避免超出視窗）
        units_per_row = 7
        for i, uid in enumerate(unit_ids):
            row = i // units_per_row
            col = i % units_per_row

            label = f"L{uid}"
            btn = KawaiiButton(
                unit_frame, text=label,
                width=85, height=40, corner_radius=12,
                bg_color=COLORS["bg_card"],
                fg_color=COLORS["text"],
                hover_color=COLORS["option_hover"],
                font=FONTS["body_bold"], shadow=False,
                command=lambda u=uid: self._select_unit(u),
            )
            btn.grid(row=row, column=col, padx=4, pady=4)
            self._unit_buttons[uid] = btn

        # ── Mode Selection (模式選擇) ──
        canvas.create_text(
            450, 345, text="🔄  選擇模式",
            font=FONTS["body_bold"], fill=COLORS["text"],
        )

        mode_frame = tk.Frame(self.frame, bg=COLORS["gradient_top"])
        canvas.create_window(450, 390, window=mode_frame)

        self._mode_buttons["zh_to_ja"] = KawaiiButton(
            mode_frame, text="中 → 日",
            width=160, height=44, corner_radius=14,
            bg_color=COLORS["accent_pink"],
            fg_color=COLORS["white"],
            font=FONTS["body_bold"], shadow=False,
            command=lambda: self._select_mode("zh_to_ja"),
        )
        self._mode_buttons["zh_to_ja"].pack(side=tk.LEFT, padx=6)

        self._mode_buttons["ja_to_zh"] = KawaiiButton(
            mode_frame, text="日 → 中",
            width=160, height=44, corner_radius=14,
            bg_color=COLORS["bg_card"],
            fg_color=COLORS["text"],
            hover_color=COLORS["option_hover"],
            font=FONTS["body_bold"], shadow=False,
            command=lambda: self._select_mode("ja_to_zh"),
        )
        self._mode_buttons["ja_to_zh"].pack(side=tk.LEFT, padx=6)

        # ── Start Button ──
        start_frame = tk.Frame(self.frame, bg=COLORS["gradient_bot"])
        canvas.create_window(450, 470, window=start_frame)

        self._start_btn = KawaiiButton(
            start_frame, text="🌟  選擇課別後開始",
            width=300, height=56, corner_radius=18,
            bg_color=COLORS["border"],
            fg_color=COLORS["text_muted"],
            font=FONTS["button"], shadow=True,
            command=self._on_start_click,
        )
        self._start_btn.pack()

        # ── Bottom Navigation ──
        nav_frame = tk.Frame(self.frame, bg=COLORS["gradient_bot"])
        canvas.create_window(450, 565, window=nav_frame)

        KawaiiButton(
            nav_frame, text="📊 成績紀錄",
            width=140, height=44, corner_radius=12,
            bg_color=COLORS["accent_purple"],
            fg_color=COLORS["white"],
            font=FONTS["body"], shadow=True,
            command=self._on_view_progress,
        ).pack(side=tk.LEFT, padx=6)

        KawaiiButton(
            nav_frame, text="🗾 解鎖背景",
            width=140, height=44, corner_radius=12,
            bg_color=COLORS["accent_mint"],
            fg_color=COLORS["text"],
            font=FONTS["body"], shadow=True,
            command=self._on_view_unlocks,
        ).pack(side=tk.LEFT, padx=6)

        # 顯示背景重置按鈕（如果有自訂背景）
        if custom_bg:
            KawaiiButton(
                nav_frame, text="🔄 預設背景",
                width=140, height=44, corner_radius=12,
                bg_color=COLORS["bg_card"],
                fg_color=COLORS["text_muted"],
                font=FONTS["body"], shadow=False,
                command=self._reset_background,
            ).pack(side=tk.LEFT, padx=6)

        # ── Footer ──
        footer_text = "NTU PBC Final Project  ·  ワニさん日本語教室"
        if custom_bg:
            footer_text += f"  ·  背景：{custom_bg.upper()}"

        canvas.create_text(
            450, 630, text=footer_text,
            font=("Hiragino Maru Gothic ProN", 9),
            fill=COLORS["text_muted"],
        )

    def _select_unit(self, unit_id: int):
        sound.play("pop")
        self._selected_unit = unit_id
        for uid, btn in self._unit_buttons.items():
            if uid == unit_id:
                btn.set_bg(COLORS["accent_mint"])
            else:
                btn.set_bg(COLORS["bg_card"])
        self._start_btn.set_bg(COLORS["accent_pink"])
        self._start_btn.configure(text_color=COLORS["white"])
        self._start_btn.set_text("🚀  開始測驗！")

        # Unit 0 (假名練習) 用不同的模式按鈕
        if unit_id == 0:
            self._mode_buttons["zh_to_ja"].configure(
                text="あ  平假名",
                text_color=COLORS["text"],
                command=lambda: self._select_mode("hira_mode"),
            )
            self._mode_buttons["ja_to_zh"].configure(
                text="ア  片假名",
                text_color=COLORS["text"],
                command=lambda: self._select_mode("kata_mode"),
            )
            self._select_mode("hira_mode")
        else:
            self._mode_buttons["zh_to_ja"].configure(
                text="中 → 日",
                text_color=COLORS["white"],
                command=lambda: self._select_mode("zh_to_ja"),
            )
            self._mode_buttons["ja_to_zh"].configure(
                text="日 → 中",
                text_color=COLORS["text"],
                command=lambda: self._select_mode("ja_to_zh"),
            )
            self._select_mode("zh_to_ja")

    def _select_mode(self, mode: str):
        sound.play("pop")
        self._selected_mode = mode
        for m, btn in self._mode_buttons.items():
            if m == mode:
                btn.set_bg(COLORS["accent_pink"])
                btn.configure(text_color=COLORS["white"])
            else:
                btn.set_bg(COLORS["bg_card"])
                btn.configure(text_color=COLORS["text"])

    def _on_start_click(self):
        if self._selected_unit is None:
            return
        sound.play("click")
        if self._on_start_quiz:
            self._on_start_quiz(self._selected_unit, self._selected_mode)

    def _reset_background(self):
        """重置為預設背景"""
        sound.play("pop")
        config = ConfigManager()
        config.clear_custom_background()

        # 顯示訊息要求重新進入主選單
        from tkinter import messagebox
        messagebox.showinfo(
            "成功",
            "已重置為預設背景！\n\n" +
            "請點擊「成績紀錄」或「解鎖背景」再返回，\n" +
            "或重新啟動程式即可看到預設背景。",
            parent=self.frame
        )

    def _draw_gradient_background(self, canvas):
        """繪製漸層背景"""
        # 簡化版漸層繪製
        top_color = "#EEF2FF"
        bot_color = "#E0E7FF"

        # 使用矩形模擬漸層（簡化版）
        steps = 50
        for i in range(steps):
            y1 = int(650 * i / steps)
            y2 = int(650 * (i + 1) / steps)

            # 計算中間色
            ratio = i / steps
            r = int(int(top_color[1:3], 16) * (1 - ratio) + int(bot_color[1:3], 16) * ratio)
            g = int(int(top_color[3:5], 16) * (1 - ratio) + int(bot_color[3:5], 16) * ratio)
            b = int(int(top_color[5:7], 16) * (1 - ratio) + int(bot_color[5:7], 16) * ratio)

            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_rectangle(0, y1, 900, y2, fill=color, outline="")

    def destroy(self):
        self.frame.destroy()
