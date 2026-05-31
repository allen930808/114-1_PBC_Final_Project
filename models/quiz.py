"""
QuizSession — 測驗邏輯模組 (Quiz Logic Module)

負責出題、選項生成、答案驗證、計分與結果統計。
"""

import random
from datetime import datetime


class QuizSession:
    """
    管理一次測驗流程的類別 (Class)。

    Attributes:
        _questions — 題目列表 (List of dict)
        _current   — 目前題號 (Index, 0-based)
        _mode      — 測驗模式：'zh_to_ja' 或 'ja_to_zh'
        _unit      — 課別編號
        _results   — 每題作答紀錄
    """

    def __init__(self):
        self._questions: list[dict] = []
        self._current: int = 0
        self._mode: str = ""
        self._unit: int = 0
        self._start_time: datetime | None = None
        self._results: list[dict] = []

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def unit(self) -> int:
        return self._unit

    def generate_questions(self, vocabs: list, mode: str, unit: int,
                           count: int = 10, all_vocabs: list = None):
        """
        產生測驗題目。

        Parameters:
            vocabs     — 本課單字列表 (用於出題)
            mode       — 'zh_to_ja'（中翻日）或 'ja_to_zh'（日翻中）
            unit       — 課別編號
            count      — 出題數量，預設 10
            all_vocabs — 所有課別的單字（用於生成干擾選項）

        每題格式 (dict):
            {
                'vocab': Vocabulary,        # 正確答案的單字物件
                'question_text': str,       # 題目文字
                'options': list[str],       # 四個選項
                'correct_index': int,       # 正確答案的索引 (Index, 0-based)
            }
        """
        self._mode = mode
        self._unit = unit
        self._start_time = datetime.now()
        self._current = 0
        self._results = []
        self._questions = []

        if all_vocabs is None:
            all_vocabs = vocabs

        # 假名模式：過濾出正確假名類型，干擾選項也只取同類型
        if mode in ("hira_mode", "kata_mode"):
            kana_type = "平假名" if mode == "hira_mode" else "片假名"
            vocabs = [v for v in vocabs if v.chinese == kana_type]
            all_vocabs = vocabs

        # 限制出題數量不超過可用單字數
        count = min(count, len(vocabs))
        selected = random.sample(vocabs, count)

        for vocab in selected:
            question = self._build_question(vocab, mode, all_vocabs)
            self._questions.append(question)

    def _build_question(self, vocab, mode: str, pool: list) -> dict:
        """為單一單字建立題目與四個選項。"""

        if mode == "zh_to_ja":
            question_text = vocab.chinese
            # 中翻日：顯示「日文（平假名）」格式
            correct_answer = f"{vocab.japanese}（{vocab.reading}）"
            distractors_pool = [
                f"{v.japanese}（{v.reading}）" for v in pool
                if v.japanese != vocab.japanese
            ]
        elif mode in ("hira_mode", "kata_mode"):
            question_text = vocab.reading        # 羅馬拼音（如 "ka"）
            correct_answer = vocab.japanese      # 假名字符（如 "か"）
            distractors_pool = [
                v.japanese for v in pool
                if v.japanese != vocab.japanese
            ]
        else:  # ja_to_zh
            question_text = vocab.japanese
            correct_answer = vocab.chinese
            distractors_pool = [
                v.chinese for v in pool
                if v.chinese != vocab.chinese
            ]

        # 去重後取 3 個干擾選項
        distractors_pool = list(set(distractors_pool))
        num_distractors = min(3, len(distractors_pool))
        distractors = random.sample(distractors_pool, num_distractors)

        # 如果干擾選項不足 3 個，補上佔位符
        while len(distractors) < 3:
            distractors.append("—")

        options = distractors + [correct_answer]
        random.shuffle(options)
        correct_index = options.index(correct_answer)

        return {
            "vocab": vocab,
            "question_text": question_text,
            "options": options,
            "correct_index": correct_index,
        }

    def get_current_question(self) -> dict | None:
        """取得目前題目。若測驗已結束則回傳 None。"""
        if self.is_finished():
            return None
        return self._questions[self._current]

    def submit_answer(self, choice: int) -> bool:
        """
        提交答案。

        Parameters:
            choice — 使用者選擇的選項索引 (0-based)

        Returns:
            bool — 是否正確
        """
        question = self._questions[self._current]
        is_correct = (choice == question["correct_index"])

        self._results.append({
            "vocab": question["vocab"],
            "question_text": question["question_text"],
            "user_choice": choice,
            "user_answer": question["options"][choice],
            "correct_answer": question["options"][question["correct_index"]],
            "is_correct": is_correct,
        })

        self._current += 1
        return is_correct

    def is_finished(self) -> bool:
        """測驗是否已結束。"""
        return self._current >= len(self._questions)

    def get_progress(self) -> tuple:
        """
        取得進度。

        Returns:
            tuple — (current_number, total)，current_number 為 1-based
        """
        return (self._current + 1, len(self._questions))

    def get_results(self) -> dict:
        """
        取得測驗結果摘要。

        Returns:
            dict — {
                'unit': int,
                'mode': str,
                'score': int,
                'total': int,
                'percent': float,
                'duration_seconds': float,
                'wrong_list': list[dict],
                'start_time': datetime,
            }
        """
        score = sum(1 for r in self._results if r["is_correct"])
        total = len(self._results)
        percent = (score / total * 100) if total > 0 else 0

        duration = 0.0
        if self._start_time:
            duration = (datetime.now() - self._start_time).total_seconds()

        wrong_list = []
        for r in self._results:
            if not r["is_correct"]:
                wrong_list.append({
                    "japanese": r["vocab"].japanese,
                    "chinese": r["vocab"].chinese,
                    "reading": r["vocab"].reading,
                    "user_answer": r["user_answer"],
                    "correct_answer": r["correct_answer"],
                })

        return {
            "unit": self._unit,
            "mode": self._mode,
            "score": score,
            "total": total,
            "percent": percent,
            "duration_seconds": duration,
            "wrong_list": wrong_list,
            "start_time": self._start_time,
        }
