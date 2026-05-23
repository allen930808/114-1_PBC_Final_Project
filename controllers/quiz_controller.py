"""
QuizController — 測驗流程控制器 (Quiz Flow Controller)

管理測驗的開始、答題、結束流程，銜接 QuizSession (Model) 與 QuizView (View)。
"""

from models.quiz import QuizSession
from views.quiz_view import QuizView


class QuizController:
    """測驗流程控制器的類別 (Class)。"""

    def __init__(self, root, session: QuizSession, parent_frame,
                 on_quiz_end=None, on_back=None):
        """
        Parameters:
            root         — tk.Tk 根視窗（用於 after 延遲）
            session      — 已初始化的 QuizSession
            parent_frame — 放置 QuizView 的容器
            on_quiz_end  — 測驗結束 Callback: (results: dict) -> None
            on_back      — 返回主選單 Callback
        """
        self._root = root
        self._session = session
        self._on_quiz_end = on_quiz_end
        self._on_back = on_back

        # 建立 View
        self._view = QuizView(parent_frame)
        self._view.render(
            on_answer=self.on_answer_selected,
            on_back=self._handle_back,
        )

        # 顯示第一題
        self._show_current_question()

    def _show_current_question(self):
        """顯示目前題目。"""
        question = self._session.get_current_question()
        if question is None:
            return
        current, total = self._session.get_progress()
        self._view.show_question(
            question, current, total, self._session.mode,
        )

    def on_answer_selected(self, choice: int):
        """
        使用者選擇答案時觸發。

        1. 提交答案至 Model
        2. 顯示回饋 (正確/錯誤)
        3. 延遲後進入下一題或結束
        """
        question = self._session._questions[self._session._current]
        correct_index = question["correct_index"]

        is_correct = self._session.submit_answer(choice)
        self._view.show_feedback(is_correct, correct_index, choice)

        # 延遲 800ms 後進入下一題
        delay = 600 if is_correct else 1200
        self._root.after(delay, self._next_or_end)

    def _next_or_end(self):
        """進入下一題或結束測驗。"""
        if self._session.is_finished():
            results = self._session.get_results()
            if self._on_quiz_end:
                self._on_quiz_end(results)
        else:
            self._show_current_question()

    def _handle_back(self):
        """處理返回主選單。"""
        self._view.destroy()
        if self._on_back:
            self._on_back()

    def destroy(self):
        """銷毀測驗畫面。"""
        self._view.destroy()
