"""
AppController — 主控制器 (Main Application Controller)

負責初始化所有元件、管理頁面切換 (Page Navigation)、
以及協調 Model / View / Controller 之間的互動。
"""

import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog

from models.database import DatabaseManager
from models.vocabulary import VocabularyBank
from models.quiz import QuizSession
from models.user_progress import UserProgress

from views.main_menu_view import MainMenuView
from views.result_view import ResultView
from views.unlock_view import UnlockView
from views.widgets import COLORS

from controllers.quiz_controller import QuizController
from controllers.progress_controller import ProgressController


class AppController:
    """
    應用程式主控制器的類別 (Class)。

    管理 tkinter 根視窗、所有 Model 實例 (Instance)、
    以及頁面之間的切換邏輯。
    """

    def __init__(self):
        # 取得專案根目錄
        self._base_dir = os.path.dirname(os.path.abspath(__file__))
        self._base_dir = os.path.dirname(self._base_dir)  # 上一層

        # 載入設定檔 (Config)
        self._config = self._load_config()

        # tkinter 根視窗
        self._root = tk.Tk()
        self._root.title(self._config.get("app_name", "Wani-Doko!"))
        self._root.geometry(
            f"{self._config.get('window_width', 900)}x"
            f"{self._config.get('window_height', 650)}"
        )

        # ✨ 設定 App Icon
        icon_path = os.path.join(self._base_dir, "assets", "icon_128.png")
        if os.path.exists(icon_path):
            try:
                from PIL import Image, ImageTk
                icon_img = Image.open(icon_path)
                icon_photo = ImageTk.PhotoImage(icon_img)
                self._root.iconphoto(True, icon_photo)
                # 保持引用避免被垃圾回收
                self._icon_ref = icon_photo
            except Exception as e:
                print(f"Icon 載入失敗：{e}")

        self._root.configure(bg=COLORS["bg"])
        self._root.resizable(False, False)

        # 主容器 (Main Container)
        self._container = tk.Frame(self._root, bg=COLORS["bg"])
        self._container.pack(fill=tk.BOTH, expand=True)

        # Model 實例
        db_path = os.path.join(self._base_dir, "wanidoko.db")
        self._db = DatabaseManager(db_path)
        self._vocab_bank = VocabularyBank()
        self._progress = UserProgress(
            weak_threshold=self._config.get("weak_word_threshold", 2),
            unlock_percent=self._config.get("unlock_score_percent", 80),
        )

        # Controller 實例
        self._progress_ctrl = ProgressController(self._progress, self._db)

        # 目前畫面的參考
        self._current_view = None

    # ------------------------------------------------------------------
    # 啟動 (Start)
    # ------------------------------------------------------------------

    def start(self):
        """啟動應用程式。"""
        # 1. 連接資料庫
        self._db.connect()

        # 2. 載入單字
        data_dir = os.path.join(self._base_dir, "data")
        try:
            self._vocab_bank.load_all_from_directory(
                data_dir,
                encoding=self._config.get("csv_encoding", "utf-8"),
            )
        except FileNotFoundError as e:
            messagebox.showwarning("資料載入警告", str(e))

        # 3. 從資料庫載入進度
        self._progress_ctrl.load_from_db()

        # 4. 顯示主選單
        self.show_main_menu()

        # 5. 進入主迴圈 (Main Loop)
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._root.mainloop()

    def _on_close(self):
        """關閉應用程式時的清理工作。"""
        self._db.close()
        self._root.destroy()

    # ------------------------------------------------------------------
    # 頁面切換 (Page Navigation)
    # ------------------------------------------------------------------

    def _clear_container(self):
        """清除目前的畫面。"""
        if self._current_view and hasattr(self._current_view, "destroy"):
            self._current_view.destroy()
        self._current_view = None

    def show_main_menu(self):
        """顯示主選單頁面。"""
        self._clear_container()
        view = MainMenuView(self._container)
        view.render(
            unit_ids=self._vocab_bank.get_unit_ids(),
            on_start_quiz=self.start_quiz,
            on_view_progress=self.show_progress,
            on_view_unlocks=self.show_unlocks,
        )
        self._current_view = view

    def start_quiz(self, unit: int, mode: str):
        """開始測驗。"""
        self._clear_container()

        vocabs = self._vocab_bank.get_unit(unit)
        if not vocabs:
            messagebox.showwarning(
                "無法開始", f"第 {unit} 課沒有單字資料。",
            )
            self.show_main_menu()
            return

        all_vocabs = self._vocab_bank.get_all()
        session = QuizSession()
        session.generate_questions(
            vocabs=vocabs, mode=mode, unit=unit,
            count=self._config.get("quiz_question_count", 10),
            all_vocabs=all_vocabs,
        )

        self._current_view = QuizController(
            root=self._root,
            session=session,
            parent_frame=self._container,
            on_quiz_end=lambda r: self._on_quiz_end(r),
            on_back=self.show_main_menu,
        )

    def _on_quiz_end(self, results: dict):
        """測驗結束時觸發。"""
        # 儲存結果
        newly_unlocked = self._progress_ctrl.save_result(results)

        # 顯示結果頁面
        self._clear_container()
        view = ResultView(self._container)
        view.render(
            results=results,
            weak_words=self._progress.get_weak_words(),
            newly_unlocked=newly_unlocked,
            on_back=self.show_main_menu,
            on_export=self._export_report,
        )
        self._current_view = view

    def show_progress(self):
        """顯示成績紀錄頁面（可愛風，支援滾動）。"""
        self._clear_container()

        frame = tk.Frame(self._container, bg=COLORS["bg"])
        frame.pack(fill=tk.BOTH, expand=True)

        from views.widgets import FONTS, KawaiiButton, create_gradient_canvas

        # 主背景 canvas（不滾動）
        bg_canvas = create_gradient_canvas(frame, 900, 650, "#F5EEFF", "#FFE4F0")
        bg_canvas.pack(fill=tk.BOTH, expand=True)

        # 標題（固定在頂部）
        bg_canvas.create_text(
            450, 40, text="📊 成績紀錄", font=FONTS["heading"],
            fill=COLORS["text"],
        )

        # 創建可滾動區域（80px 到 580px，高度 500px）
        scroll_container = tk.Frame(frame, bg=COLORS["bg"])
        bg_canvas.create_window(450, 330, window=scroll_container, width=880, height=500)

        # Canvas + Scrollbar
        scroll_canvas = tk.Canvas(scroll_container, bg=COLORS["bg"],
                                  highlightthickness=0, width=860, height=500)
        scrollbar = tk.Scrollbar(scroll_container, orient="vertical",
                                command=scroll_canvas.yview)
        scrollable_frame = tk.Frame(scroll_canvas, bg=COLORS["bg"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        )

        scroll_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scrollbar.set)

        scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 綁定滾輪事件到整個頁面
        def _on_mousewheel(event):
            scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        frame.bind_all("<MouseWheel>", _on_mousewheel)

        # === 內容區域（放在 scrollable_frame 中）===

        # 各課最佳成績
        history = self._db.load_quiz_history()
        if not history:
            tk.Label(
                scrollable_frame, text="尚無測驗紀錄",
                font=FONTS["body"], fg=COLORS["text_muted"],
                bg=COLORS["bg"]
            ).pack(pady=50)
        else:
            # 表格顯示（最多 10 筆）
            table_f = tk.Frame(scrollable_frame, bg=COLORS["bg_card"], bd=0,
                              highlightbackground=COLORS["border"], highlightthickness=2)
            table_f.pack(pady=20, padx=40)

            header_f = tk.Frame(table_f, bg=COLORS["accent_pink"])
            header_f.pack(fill=tk.X)
            for col, text in enumerate(["課別", "模式", "分數", "時間"]):
                tk.Label(
                    header_f, text=text, font=FONTS["body_bold"],
                    fg=COLORS["white"], bg=COLORS["accent_pink"],
                    width=15, anchor="center",
                ).grid(row=0, column=col, padx=5, pady=6)

            for i, rec in enumerate(history[:10]):  # 最多顯示 10 筆
                row_bg = COLORS["option_bg"] if i % 2 == 0 else COLORS["white"]
                row_f = tk.Frame(table_f, bg=row_bg)
                row_f.pack(fill=tk.X)

                mode_map = {
                    "zh_to_ja": "中翻日",
                    "ja_to_zh": "日翻中",
                    "hira_mode": "平假名",
                    "kata_mode": "片假名",
                }
                mode_text = mode_map.get(rec["mode"], rec["mode"])
                score_text = f"{rec['score']}/{rec['total']}"
                time_text = rec["timestamp"][:16].replace("T", " ")

                for col, text in enumerate(
                    [f"L{rec['unit']}", mode_text, score_text, time_text]
                ):
                    tk.Label(
                        row_f, text=text, font=FONTS["small"],
                        fg=COLORS["text"], bg=row_bg,
                        width=15, anchor="center",
                    ).grid(row=0, column=col, padx=5, pady=4)

        # 弱點單字（按課別分組顯示，錯過一次就算）
        weak_by_unit = self._db.load_weak_words_by_unit(threshold=1)

        if weak_by_unit:
            # 標題
            tk.Label(
                scrollable_frame, text="⚠️ 各課弱點單字",
                font=FONTS["body_bold"], fg=COLORS["accent_pink"],
                bg=COLORS["bg"]
            ).pack(pady=(30, 15))

            # 卡片容器（改為垂直排列，顯示所有課別）
            weak_container = tk.Frame(scrollable_frame, bg=COLORS["bg"])
            weak_container.pack(padx=40)

            # 顯示所有課別（每行 4 個卡片）
            for i, (unit, words) in enumerate(sorted(weak_by_unit.items())):
                unit_card = tk.Frame(weak_container, bg=COLORS["bg_card"],
                                    highlightbackground=COLORS["border"],
                                    highlightthickness=1, padx=8, pady=6,
                                    width=200, height=120)
                unit_card.grid(row=i // 4, column=i % 4, padx=6, pady=8, sticky="n")

                # 課別標題
                tk.Label(
                    unit_card, text=f"L{unit}",
                    font=FONTS["body_bold"], fg=COLORS["accent_purple"],
                    bg=COLORS["bg_card"]
                ).pack()

                # 單字列表（最多 6 個）
                words_text = "、".join(words[:6])
                tk.Label(
                    unit_card, text=words_text,
                    font=FONTS["japanese_sm"], fg=COLORS["text"],
                    bg=COLORS["bg_card"], wraplength=180,
                    justify=tk.LEFT
                ).pack()

                # 如果超過 6 個，顯示可點擊的「查看全部」
                if len(words) > 6:
                    def show_all_weak_words(u=unit, w=words):
                        all_words = "、".join(w)
                        messagebox.showinfo(
                            f"L{u} 弱點單字 ({len(w)} 個)",
                            all_words,
                            parent=frame
                        )

                    view_all_label = tk.Label(
                        unit_card, text=f"...查看全部 {len(words)} 個 →",
                        font=FONTS["small"], fg=COLORS["accent_pink"],
                        bg=COLORS["bg_card"], cursor="hand2"
                    )
                    view_all_label.pack()
                    view_all_label.bind("<Button-1>", lambda e, f=show_all_weak_words: f())

        # 底部留白
        tk.Frame(scrollable_frame, bg=COLORS["bg"], height=20).pack()

        # 返回按鈕（固定在底部）
        btn_f = tk.Frame(frame, bg=COLORS["gradient_bot"])
        bg_canvas.create_window(450, 600, window=btn_f)
        
        KawaiiButton(
            btn_f, text="🏠 返回主選單",
            width=200, height=48, corner_radius=14,
            bg_color=COLORS["accent_purple"],
            font=FONTS["button"], command=self.show_main_menu,
        ).pack()

        self._current_view = type("View", (), {"destroy": frame.destroy})()

    def show_unlocks(self):
        """顯示解鎖背景頁面。"""
        self._clear_container()

        trivia_path = os.path.join(self._base_dir, "data", "trivia.json")
        view = UnlockView(self._container)
        view.render(
            unit_ids=self._vocab_bank.get_unit_ids(),
            unlocked=self._progress.get_unlocked(),
            trivia_path=trivia_path,
            on_back=self.show_main_menu,
        )
        self._current_view = view

    # ------------------------------------------------------------------
    # 工具方法 (Utility)
    # ------------------------------------------------------------------

    def _load_config(self) -> dict:
        """載入 config.json 設定檔。"""
        config_path = os.path.join(self._base_dir, "config.json")
        default_config = {
            "app_name": "Wani-Doko! ワニどこ!",
            "window_width": 900,
            "window_height": 650,
            "quiz_question_count": 10,
            "weak_word_threshold": 2,
            "unlock_score_percent": 80,
            "csv_encoding": "utf-8",
        }
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                default_config.update(loaded)
        except FileNotFoundError:
            print("[資訊] config.json 不存在，使用預設設定。")
        except json.JSONDecodeError as e:
            print(f"[警告] config.json 格式錯誤：{e}，使用預設設定。")
        return default_config

    def _export_report(self):
        """匯出錯題報告 — 跳出檔案選擇對話框。"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV 檔案", "*.csv")],
            title="匯出錯題報告",
        )
        if filepath:
            try:
                actual_path = self._progress_ctrl.export_wrong_report(filepath)
                messagebox.showinfo(
                    "匯出成功", f"錯題報告已匯出至：\n{actual_path}",
                )
            except IOError as e:
                messagebox.showerror("匯出失敗", str(e))
