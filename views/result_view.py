"""
ResultView — 成績結果畫面 (Result View) — 可愛風 (Kawaii Style)
"""

import tkinter as tk
from views.widgets import (COLORS, FONTS, KawaiiButton, sound, count_up_animation)
from views.background_helper import create_background_canvas


class ResultView:
    def __init__(self, parent: tk.Widget):
        self._parent = parent
        self.frame = tk.Frame(parent, bg=COLORS["bg"])
        self._canvas = None
        self._bg_image = None  # 保持背景圖片參考

    def render(self, results: dict, weak_words: set,
               newly_unlocked: bool = False,
               on_back=None, on_export=None):
        self.frame.pack(fill=tk.BOTH, expand=True)

        # 背景（支援自訂背景）
        self._canvas, self._bg_image = create_background_canvas(
            self.frame, 900, 650, "#E8D5FF", "#FFF5FA"
        )
        self._canvas.pack(fill=tk.BOTH, expand=True)

        score = results["score"]
        total = results["total"]
        pct = int(results["percent"])

        if newly_unlocked:
            sound.play("unlock")
        elif pct >= 80:
            sound.play("complete")

        # ── Score Header ──
        score_color = COLORS["success"] if pct >= 80 else COLORS["accent_pink"]

        self._canvas.create_text(
            450, 70, text="📝 測驗結果", font=FONTS["heading"],
            fill=COLORS["text"],
        )

        # 數字動畫 Label
        score_label = tk.Label(
            self.frame, text="0", font=FONTS["score"],
            fg=score_color, bg=COLORS["gradient_top"],
        )
        self._canvas.create_window(430, 140, window=score_label)
        count_up_animation(score_label, pct, self.frame, duration_ms=1000)

        self._canvas.create_text(
            510, 150, text="%", font=FONTS["heading"],
            fill=score_color,
        )

        self._canvas.create_text(
            450, 200, text=f"答對 {score} / {total} 題",
            font=FONTS["subtitle"], fill=COLORS["text_muted"],
        )

        # ── Unlock Notification ──
        if newly_unlocked:
            self._canvas.create_text(
                450, 240, text="🎉 恭喜！已解鎖新背景！✨",
                font=FONTS["body_bold"], fill=COLORS["warning"],
            )

        # ── Wrong Answers List ──
        wrong = results.get("wrong_list", [])
        y_offset = 280

        if wrong:
            self._canvas.create_text(
                150, y_offset, text="❌ 答錯的單字：",
                font=FONTS["body_bold"], fill=COLORS["error"], anchor="w"
            )
            y_offset += 30

            for i, w in enumerate(wrong[:4]): # 最多顯示 4 筆避免超出畫面
                txt = f" {w['japanese']} ({w['reading']}) — {w['chinese']}  |  你的答案: {w['user_answer']}"
                self._canvas.create_text(
                    170, y_offset, text=txt,
                    font=FONTS["small"], fill=COLORS["text"], anchor="w"
                )
                y_offset += 25
            if len(wrong) > 4:
                self._canvas.create_text(
                    170, y_offset, text=f"...等 {len(wrong)} 個",
                    font=FONTS["small"], fill=COLORS["text_muted"], anchor="w"
                )
                y_offset += 25

        y_offset += 10

        # ── Weak Words ──
        if weak_words:
            self._canvas.create_text(
                150, y_offset, text=f"⚠️ 弱點單字 ({len(weak_words)} 個):",
                font=FONTS["body_bold"], fill=COLORS["accent_pink"], anchor="w"
            )
            y_offset += 30
            
            weak_text = "、".join(sorted(weak_words))
            self._canvas.create_text(
                170, y_offset, text=weak_text,
                font=FONTS["japanese_sm"], fill=COLORS["text_muted"],
                width=600, anchor="w",
            )

        # ── Buttons ──
        btn_f = tk.Frame(self.frame, bg=COLORS["gradient_bot"])
        self._canvas.create_window(450, 580, window=btn_f)

        KawaiiButton(
            btn_f, text="🏠 返回主選單",
            width=200, height=48, corner_radius=14,
            bg_color=COLORS["accent_purple"], font=FONTS["button"],
            command=on_back,
        ).pack(side=tk.LEFT, padx=10)

        if wrong and on_export:
            KawaiiButton(
                btn_f, text="📄 匯出錯題",
                width=200, height=48, corner_radius=14,
                bg_color=COLORS["accent_mint"], fg_color=COLORS["text"],
                font=FONTS["button"], command=on_export,
            ).pack(side=tk.LEFT, padx=10)

    def destroy(self):
        self.frame.destroy()
