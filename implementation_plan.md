# Wani-Doko! (ワニどこ!) — 實作計畫 v1.2

## 🎯 專案目標

打造專業的 MVC 架構 Python 應用程式，針對台大日文一（ワニさん）課程設計的互動式單字訓練系統。

**最新版本**: v1.2 (2026-05-31)
- ✅ 13 張背景對應 13 個關卡（每關專屬背景）
- ✅ 中翻日只對漢字詞加平假名標註
- ✅ 測驗與結果畫面支援自訂背景
- ✅ 加入 App Icon（鱷魚 emoji）
- ✅ 優化背景處理（統一函數）

---

## 📚 詞彙資料（從 PDF 提取）

| Unit | 名稱 | 單字數 | 背景主題 | 小知識主題 |
|------|------|--------|----------|------------|
| L0 | 平假名・片假名 | 138 | 背景1 | 日本的文字系統 |
| L1 | 問候・自我介紹 | 45 | 背景2 | 日本的問候文化 |
| L2 | 購物・日圓 | 38 | 背景3 | 日本的便利商店文化 |
| L3 | 日常動詞 | 35 | 背景4 | 日本的一日三餐 |
| L4 | 喜好・伴手禮 | 28 | 背景5 | 日本的伴手禮文化 |
| L5 | 交通工具 | 32 | 背景6 | 東京的交通網絡 |
| L6 | 存在・位置 | 25 | 背景7 | 奈良的鹿與神社 |
| L7 | 家族・送禮・節日 | 46 | 背景8 | 日本家庭文化 |
| L8 | 交通・季節 | 36 | 背景9 | 新幹線 |
| L9 | 食物・身體 | 36 | 背景10 | 日本料理的「五味五色」|
| L10 | 居住・家電 | 30 | 背景11 | 日本的居住空間 |
| L11 | 學校・動作 | 40 | 背景12 | 從富士山看日本精神 |
| L12 | 服裝・文化 | 63 | 背景13 | 日本的盆踊り |
| **Total** | | **592** | | |

---

## 🎨 UI/UX 設計（Kawaii 風格）

