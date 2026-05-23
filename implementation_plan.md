# Wani-Doko! (ワニどこ!) — Architecture & Implementation Plan (Updated)

## Goal

Build a professional MVC-based Python application for Japanese vocabulary drilling, targeting NTU Japanese 1 (ワニさん) curriculum.
**Latest Update**: The UI has been completely overhauled into a "Kawaii" (cute) pastel style, featuring animations, system sound effects, and AI-generated unlockable background images.

---

## UI / UX Enhancements (Kawaii Overhaul)

1. **Color Theme**: Pastel color palette (Lavender blush, coral pink, mint green, warm yellow).
2. **Typography**: MacOS rounded fonts (`Hiragino Maru Gothic ProN`).
3. **Animations**: Number count-up animations for scores, smooth hover transitions on buttons.
4. **Sound Effects**: Integrated macOS system sounds via `afplay` (`Tink.aiff`, `Glass.aiff`, `Hero.aiff`, etc.) for clicks, correct/wrong answers, and unlocking achievements.
5. **Unlockable Gallery**: Beautiful AI-generated watercolor-style backgrounds (Fuji, Kyoto, Osaka, Tokyo, Nara) displayed in a full-screen popup when a user achieves ≥ 80% on a lesson.

---

## Vocabulary Data (Extracted from PDF)

| Unit | 名稱 | 單字數 | 背景主題 |
|------|------|--------|----------|
| L7   | 第七課（家族、送禮、節日） | 46 | Tokyo |
| L8   | 第八課（交通、季節） | 36 | Osaka |
| L9   | 第九課（食物、身體） | 36 | Kyoto |
| L10  | 第十課（居住、家電） | 30 | Nara |
| L11  | 第十一課（學校、動作） | 40 | Fuji |
| L12  | 第十二課（服裝、文化） | 63 | Tokyo |
| **Total** | | **251** | |

---

## Advanced Technique Coverage (6/6)

| # | Technique | Where |
|---|-----------|-------|
| 1 | **File I/O** | CSV 載入、config.json、錯題 CSV 匯出 |
| 2 | **Advanced Data Structures** | `dict`, `set`, `tuple`, `datetime` |
| 3 | **Exception Handling** | 檔案/DB/CSV/圖片載入 錯誤處理 |
| 4 | **Custom Classes** | 12+ 自定義類別 (含 Custom Widget 繼承) |
| 5 | **GUI** | `tkinter` 全介面 + `Pillow` 影像處理 |
| 6 | **Database** | `sqlite3` — quiz_results, wrong_answers, unlocks |

---

## File Structure (Final)

```
Final Project/
├── main.py
├── config.json
├── extract_vocab.py           # 單字提取工具
├── models/
│   ├── database.py            # DatabaseManager
│   ├── vocabulary.py          # Vocabulary, VocabularyBank
│   ├── quiz.py                # QuizSession
│   └── user_progress.py       # UserProgress
├── views/
│   ├── widgets.py             # Kawaii Theme, Custom Buttons, SoundManager
│   ├── main_menu_view.py      # MainMenuView (Gradient + Emoji)
│   ├── quiz_view.py           # QuizView (Animations & Sound)
│   ├── result_view.py         # ResultView (Score Count-up Animation)
│   └── unlock_view.py         # UnlockView (Image Gallery)
├── controllers/
│   ├── app_controller.py      # AppController
│   ├── quiz_controller.py     # QuizController
│   └── progress_controller.py # ProgressController
├── data/
│   ├── vocab_unit07.csv ~ vocab_unit12.csv (6 files)
│   └── trivia.json            # 日本小知識 (7 entries)
├── assets/
│   └── backgrounds/
│       ├── fuji.png, kyoto.png, nara.png, osaka.png, tokyo.png
└── wanidoko.db                # SQLite (runtime generated)
```

---

## How to Run

1. Ensure dependencies are installed: `pip3 install pillow`
2. Run the app:
```bash
cd "/Users/allen/Desktop/Final Project"
python3 main.py
```
