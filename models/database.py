"""
DatabaseManager — SQLite 資料庫管理模組 (Database Module)

負責所有資料庫 (Database) 的連線 (Connection)、建表 (Table Creation)、
以及 CRUD 操作。
"""

import sqlite3
import os
from datetime import datetime


class DatabaseManager:
    """管理 SQLite 資料庫連線與操作的類別 (Class)。"""

    def __init__(self, db_path: str = "wanidoko.db"):
        self._db_path = db_path
        self._conn: sqlite3.Connection | None = None

    # ------------------------------------------------------------------
    # 連線管理 (Connection Management)
    # ------------------------------------------------------------------

    def connect(self):
        """建立資料庫連線 (Connection)。若資料庫損壞則備份並重建。"""
        try:
            self._conn = sqlite3.connect(self._db_path)
            self._conn.row_factory = sqlite3.Row
            self.init_tables()
        except sqlite3.DatabaseError:
            backup_path = self._db_path + ".backup"
            if os.path.exists(self._db_path):
                os.rename(self._db_path, backup_path)
            self._conn = sqlite3.connect(self._db_path)
            self._conn.row_factory = sqlite3.Row
            self.init_tables()
            print(f"[警告] 資料庫損壞，已備份至 {backup_path} 並重建。")

    def close(self):
        """關閉資料庫連線。"""
        if self._conn:
            self._conn.close()
            self._conn = None

    def init_tables(self):
        """建立資料表 (Table)，若不存在則自動建立。"""
        cursor = self._conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS quiz_results (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                unit      INTEGER NOT NULL,
                mode      TEXT    NOT NULL,
                score     INTEGER NOT NULL,
                total     INTEGER NOT NULL,
                timestamp TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS wrong_answers (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id     INTEGER NOT NULL,
                japanese    TEXT    NOT NULL,
                chinese     TEXT    NOT NULL,
                user_answer TEXT    NOT NULL,
                FOREIGN KEY (quiz_id) REFERENCES quiz_results(id)
            );

            CREATE TABLE IF NOT EXISTS unlocks (
                unit        INTEGER PRIMARY KEY,
                unlocked_at TEXT    NOT NULL
            );
        """)
        self._conn.commit()

    # ------------------------------------------------------------------
    # 測驗結果 (Quiz Results)
    # ------------------------------------------------------------------

    def save_quiz_result(self, unit: int, mode: str, score: int,
                         total: int, wrong_list: list) -> int:
        """
        儲存一次測驗的結果與錯題。

        Parameters:
            unit       — 課別 (Unit number)
            mode       — 模式 ('zh_to_ja' 或 'ja_to_zh')
            score      — 答對題數
            total      — 總題數
            wrong_list — 錯題列表，每筆為 dict 含 japanese / chinese / user_answer

        Returns:
            quiz_id — 新建紀錄的 ID
        """
        cursor = self._conn.cursor()
        timestamp = datetime.now().isoformat()

        cursor.execute(
            "INSERT INTO quiz_results (unit, mode, score, total, timestamp) "
            "VALUES (?, ?, ?, ?, ?)",
            (unit, mode, score, total, timestamp),
        )
        quiz_id = cursor.lastrowid

        for wrong in wrong_list:
            cursor.execute(
                "INSERT INTO wrong_answers "
                "(quiz_id, japanese, chinese, user_answer) "
                "VALUES (?, ?, ?, ?)",
                (quiz_id, wrong["japanese"], wrong["chinese"],
                 wrong["user_answer"]),
            )

        self._conn.commit()
        return quiz_id

    def load_quiz_history(self, unit: int = None) -> list:
        """載入測驗歷史紀錄。可選填 unit 篩選特定課別。"""
        cursor = self._conn.cursor()
        if unit is not None:
            cursor.execute(
                "SELECT * FROM quiz_results WHERE unit = ? "
                "ORDER BY timestamp DESC", (unit,),
            )
        else:
            cursor.execute(
                "SELECT * FROM quiz_results ORDER BY timestamp DESC"
            )
        return [dict(row) for row in cursor.fetchall()]

    def load_wrong_answers(self, quiz_id: int = None) -> list:
        """載入錯題紀錄。可選填 quiz_id 篩選特定測驗。"""
        cursor = self._conn.cursor()
        if quiz_id is not None:
            cursor.execute(
                "SELECT * FROM wrong_answers WHERE quiz_id = ?", (quiz_id,),
            )
        else:
            cursor.execute("SELECT * FROM wrong_answers")
        return [dict(row) for row in cursor.fetchall()]

    def load_all_wrong_counts(self) -> dict:
        """
        統計每個單字的累計錯誤次數。

        Returns:
            dict — {japanese_word: error_count}
        """
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT japanese, COUNT(*) as cnt "
            "FROM wrong_answers GROUP BY japanese"
        )
        return {row["japanese"]: row["cnt"] for row in cursor.fetchall()}

    # ------------------------------------------------------------------
    # 解鎖 (Unlocks)
    # ------------------------------------------------------------------

    def save_unlock(self, unit: int):
        """儲存解鎖紀錄。"""
        cursor = self._conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute(
            "INSERT OR IGNORE INTO unlocks (unit, unlocked_at) "
            "VALUES (?, ?)", (unit, timestamp),
        )
        self._conn.commit()

    def load_unlocks(self) -> set:
        """載入已解鎖的課別集合 (Set)。"""
        cursor = self._conn.cursor()
        cursor.execute("SELECT unit FROM unlocks")
        return {row["unit"] for row in cursor.fetchall()}

    def get_best_score(self, unit: int, mode: str) -> tuple:
        """
        取得某課某模式的最佳成績。

        Returns:
            tuple — (best_score, total)，無紀錄時回傳 (0, 0)
        """
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT score, total FROM quiz_results "
            "WHERE unit = ? AND mode = ? ORDER BY score DESC LIMIT 1",
            (unit, mode),
        )
        row = cursor.fetchone()
        if row:
            return (row["score"], row["total"])
        return (0, 0)
