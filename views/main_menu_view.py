"""
MainMenuView — 主選單畫面 (Main Menu View) — 可愛風 (Kawaii Style)

漸層背景、圓角按鈕、裝飾性 emoji、柔和色調。
"""

import tkinter as tk
from views.widgets import (COLORS, FONTS, KawaiiButton,
                           create_gradient_canvas, sound)


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

    def render(self, unit_ids: list, on_start_quiz=None,
               on_view_progress=None, on_view_unlocks=None):
        self._on_start_quiz = on_start_quiz
        self._on_view_progress = on_view_progress
        self._on_view_unlocks = on_view_unlocks
        self.frame.pack(fill=tk.BOTH, expand=True)

        # ── 漸層背景 Canvas ──
        canvas = create_gradient_canvas(self.frame, 900, 650)

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
            width=180, height=44, corner_radius=12,
            bg_color=COLORS["accent_purple"],
            fg_color=COLORS["white"],
            font=FONTS["body"], shadow=True,
            command=self._on_view_progress,
        ).pack(side=tk.LEFT, padx=10)

        KawaiiButton(
            nav_frame, text="🗾 解鎖背景",
            width=180, height=44, corner_radius=12,
            bg_color=COLORS["accent_mint"],
            fg_color=COLORS["text"],
            font=FONTS["body"], shadow=True,
            command=self._on_view_unlocks,
        ).pack(side=tk.LEFT, padx=10)

        # ── Footer ──
        canvas.create_text(
            450, 630, text="NTU PBC Final Project  ·  ワニさん日本語教室",
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

    def destroy(self):
        self.frame.destroy()
