"""
UserProgress — 使用者進度模組 (User Progress Module)

負責追蹤成績、錯題紀錄 (Wrong Answer Tracking)、
弱點單字標記 (Weak Word Marking) 與解鎖判定 (Unlock Check)。
"""

from datetime import datetime


class UserProgress:
    """
    追蹤使用者學習進度的類別 (Class)。

    Attributes:
        _scores       — dict: {unit: list of result dicts}
        _weak_words   — set: 被標記為弱點的日文單字集合
        _wrong_counts — dict: {japanese_word: cumulative_error_count}
        _unlocked     — set: 已解鎖的課別集合
    """

    def __init__(self, weak_threshold: int = 2,
                 unlock_percent: float = 80.0):
        self._scores: dict[int, list] = {}
        self._weak_words: set[str] = set()
        self._wrong_counts: dict[str, int] = {}
        self._unlocked: set[int] = set()
        self._weak_threshold = weak_threshold
        self._unlock_percent = unlock_percent

    # ------------------------------------------------------------------
    # 成績紀錄 (Score Recording)
    # ------------------------------------------------------------------

    def record_result(self, results: dict):
        """
        記錄一次測驗結果。

        Parameters:
            results — QuizSession.get_results() 回傳的 dict

        此方法會同時更新弱點單字標記。
        """
        unit = results["unit"]
        if unit not in self._scores:
            self._scores[unit] = []

        self._scores[unit].append({
            "score": results["score"],
            "total": results["total"],
            "percent": results["percent"],
            "mode": results["mode"],
            "timestamp": datetime.now().isoformat(),
        })

        # 更新錯題計數 → 判定弱點單字
        for wrong in results["wrong_list"]:
            word = wrong["japanese"]
            self._wrong_counts[word] = self._wrong_counts.get(word, 0) + 1
            if self._wrong_counts[word] >= self._weak_threshold:
                self._weak_words.add(word)

    # ------------------------------------------------------------------
    # 弱點單字 (Weak Words)
    # ------------------------------------------------------------------

    def get_weak_words(self) -> set:
        """取得弱點單字集合 (Set)。"""
        return self._weak_words.copy()

    def load_weak_words_from_counts(self, counts: dict):
        """
        從資料庫載入的錯題統計中重建弱點標記。

        Parameters:
            counts — {japanese_word: error_count}
        """
        self._wrong_counts = dict(counts)
        self._weak_words = {
            word for word, cnt in counts.items()
            if cnt >= self._weak_threshold
        }

    # ------------------------------------------------------------------
    # 解鎖判定 (Unlock Check)
    # ------------------------------------------------------------------

    def check_unlock(self, unit: int) -> bool:
        """
        檢查該課別是否達到解鎖門檻。

        條件：該課最佳正確率 ≥ unlock_percent (預設 80%)。

        Returns:
            bool — True 表示已達標可解鎖
        """
        if unit in self._unlocked:
            return True

        records = self._scores.get(unit, [])
        if not records:
            return False

        best_percent = max(r["percent"] for r in records)
        return best_percent >= self._unlock_percent

    def set_unlocked(self, units: set):
        """從資料庫載入已解鎖的課別集合 (Set)。"""
        self._unlocked = set(units)

    def get_unlocked(self) -> set:
        """取得已解鎖的課別集合 (Set)。"""
        return self._unlocked.copy()

    def add_unlock(self, unit: int):
        """新增一個已解鎖的課別。"""
        self._unlocked.add(unit)

    # ------------------------------------------------------------------
    # 歷史查詢 (History Query)
    # ------------------------------------------------------------------

    def get_history(self, unit: int = None) -> list:
        """取得測驗歷史。可選填 unit 篩選特定課別。"""
        if unit is not None:
            return self._scores.get(unit, [])
        all_records = []
        for records in self._scores.values():
            all_records.extend(records)
        return sorted(all_records, key=lambda r: r["timestamp"], reverse=True)

    def get_best_percent(self, unit: int) -> float:
        """取得某課的最佳正確率。無紀錄時回傳 0.0。"""
        records = self._scores.get(unit, [])
        if not records:
            return 0.0
        return max(r["percent"] for r in records)