### 色彩主題
- **漸層背景**: 淡紫色系 (#EEF2FF → #E0E7FF)
- **強調色**: 珊瑚粉 (#EC4899)、薄荷綠 (#14B8A6)、淺紫 (#8B5CF6)
- **文字色**: 深藍紫 (#1E1B4B)

### 字型
- **主要字型**: Hiragino Maru Gothic ProN（macOS 圓體）
- **日文大字**: 36pt bold
- **日文中字**: 22pt
- **按鈕文字**: 14pt bold

### 動畫效果
1. **分數計數動畫**: 從 0 累加至實際分數
2. **按鈕 hover 效果**: 平滑色彩過渡
3. **進度條**: 隨答題進度推進

### 音效（macOS）
- **點擊**: Tink.aiff
- **答對**: Glass.aiff
- **答錯**: Basso.aiff
- **解鎖**: Hero.aiff

### 解鎖畫廊
- **觸發條件**: 單元測驗正確率 ≥ 80%
- **獎勵**: 日本城市背景圖 + 文化小知識
- **全螢幕展示**: 900×650 高解析度圖片

---

## 🎮 核心功能

### 1. 多模式測驗
- **中翻日** (zh_to_ja): 顯示中文，選擇日文（含平假名標註）
- **日翻中** (ja_to_zh): 顯示日文，選擇中文
- **平假名** (hira_mode): 顯示羅馬拼音，選擇平假名（L0 專用）
- **片假名** (kata_mode): 顯示羅馬拼音，選擇片假名（L0 專用）

### 2. 智慧出題
- 從同單元隨機抽選 10 題
- 干擾選項從相同類別抽取（避免過於明顯）
- 假名模式自動過濾對應類型

### 3. 即時回饋
- ✅ 答對：綠色高亮 + Glass 音效
- ❌ 答錯：紅色高亮錯誤答案 + 綠色顯示正確答案 + Basso 音效

### 4. 成就系統
- 達成 80% 以上正確率解鎖背景
- 累積解鎖 13 個日本城市背景
- 每個背景搭配獨特的文化小知識

### 5. 自訂背景 ⭐ NEW in v1.1
- 解鎖後可設為主選單背景
- 自動增加亮度並加上半透明遮罩
- 可隨時重置為預設漸層背景

### 6. 進度追蹤
- SQLite 資料庫記錄所有測驗結果
- 錯題記錄供後續複習
- 每位使用者獨立資料庫（不共享）

---

## 🏗️ 系統架構（MVC）

### Model 層
```
models/
├── database.py           # 資料庫管理（SQLite3）
├── vocabulary.py         # 單字資料結構
├── quiz.py              # 測驗邏輯與出題演算法
├── user_progress.py     # 使用者進度追蹤
└── config_manager.py    # 配置檔案管理 ⭐ NEW
```

### View 層
```
views/
├── widgets.py              # UI 元件、主題、音效管理
├── main_menu_view.py       # 主選單（支援自訂背景 ⭐）
├── quiz_view.py            # 測驗畫面（支援自訂背景 ⭐ v1.2）
├── result_view.py          # 結果畫面（支援自訂背景 ⭐ v1.2）
├── unlock_view.py          # 解鎖畫廊（支援設為背景 ⭐）
└── background_helper.py    # 背景處理共用函數 ⭐ NEW v1.2
```

### Controller 層
```
controllers/
├── app_controller.py         # 應用程式主控制器
├── quiz_controller.py        # 測驗流程控制
└── progress_controller.py    # 進度管理
```

### 資料層
```
data/
├── vocab_unit00.csv ~ vocab_unit12.csv  # 13 個單元 CSV
└── trivia.json                           # 13 個文化小知識
```

### 資源層
```
assets/
├── backgrounds/
│   ├── bg1.png ~ bg13.png  # 13 張背景（每關專屬） ⭐ v1.2
├── icon_16.png             # App Icon 16×16 ⭐ NEW v1.2
├── icon_32.png             # App Icon 32×32 ⭐ NEW v1.2
├── icon_64.png             # App Icon 64×64 ⭐ NEW v1.2
├── icon_128.png            # App Icon 128×128 ⭐ NEW v1.2
└── icon_256.png            # App Icon 256×256 ⭐ NEW v1.2
```

---

## 🔧 進階技術應用（6/6 符合課程要求）

| # | 技術 | 應用位置 | 說明 |
|---|------|----------|------|
| 1 | **File I/O** | CSV 載入、JSON 配置、圖片資源 | 13 個 CSV 檔案、config.json、trivia.json |
| 2 | **Advanced Data Structures** | dict、set、tuple、datetime | 按鈕映射、解鎖集合、字型設定、時間戳記 |
| 3 | **Exception Handling** | 檔案/DB/圖片載入 | try-except 包裹所有 I/O 操作 |
| 4 | **Custom Classes** | 15+ 自定義類別 | MVC 架構 + UI 元件繼承 |
| 5 | **GUI** | tkinter + CustomTkinter + Pillow | 完整圖形介面應用程式 |
| 6 | **Database** | SQLite3 | 3 張關聯資料表 |

---

## 💾 資料庫設計

### quiz_results（測驗結果）
```sql
CREATE TABLE quiz_results (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    unit      INTEGER NOT NULL,
    mode      TEXT    NOT NULL,
    score     INTEGER NOT NULL,
    total     INTEGER NOT NULL,
    timestamp TEXT    NOT NULL
);
```

### wrong_answers（錯題記錄）
```sql
CREATE TABLE wrong_answers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id     INTEGER NOT NULL,
    japanese    TEXT    NOT NULL,
    chinese     TEXT    NOT NULL,
    user_answer TEXT    NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES quiz_results(id)
);
```

### unlocks（解鎖記錄）
```sql
CREATE TABLE unlocks (
    unit        INTEGER PRIMARY KEY,
    unlocked_at TEXT    NOT NULL
);
```

---

## 📁 完整檔案結構

```
Final Project/
├── main.py                         # 程式進入點
├── config.json                     # 系統配置（含自訂背景設定）
├── requirements.txt                # Python 相依套件 ⭐
├── extract_vocab.py                # 單字提取工具
│
├── models/                         # 資料模型層
│   ├── __init__.py
│   ├── database.py                # DatabaseManager
│   ├── vocabulary.py              # Vocabulary, VocabularyBank
│   ├── quiz.py                    # QuizSession（含平假名標註 ⭐）
│   ├── user_progress.py           # UserProgress
│   └── config_manager.py          # ConfigManager ⭐ NEW
│
├── views/                          # 使用者介面層
│   ├── __init__.py
│   ├── widgets.py                 # UI 元件、主題、音效
│   ├── main_menu_view.py          # 主選單（自訂背景支援 ⭐）
│   ├── quiz_view.py               # 測驗畫面
│   ├── result_view.py             # 結果畫面
│   └── unlock_view.py             # 解鎖畫廊（設為背景 ⭐）
│
├── controllers/                    # 控制器層
│   ├── __init__.py
│   ├── app_controller.py          # AppController
│   ├── quiz_controller.py         # QuizController
│   └── progress_controller.py     # ProgressController
│
├── data/                           # 資料檔案
│   ├── vocab_unit00.csv           # L0: 平假名・片假名 (138 詞)
│   ├── vocab_unit01.csv           # L1: 問候 (45 詞)
│   ├── vocab_unit02.csv           # L2: 購物 (38 詞)
│   ├── vocab_unit03.csv           # L3: 動詞 (35 詞)
│   ├── vocab_unit04.csv           # L4: 喜好 (28 詞)
│   ├── vocab_unit05.csv           # L5: 交通 (32 詞)
│   ├── vocab_unit06.csv           # L6: 位置 (25 詞)
│   ├── vocab_unit07.csv           # L7: 家族 (46 詞)
│   ├── vocab_unit08.csv           # L8: 交通 (36 詞)
│   ├── vocab_unit09.csv           # L9: 食物 (36 詞)
│   ├── vocab_unit10.csv           # L10: 居住 (30 詞)
│   ├── vocab_unit11.csv           # L11: 學校 (40 詞)
│   ├── vocab_unit12.csv           # L12: 文化 (63 詞)
│   ├── trivia.json                # 13 個日本文化小知識
│   └── facts.json                 # (備用資料)
│
├── assets/                         # 資源檔案
│   └── backgrounds/               # 背景圖片（AI 生成水彩風格）
│       ├── tokyo.png              # 東京都市景觀
│       ├── osaka.png              # 大阪街景
│       ├── kyoto.png              # 京都古都風情
│       ├── nara.png               # 奈良鹿與神社
│       └── fuji.png               # 富士山聖山
│
├── wanidoko.db                     # SQLite 資料庫（執行時生成，不入 Git）
│
├── README.md                       # 完整專案說明 ⭐
├── WRITTEN_REPORT.md              # 書面報告 ⭐
├── CHANGELOG.md                   # 版本變更記錄 ⭐
├── BACKGROUND_GUIDE.md            # 背景功能說明 ⭐
│
├── Wani-Doko.spec                 # PyInstaller 配置 ⭐
├── build.bat                      # Windows 一鍵打包 ⭐
├── BUILD_GUIDE.md                 # 詳細打包教學 ⭐
├── QUICK_BUILD.md                 # 快速打包指南 ⭐
│
├── test_background.py             # 背景功能測試 ⭐
└── implementation_plan.md         # 本文件
```

---

## 🚀 執行方式

### 開發環境執行

```bash
# 1. 安裝相依套件
pip install -r requirements.txt

# 或手動安裝
pip install customtkinter Pillow

# 2. 執行程式
cd "/Users/allen/Desktop/Final Project"
python3 main.py
```

### 打包成 Windows 執行檔

```bash
# 方法 1: 一鍵打包（Windows）
build.bat

# 方法 2: 手動打包
pip install pyinstaller
pyinstaller Wani-Doko.spec
```

執行檔位置: `dist/Wani-Doko/Wani-Doko.exe`

---

## ✨ v1.2 新功能 (2026-05-31)

### 1. 13 張背景對應 13 個關卡
- **功能**：每個關卡（L0-L12）都有專屬的解鎖背景
- **實作**：
  - 背景命名統一為 bg1.png ~ bg13.png
  - 更新 trivia.json 背景對應
  - 更新 unlock_view.py 備用對應表

### 2. 修正中翻日平假名標註邏輯
- **問題**：片假名詞彙也被加上平假名標註（不必要）
- **解決**：只對包含漢字的詞彙加上平假名標註
- **範例**：
  - ✅ 「学生（がくせい）」（漢字 + 平假名）
  - ✅ 「アメリカ」（片假名，不加標註）
  - ✅ 「はい」（平假名，不加標註）

### 3. 測驗與結果畫面支援自訂背景
- **功能**：測驗畫面和結果畫面也能使用自訂背景
- **實作**：
  - 創建 background_helper.py 統一背景處理
  - 更新 quiz_view.py、result_view.py、main_menu_view.py
  - 消除重複 code，符合 DRY 原則

### 4. App Icon（鱷魚 emoji 🐊）
- **功能**：程式視窗顯示鱷魚 icon 而非預設 Python icon
- **實作**：
  - 生成多種尺寸 icon（16/32/64/128/256px）
  - 在 app_controller.py 中設定 iconphoto
  - macOS 使用 Apple Color Emoji 字體

---

## ✨ v1.1 新功能

### 1. 修正資料庫共享問題

### 1. 修正資料庫共享問題
- **問題**: 所有使用者共用同一個資料庫檔案
- **解決**: 將 `wanidoko.db` 從 Git 移除，每人獨立生成
- **影響**: 每位使用者都有自己的測驗紀錄

### 2. 中翻日顯示平假名標註
- **功能**: 中翻日模式選項顯示「漢字（平假名）」
- **範例**: `祖母（そぼ）`、`祖父（そふ）`
- **實作**: 修改 `models/quiz.py` 的 `_build_question()` 方法

### 3. 自訂背景功能
- **功能**: 解鎖後可設為主選單背景
- **操作**: 解鎖畫廊 → 點擊「設為背景」
- **重置**: 主選單「預設背景」按鈕
- **技術**: PIL 圖片混合 + ConfigManager 配置管理

### 4. 跨平台支援
- **文件**: 完整的 README.md 與 BUILD_GUIDE.md
- **打包**: PyInstaller 配置與一鍵打包腳本
- **測試**: Windows/macOS/Linux 安裝說明

---

## 🎯 專案亮點

1. **完整的 MVC 架構**: 清晰的程式碼組織與模組化設計
2. **遊戲化學習**: 成就解鎖、背景收集提升學習動機
3. **精美的 UI 設計**: Kawaii 風格、動畫效果、音效回饋
4. **實用價值**: 針對實際課程內容，可供修課學生使用
5. **技術深度**: 涵蓋 6 項進階技術，超過課程要求
6. **跨平台**: 支援 Windows/macOS/Linux，含打包工具
7. **文化學習**: 13 個日本文化小知識，寓教於樂
8. **可擴充性**: 良好的架構設計，易於新增功能

---

## 📊 專案統計

- **程式碼行數**: ~2,500 行（不含空行與註解）
- **自定義類別**: 15+ 個
- **資料檔案**: 13 個 CSV + 1 個 JSON
- **圖片資源**: 5 張高解析度背景
- **資料庫表格**: 3 張
- **詞彙總數**: 592 個
- **支援單元**: 13 個（L0-L12）
- **測驗模式**: 4 種

---

## 🔮 未來擴充方向

- [ ] 間隔重複演算法（Spaced Repetition）
- [ ] 聽力測驗模式（整合 TTS）
- [ ] 錯題本專項複習
- [ ] 多人競賽模式
- [ ] 匯出學習報告（PDF）
- [ ] Web 版本（Flask + JavaScript）
- [ ] 行動 App（Kivy）
- [ ] 更多背景主題與文化小知識
- [ ] 深色模式
- [ ] 音效開關設定

---

## 📞 專案資訊

- **課程**: 台大商管程式設計（114-2）
- **專案名稱**: Wani-Doko!（ワニどこ！）
- **版本**: v1.1
- **最後更新**: 2026-05-31
- **開發團隊**: `[組員姓名]`
- **指導老師**: `[老師姓名]`

---

## 📄 相關文件

- `README.md` - 完整專案說明與安裝指南
- `WRITTEN_REPORT.md` - 期末專案書面報告
- `CHANGELOG.md` - 版本變更記錄
- `BUILD_GUIDE.md` - Windows 打包詳細教學
- `QUICK_BUILD.md` - 快速打包參考
- `BACKGROUND_GUIDE.md` - 自訂背景功能說明

---

**祝學習愉快！頑張ってください！✨**
