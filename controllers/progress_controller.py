"""
ProgressController — 成績 / 解鎖邏輯控制器 (Progress Controller)

負責將 UserProgress (Model) 與 DatabaseManager 同步，
以及匯出錯題報告 (Export Wrong Report)。
"""

import csv
import os
from datetime import datetime
from models.database import DatabaseManager
from models.user_progress import UserProgress


class ProgressController:
    """成績與解鎖邏輯的控制器類別 (Class)。"""

    def __init__(self, progress: UserProgress, db: DatabaseManager):
        self._progress = progress
        self._db = db

    def load_from_db(self):
        """從資料庫載入歷史資料至 UserProgress。"""
        # 載入解鎖狀態
        unlocks = self._db.load_unlocks()
        self._progress.set_unlocked(unlocks)

        # 載入錯題統計 → 重建弱點標記
        wrong_counts = self._db.load_all_wrong_counts()
        self._progress.load_weak_words_from_counts(wrong_counts)

    def save_result(self, results: dict) -> bool:
        """
        儲存測驗結果至資料庫，並更新 UserProgress。

        Parameters:
            results — QuizSession.get_results() 的回傳值

        Returns:
            bool — 本次是否新解鎖了背景
        """
        # 記錄至 UserProgress (in-memory)
        self._progress.record_result(results)

        # 寫入資料庫 (persistent)
        self._db.save_quiz_result(
            unit=results["unit"],
            mode=results["mode"],
            score=results["score"],
            total=results["total"],
            wrong_list=results["wrong_list"],
            correct_list=results.get("correct_list", []),
        )

        # 檢查解鎖
        unit = results["unit"]
        already_unlocked = self._progress.get_unlocked()
        newly_unlocked = False

        if unit not in already_unlocked and self._progress.check_unlock(unit):
            self._progress.add_unlock(unit)
            self._db.save_unlock(unit)
            newly_unlocked = True

        return newly_unlocked

    def export_wrong_report(self, filepath: str = None) -> str:
        """
        匯出錯題報告為 CSV 檔案 (File I/O)。

        Parameters:
            filepath — 匯出路徑，預設為 wrong_report_<timestamp>.csv

        Returns:
            str — 實際匯出的檔案路徑
        """
        if filepath is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"wrong_report_{ts}.csv"

        wrong_answers = self._db.load_wrong_answers()

        try:
            with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["quiz_id", "japanese", "chinese",
                                 "user_answer"])
                for w in wrong_answers:
                    writer.writerow([
                        w["quiz_id"], w["japanese"],
                        w["chinese"], w["user_answer"],
                    ])
        except IOError as e:
            print(f"[錯誤] 匯出失敗：{e}")
            raise

        return filepath
