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
from models.config_manager import ConfigManager


class UnlockView:
    def __init__(self, parent: tk.Widget):
        self._parent = parent
        self.frame = tk.Frame(parent, bg=COLORS["bg"])
        self._images = {} # 防止被 GC 垃圾回收
        self._mousewheel_bound = False  # 追蹤滾輪綁定狀態
        # 背景名稱對應（若 trivia.json 中沒有 background 欄位時使用）
        self._bg_names = {
            0: "bg1", 1: "bg2", 2: "bg3", 3: "bg4",
            4: "bg5", 5: "bg6", 6: "bg7", 7: "bg8",
            8: "bg9", 9: "bg10", 10: "bg11", 11: "bg12", 12: "bg13"
        }

    def render(self, unit_ids: list, unlocked: set,
               trivia_path: str, on_back=None):
        self.frame.pack(fill=tk.BOTH, expand=True)

        # 主背景 canvas（不滾動）
        bg_canvas = create_gradient_canvas(self.frame, 900, 650,
                                          "#FFF0F5", "#E8D5FF")
        bg_canvas.pack(fill=tk.BOTH, expand=True)

        # Header
        bg_canvas.create_text(
            450, 40, text="🔓 解鎖背景與日本小知識",
            font=FONTS["heading"], fill=COLORS["text"],
        )
        bg_canvas.create_text(
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

        # 創建可滾動區域（100px 到 540px，高度 440px）
        scroll_container = tk.Frame(self.frame, bg=COLORS["bg"])
        bg_canvas.create_window(450, 310, window=scroll_container, width=880, height=440)

        # Canvas + Scrollbar
        canvas = tk.Canvas(scroll_container, bg=COLORS["bg"],
                          highlightthickness=0, width=860, height=440)
        scrollbar = tk.Scrollbar(scroll_container, orient="vertical",
                                command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["bg"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 綁定滾輪事件到整個頁面（不只是 canvas）
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # 綁定到整個 frame，讓滑鼠在頁面任何位置都能滾動
        self.frame.bind_all("<MouseWheel>", _on_mousewheel)

        # 儲存綁定 ID 以便之後清理
        self._mousewheel_bound = True

        # Card grid（放在 scrollable_frame 中）
        grid = tk.Frame(scrollable_frame, bg=COLORS["bg"])
        grid.pack(padx=20, pady=10)

        # 顯示 3 個卡片一行
        for i, uid in enumerate(unit_ids):
            is_unlocked = uid in unlocked
            self._create_card(grid, uid, is_unlocked, trivia,
                              row=i // 3, col=i % 3)

        # Back button（固定在底部）
        btn_f = tk.Frame(self.frame, bg=COLORS["gradient_bot"])
        bg_canvas.create_window(450, 600, window=btn_f)
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

        # 按鈕區域
        btn_window = tk.Frame(top, bg=COLORS["white"])
        canvas.create_window(450, 610, window=btn_window)

        # 設為背景按鈕
        KawaiiButton(
            btn_window, text="🎨 設為背景", width=140, height=36, corner_radius=8,
            bg_color=COLORS["accent_mint"], fg_color=COLORS["text"],
            font=FONTS["body_bold"], shadow=False,
            command=lambda: self._set_as_background(bg_name, top)
        ).pack(side=tk.LEFT, padx=5)

        # 關閉按鈕
        KawaiiButton(
            btn_window, text="關閉", width=120, height=36, corner_radius=8,
            bg_color=COLORS["white"], fg_color=COLORS["text"],
            font=FONTS["body_bold"], shadow=False, command=top.destroy
        ).pack(side=tk.LEFT, padx=5)

    def _set_as_background(self, bg_name, window):
        """設定為主選單背景"""
        try:
            config = ConfigManager()
            config.set_custom_background(bg_name)
            sound.play("unlock")
            messagebox.showinfo("成功", f"已將背景設為 {bg_name.upper()}！\n重新進入主選單即可看到效果。")
            window.destroy()
        except Exception as e:
            print(f"設定背景失敗：{e}")
            messagebox.showerror("錯誤", "設定背景失敗，請稍後再試。")

    def destroy(self):
        # 清理滾輪綁定
        if self._mousewheel_bound:
            self.frame.unbind_all("<MouseWheel>")
            self._mousewheel_bound = False
        self.frame.destroy()
