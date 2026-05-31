"""
QuizView — 測驗畫面 (Quiz View) — 可愛風 (Kawaii Style)
"""

import tkinter as tk
from views.widgets import (COLORS, FONTS, KawaiiButton, ProgressBar, sound)
from views.background_helper import create_background_canvas


class QuizView:
    """測驗畫面的類別 (Class)。"""

    def __init__(self, parent: tk.Widget):
        self._parent = parent
        self.frame = tk.Frame(parent, bg=COLORS["bg"])
        self._option_buttons: list[KawaiiButton] = []
        self._on_answer = None
        self._on_back = None
        self._canvas = None
        self._bg_image = None  # 保持背景圖片參考

    def render(self, on_answer=None, on_back=None):
        self._on_answer = on_answer
        self._on_back = on_back
        self.frame.pack(fill=tk.BOTH, expand=True)

        # 背景（支援自訂背景）
        self._canvas, self._bg_image = create_background_canvas(
            self.frame, 900, 650, "#FFF5FA", "#F0E6FF"
        )
        self._canvas.pack(fill=tk.BOTH, expand=True)

        # ── Top bar ──
        back_f = tk.Frame(self.frame, bg=COLORS["gradient_top"])
        self._canvas.create_window(70, 30, window=back_f)
        KawaiiButton(
            back_f, text="← 返回", width=90, height=34, corner_radius=10,
            bg_color=COLORS["bg_card"], fg_color=COLORS["text_muted"],
            font=FONTS["small"], shadow=False, command=self._on_back,
        ).pack()

        self._progress_label = tk.Label(
            self.frame, text="1 / 10", font=FONTS["body_bold"],
            fg=COLORS["text_muted"], bg=COLORS["gradient_top"],
        )
        self._canvas.create_window(830, 30, window=self._progress_label)

        # ── Progress Bar ──
        bar_f = tk.Frame(self.frame, bg=COLORS["gradient_top"])
        self._canvas.create_window(450, 60, window=bar_f)
        self._progress_bar = ProgressBar(
            bar_f, width=800, height=10,
        )
        self._progress_bar.pack()

        # ── Mode label ──
        self._mode_label = tk.Label(
            self.frame, text="", font=FONTS["small"],
            fg=COLORS["text_muted"], bg=COLORS["gradient_top"],
        )
        self._canvas.create_window(450, 90, window=self._mode_label)

        # ── Question Card (白底圓角卡片) ──
        card = tk.Frame(self.frame, bg=COLORS["white"],
                        highlightbackground=COLORS["border"],
                        highlightthickness=2)
        self._canvas.create_window(450, 190, window=card)

        # 卡片內容
        self._question_label = tk.Label(
            card, text="", font=FONTS["japanese_lg"],
            fg=COLORS["text"], bg=COLORS["white"],
            wraplength=500, padx=60, pady=30,
        )
        self._question_label.pack()

        # ── 裝飾 ──
        self._canvas.create_text(100, 190, text="🌸",
                                  font=("Apple Color Emoji", 20))
        self._canvas.create_text(800, 190, text="🌸",
                                  font=("Apple Color Emoji", 20))

        # ── Options (2×2 grid) ──
        opts_f = tk.Frame(self.frame, bg=COLORS["gradient_bot"])
        self._canvas.create_window(450, 400, window=opts_f)

        for i in range(4):
            btn = KawaiiButton(
                opts_f, text="", width=340, height=52, corner_radius=14,
                bg_color=COLORS["option_bg"],
                fg_color=COLORS["text"],
                hover_color=COLORS["option_hover"],
                font=FONTS["japanese_md"], shadow=True,
                command=lambda idx=i: self._handle_answer(idx),
            )
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=8)
            self._option_buttons.append(btn)

        # ── Feedback ──
        self._feedback_label = tk.Label(
            self.frame, text="", font=FONTS["heading"],
            bg=COLORS["gradient_bot"],
        )
        self._canvas.create_window(450, 510, window=self._feedback_label)

    def show_question(self, question: dict, current: int, total: int,
                      mode: str):
        self._progress_label.config(text=f"{current} / {total}")
        prog = max(0, (current - 1)) / total
        self._progress_bar.set_progress(prog)

        mode_map = {
            "zh_to_ja": "📝 中文 → 日文",
            "ja_to_zh": "📝 日文 → 中文",
            "hira_mode": "あ  平假名練習",
            "kata_mode": "ア  片假名練習",
        }
        mode_text = mode_map.get(mode, "📝 測驗模式")
        self._mode_label.config(text=mode_text)

        # 假名模式：問題是羅馬拼音，選項是假名
        if mode in ("hira_mode", "kata_mode"):
            q_font = FONTS["body_bold"]
            opt_font = FONTS["japanese_md"]
        elif mode == "zh_to_ja":
            q_font = FONTS["heading"]
            opt_font = FONTS["japanese_md"]
        else:  # ja_to_zh
            q_font = FONTS["japanese_lg"]
            opt_font = FONTS["body_bold"]

        self._question_label.config(text=question["question_text"], font=q_font)
        for i, btn in enumerate(self._option_buttons):
            btn.set_text(question["options"][i])
            btn.set_bg(COLORS["option_bg"])
            btn.set_state(True)
            btn.set_font(opt_font)

        self._feedback_label.config(text="")

    def show_feedback(self, is_correct: bool, correct_index: int,
                      user_choice: int):
        for btn in self._option_buttons:
            btn.set_state(False)

        if is_correct:
            sound.play("correct")
            self._option_buttons[user_choice].set_bg(COLORS["success"])
            self._feedback_label.config(text="✨ 正確！すごい！✨",
                                         fg=COLORS["success"])
        else:
            sound.play("wrong")
            self._option_buttons[user_choice].set_bg(COLORS["error"])
            self._option_buttons[correct_index].set_bg(COLORS["success"])
            self._feedback_label.config(text="💦 再加油！",
                                         fg=COLORS["accent_pink"])

    def _handle_answer(self, index: int):
        if self._on_answer:
            self._on_answer(index)

    def destroy(self):
        self.frame.destroy()
