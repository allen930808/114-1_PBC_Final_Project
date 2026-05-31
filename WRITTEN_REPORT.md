# 商管程式設計（114-2）期末專案書面報告

## Wani-Doko! (ワニどこ!) — NTU 日文一單字訓練系統

---

### 組別資訊

**組別編號**：`[待填寫]`

**組員資料**：

| 學號 | 姓名 |
|------|------|
| `[待填寫]` | `[待填寫]` |
| `[待填寫]` | `[待填寫]` |
| `[待填寫]` | `[待填寫]` |
| `[待填寫]` | `[待填寫]` |

---

## 一、專案主題與動機

### 1.1 主題簡介

Wani-Doko!（ワニどこ！）是一個針對台大日文一課程設計的互動式單字學習系統。系統名稱源自台大日文一使用的「ワニさん」教材，旨在幫助修課學生透過遊戲化的測驗方式，有效記憶和複習課程單字。

### 1.2 開發動機

1. **學習需求**：日文一課程涵蓋大量單字（L0-L12 共 13 個單元，約 500+ 個詞彙），學生需要有效的複習工具
2. **傳統方法的侷限**：紙本單字卡效率低，缺乏即時回饋；線上工具多為日檢導向，不符合課程內容
3. **遊戲化學習**：透過成就解鎖、背景收集等機制，提升學習動機
4. **實用價值**：可供實際修課學生使用，解決真實的學習痛點

### 1.3 目標使用者

- 台大日文一修課學生
- 自學日文 50 音及基礎單字的學習者
- 需要複習日語基礎詞彙的使用者

---

## 二、系統設計

### 2.1 系統架構

本系統採用 **MVC（Model-View-Controller）架構**，確保程式碼的模組化與可維護性：

```
Wani-Doko/
├── main.py                    # 程式進入點
├── config.json                # 系統配置檔
├── models/                    # 資料模型層
│   ├── database.py           # 資料庫管理
│   ├── vocabulary.py         # 單字資料結構
│   ├── quiz.py               # 測驗邏輯
│   └── user_progress.py      # 使用者進度追蹤
├── views/                     # 使用者介面層
│   ├── widgets.py            # UI 元件與主題
│   ├── main_menu_view.py     # 主選單畫面
│   ├── quiz_view.py          # 測驗畫面
│   ├── result_view.py        # 結果畫面
│   └── unlock_view.py        # 解鎖畫廊
├── controllers/               # 控制器層
│   ├── app_controller.py     # 應用程式主控制器
│   ├── quiz_controller.py    # 測驗流程控制
│   └── progress_controller.py # 進度管理
├── data/                      # 資料檔案
│   ├── vocab_unit00.csv ~ vocab_unit12.csv
│   └── trivia.json           # 日本文化小知識
├── assets/
│   ├── backgrounds/          # 背景圖片資源（13 張）
│   │   └── bg1.png ~ bg13.png
│   └── icon_*.png            # App Icon（5 種尺寸）
└── wanidoko.db               # SQLite 資料庫（執行時生成）
```

### 2.2 核心功能模組

#### 2.2.1 單字資料管理（Vocabulary Module）

**資料結構設計**：

```
Vocabulary:
    - japanese: str      # 日文詞彙（如「祖母」）
    - reading: str       # 假名讀音（如「そぼ」）
    - chinese: str       # 中文意思（如「奶奶」）
    
VocabularyBank:
    - load_from_csv(file_path) → List[Vocabulary]
    - get_by_unit(unit_id) → List[Vocabulary]
    - get_all() → List[Vocabulary]
```

**資料來源**：從 PDF 教材中提取單字，儲存為 CSV 格式，包含 13 個單元共 500+ 個詞彙。

#### 2.2.2 測驗系統（Quiz Module）

**測驗模式**：

1. **中翻日模式**（zh_to_ja）：顯示中文，選擇對應日文
2. **日翻中模式**（ja_to_zh）：顯示日文，選擇對應中文
3. **平假名模式**（hira_mode）：顯示羅馬拼音，選擇對應平假名（僅 L0）
4. **片假名模式**（kata_mode）：顯示羅馬拼音，選擇對應片假名（僅 L0）

**題目生成演算法**（偽代碼）：

```
function generate_quiz_questions(vocabs, mode, count):
    if mode is kana_mode:
        # 假名模式：過濾出指定類型的假名
        kana_type = "平假名" if mode == "hira_mode" else "片假名"
        vocabs = filter(vocabs, lambda v: v.chinese == kana_type)
    
    # 隨機抽選題目
    selected_vocabs = random_sample(vocabs, min(count, len(vocabs)))
    questions = []
    
    for vocab in selected_vocabs:
        # 根據模式設定題目與正確答案
        if mode == "zh_to_ja":
            question_text = vocab.chinese
            correct_answer = vocab.japanese
            pool = [v.japanese for v in vocabs if v != vocab]
        elif mode in ["hira_mode", "kata_mode"]:
            question_text = vocab.reading  # 羅馬拼音
            correct_answer = vocab.japanese  # 假名字符
            pool = [v.japanese for v in vocabs if v != vocab]
        else:  # ja_to_zh
            question_text = vocab.japanese
            correct_answer = vocab.chinese
            pool = [v.chinese for v in vocabs if v != vocab]
        
        # 生成 3 個干擾選項
        distractors = random_sample(pool, 3)
        options = shuffle(distractors + [correct_answer])
        correct_index = options.index(correct_answer)
        
        questions.append({
            vocab: vocab,
            question_text: question_text,
            options: options,
            correct_index: correct_index
        })
    
    return questions
```

**計分機制**：

- 每題答對得 1 分
- 即時顯示正確/錯誤回饋
- 測驗結束計算總分、正確率、用時
- 錯誤題目記錄至資料庫供複習

#### 2.2.3 資料庫系統（Database Module）

**資料表設計**：

```sql
-- 測驗結果記錄
CREATE TABLE quiz_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unit INTEGER NOT NULL,           -- 單元編號
    mode TEXT NOT NULL,               -- 測驗模式
    score INTEGER NOT NULL,           -- 得分
    total INTEGER NOT NULL,           -- 總題數
    timestamp TEXT NOT NULL           -- 測驗時間
);

-- 錯題記錄
CREATE TABLE wrong_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,         -- 對應的測驗 ID
    japanese TEXT NOT NULL,           -- 日文詞彙
    chinese TEXT NOT NULL,            -- 中文意思
    user_answer TEXT NOT NULL,        -- 使用者的錯誤答案
    FOREIGN KEY (quiz_id) REFERENCES quiz_results(id)
);

-- 背景解鎖記錄
CREATE TABLE unlocks (
    unit INTEGER PRIMARY KEY,         -- 單元編號
    unlocked_at TEXT NOT NULL         -- 解鎖時間
);
```

**資料庫操作邏輯**：

```
function save_quiz_result(unit, mode, score, total, wrong_list):
    # 1. 儲存測驗結果
    quiz_id = INSERT INTO quiz_results VALUES (unit, mode, score, total, now())
    
    # 2. 儲存錯題
    for wrong in wrong_list:
        INSERT INTO wrong_answers VALUES (quiz_id, wrong.japanese, 
                                          wrong.chinese, wrong.user_answer)
    
    # 3. 檢查解鎖條件
    if score / total >= 0.8:  # 正確率 ≥ 80%
        if unit not in unlocks:
            INSERT INTO unlocks VALUES (unit, now())
            return True  # 新解鎖
    
    return False  # 未達成解鎖
```

#### 2.2.4 使用者介面（GUI Module）

**設計理念**：採用「Kawaii」（可愛）風格的 Pastel 配色，提升使用體驗。

**色彩主題**：

- 主色調：淡紫色漸層（#FAF7FF → #F0E6FF）
- 強調色：珊瑚粉（#EC4899）、薄荷綠（#14B8A6）、淺紫（#8B5CF6）
- 文字色：深藍紫（#1E1B4B）、灰色（#64748B）

**字型選擇**：

- 介面文字：Hiragino Maru Gothic ProN（macOS 圓體，呈現柔和感）
- 日文大字：36pt bold（題目顯示）
- 日文中字：22pt（選項按鈕）

**動畫效果**：

1. **分數計數動畫**：結果畫面的分數從 0 逐步累加至實際分數
2. **按鈕 hover 效果**：滑鼠移入時背景色平滑轉換
3. **進度條**：隨答題進度平滑推進

**音效整合**：

- 使用 macOS 系統音效（`afplay` 指令）
- 點擊按鈕：Tink.aiff
- 答對：Glass.aiff（清脆聲）
- 答錯：Basso.aiff（低沉聲）
- 解鎖成就：Hero.aiff（英雄音效）

#### 2.2.5 成就系統（Unlock Module）

**解鎖機制**：

- 條件：單元測驗正確率 ≥ 80%
- 獎勵：日本城市背景圖 + 日本文化小知識

**背景與小知識配對**：

| 單元 | 主題 | 背景 | 小知識標題 | 分類 |
|------|------|------|------------|------|
| L0 | 假名 | bg1 | 綠燈其實是「藍燈」 | 語言 |
| L1 | 問候 | bg2 | 聖誕節的標配是「肯德基」 | 文化 |
| L2 | 購物 | bg3 | 方形西瓜不是用來吃的 | 文化 |
| L3 | 動詞 | bg4 | 膠囊旅館發源於大阪 | 生活 |
| L4 | 喜好 | bg5 | 嚴格的「廁所專用拖鞋」 | 禮儀 |
| L5 | 交通 | bg6 | 哈密瓜麵包裡面沒有哈密瓜 | 美食 |
| L6 | 位置 | bg7 | 吃麵發出聲音是種讚美 | 美食 |
| L7 | 家族 | bg8 | 全球自動販賣機密度最高的國家 | 生活 |
| L8 | 交通 | bg9 | 給小費反而會造成困擾 | 禮儀 |
| L9 | 食物 | bg10 | 餐廳的濕紙巾（おしぼり）只能擦手 | 禮儀 |
| L10 | 居住 | bg11 | 日常生活中仍高度依賴「印章」 | 文化 |
| L11 | 學校 | bg12 | 極度忌諱數字 4 與 9 | 文化 |
| L12 | 服裝 | bg13 | 神社裡的狐狸是神明的「使者」 | 文化 |

**全螢幕畫廊展示**：

- 點擊解鎖單元可開啟全螢幕視窗
- 顯示高解析度背景圖（AI 生成的水彩風格）
- 呈現 150-200 字的日本文化小知識
- 提供關閉按鈕返回解鎖列表

---

## 三、進階技術應用

根據課程要求，本專案使用了以下 **六項進階技術**（超過要求的三項）：

### 3.1 檔案輸入輸出（File I/O）

**應用場景**：

1. **CSV 單字載入**：
   ```python
   # vocabulary.py: VocabularyBank.load_from_csv()
   with open(csv_path, 'r', encoding='utf-8') as f:
       reader = csv.DictReader(f)
       for row in reader:
           vocab = Vocabulary(
               japanese=row['japanese'],
               reading=row['reading'],
               chinese=row['chinese']
           )
           vocabularies.append(vocab)
   ```

2. **JSON 配置與小知識載入**：
   ```python
   # unlock_view.py: 載入 trivia.json
   with open('data/trivia.json', 'r', encoding='utf-8') as f:
       trivia = json.load(f)
   ```

3. **圖片資源載入**：
   ```python
   # unlock_view.py: 載入背景圖片
   from PIL import Image, ImageTk
   img = Image.open(f'assets/backgrounds/{bg_name}.png')
   photo = ImageTk.PhotoImage(img.resize((900, 500)))
   ```

**例外處理整合**：

```python
try:
    with open(csv_path, 'r', encoding='utf-8') as f:
        # 檔案讀取邏輯
except FileNotFoundError:
    print(f"錯誤：找不到檔案 {csv_path}")
except UnicodeDecodeError:
    print(f"錯誤：檔案編碼格式不正確")
except Exception as e:
    print(f"未預期的錯誤：{e}")
```

### 3.2 進階資料結構（Advanced Data Structures）

**應用場景**：

1. **Dictionary（字典）**：
   - 儲存小知識資料（單元 ID → 小知識內容）
   - UI 元件管理（按鈕名稱 → 按鈕物件）
   ```python
   self._mode_buttons = {
       "zh_to_ja": KawaiiButton(...),
       "ja_to_zh": KawaiiButton(...),
   }
   ```

2. **Set（集合）**：
   - 管理已解鎖單元（避免重複）
   ```python
   unlocked_units = {0, 7, 9}  # 已解鎖的單元
   if current_unit in unlocked_units:
       show_unlock_gallery()
   ```

3. **Tuple（元組）**：
   - 字型設定（不可變配置）
   ```python
   FONTS = {
       "title": ("Hiragino Maru Gothic ProN", 30, "bold"),
       "japanese_lg": ("Hiragino Maru Gothic ProN", 36, "bold"),
   }
   ```

4. **Datetime（日期時間）**：
   - 記錄測驗時間與計算用時
   ```python
   from datetime import datetime
   
   start_time = datetime.now()
   # ... 測驗進行 ...
   end_time = datetime.now()
   duration = (end_time - start_time).total_seconds()
   ```

### 3.3 例外處理（Exception Handling）

**應用場景**：

1. **資料庫操作**：
   ```python
   # database.py
   try:
       cursor.execute("INSERT INTO quiz_results VALUES (?, ?, ?, ?, ?)",
                      (unit, mode, score, total, timestamp))
       conn.commit()
   except sqlite3.IntegrityError:
       print("資料庫完整性錯誤")
   except sqlite3.OperationalError:
       print("資料庫操作錯誤（可能被鎖定）")
   ```

2. **圖片載入**：
   ```python
   # unlock_view.py
   try:
       img = Image.open(bg_path)
   except FileNotFoundError:
       print(f"背景圖片不存在：{bg_path}")
       img = create_placeholder_image()  # 使用佔位圖
   except PIL.UnidentifiedImageError:
       print(f"無法識別的圖片格式：{bg_path}")
   ```

3. **音效播放**：
   ```python
   # widgets.py: SoundManager
   try:
       subprocess.run(['afplay', sound_path], check=True)
   except FileNotFoundError:
       pass  # macOS 以外的系統不支援 afplay
   except Exception:
       pass  # 音效播放失敗不影響核心功能
   ```

### 3.4 自定義類別（Custom Classes）

本專案定義了 **12+ 個自定義類別**，主要分為三層：

**Model 層類別**：

1. `Vocabulary`：單字資料結構
2. `VocabularyBank`：單字庫管理
3. `QuizSession`：測驗流程管理
4. `UserProgress`：使用者進度追蹤
5. `DatabaseManager`：資料庫操作封裝

**View 層類別**：

6. `KawaiiButton`：自定義按鈕（繼承自 `customtkinter.CTkButton`）
7. `ProgressBar`：進度條元件
8. `SoundManager`：音效管理器
9. `MainMenuView`：主選單視圖
10. `QuizView`：測驗視圖
11. `ResultView`：結果視圖
12. `UnlockView`：解鎖畫廊視圖

**Controller 層類別**：

13. `AppController`：應用程式主控制器
14. `QuizController`：測驗流程控制器
15. `ProgressController`：進度管理控制器

**類別繼承範例**：

```python
class KawaiiButton(ctk.CTkButton):
    """自定義可愛風格按鈕，繼承自 CustomTkinter 按鈕"""
    
    def __init__(self, parent, text="", command=None,
                 width=240, height=50, bg_color=None, 
                 fg_color=None, hover_color=None, ...):
        # 客製化參數處理
        _bg = bg_color or COLORS["primary"]
        _fg = fg_color or COLORS["text_light"]
        
        # 呼叫父類別建構子
        super().__init__(parent, text=text, command=command, ...)
    
    def set_text(self, text: str):
        """設定按鈕文字"""
        self.configure(text=text)
    
    def set_bg(self, color: str):
        """設定背景顏色"""
        self.configure(fg_color=color)
    
    def set_font(self, font):
        """設定字型（支援動態切換）"""
        self.configure(font=font)
```

### 3.5 圖形化介面（GUI）

**使用套件**：

- **tkinter**：Python 標準 GUI 函式庫
- **customtkinter**：現代化 UI 元件（圓角按鈕、漸層效果）
- **PIL (Pillow)**：影像處理與顯示

**主要畫面**：

1. **主選單（MainMenuView）**：
   - 13 個單元按鈕（2 行 × 7 列排列）
   - 模式選擇按鈕（中翻日、日翻中；L0 切換為平假名、片假名）
   - 開始測驗按鈕（動態啟用/禁用）
   - 底部導航：查看進度、解鎖畫廊

2. **測驗畫面（QuizView）**：
   - 頂部進度條與題號顯示
   - 中央題目卡片（白底圓角設計）
   - 四個選項按鈕（2×2 網格）
   - 即時正確/錯誤回饋

3. **結果畫面（ResultView）**：
   - 大字體分數顯示（計數動畫）
   - 正確率百分比與用時
   - 解鎖提示（達成 80% 時）
   - 返回主選單與查看錯題按鈕

4. **解鎖畫廊（UnlockView）**：
   - 13 個單元卡片（3×5 網格）
   - 已解鎖：顯示「觀看小知識與背景」按鈕
   - 未解鎖：顯示鎖頭圖示與解鎖條件
   - 全螢幕背景與小知識展示

**響應式設計**：

- 固定視窗大小：900×650 像素
- 使用 `canvas.create_window()` 實現元素定位
- 漸層背景透過 Canvas 繪製矩形實現

### 3.6 資料庫（Database）

**使用技術**：SQLite3（Python 內建）

**資料庫設計原則**：

1. **正規化**：避免資料冗餘
   - `quiz_results` 與 `wrong_answers` 透過外鍵關聯
   
2. **索引最佳化**：
   - `unit` 欄位建立索引（查詢特定單元的歷史記錄）
   
3. **資料完整性**：
   - 使用 `FOREIGN KEY` 確保錯題記錄對應有效的測驗
   - `NOT NULL` 約束防止關鍵欄位為空

**資料庫操作封裝**：

```python
class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
    
    def save_result(self, unit, mode, score, total, timestamp):
        """儲存測驗結果"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO quiz_results (unit, mode, score, total, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (unit, mode, score, total, timestamp))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_unlocked_units(self):
        """取得已解鎖的單元列表"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT unit FROM unlocks")
        return {row[0] for row in cursor.fetchall()}
    
    def get_quiz_history(self, unit=None):
        """取得測驗歷史記錄"""
        cursor = self.conn.cursor()
        if unit is not None:
            cursor.execute("""
                SELECT * FROM quiz_results 
                WHERE unit = ? 
                ORDER BY timestamp DESC
            """, (unit,))
        else:
            cursor.execute("""
                SELECT * FROM quiz_results 
                ORDER BY timestamp DESC
            """)
        return cursor.fetchall()
```

---

## 四、分工說明

**說明**：本專案為個人/小組合作開發，以下為各成員負責的主要模組與任務。

### 4.1 組員分工表

| 組員 | 主要負責模組 | 工作內容 |
|------|-------------|----------|
| `[待填寫]` | `[待填寫]` | `[待填寫]` |
| `[待填寫]` | `[待填寫]` | `[待填寫]` |
| `[待填寫]` | `[待填寫]` | `[待填寫]` |
| `[待填寫]` | `[待填寫]` | `[待填寫]` |

### 4.2 協作方式

- **版本控制**：使用 Git 進行程式碼版本管理
- **溝通管道**：LINE 群組 + 定期實體會議
- **文件管理**：Google Docs 共同編輯規格文件
- **測試分工**：交叉測試（開發者測試其他成員的模組）

---

## 五、開發挑戰與解決方案

### 5.1 技術挑戰

**挑戰 1：tkinter 與 CustomTkinter 的整合**

- **問題**：CustomTkinter 的 `CTkButton` 與標準 tkinter 在參數命名上有差異（如 `fg_color` vs `bg`）
- **解決**：封裝自定義 `KawaiiButton` 類別，統一參數介面

**挑戰 2：假名模式的字體顯示問題**

- **問題**：按鈕文字從英文切換到日文假名時，字體未正確更新
- **解決**：新增 `set_font()` 方法，在切換模式時動態調整字型

**挑戰 3：單元列表超出視窗範圍**

- **問題**：13 個單元按鈕水平排列超過 900px 寬度
- **解決**：改用 `grid` 佈局，分成 2 行顯示（每行 7 個）

### 5.2 設計挑戰

**挑戰 1：測驗題目的干擾選項生成**

- **問題**：完全隨機的干擾選項可能過於明顯（如問「媽媽」給出「飛機」選項）
- **解決**：從同一單元或同一類別（如家族詞彙）中抽取干擾選項

**挑戰 2：背景與小知識的配對**

- **問題**：需要 13 張背景對應 13 個單元
- **解決**：使用統一命名（bg1-bg13），每個關卡專屬背景，提升解鎖成就感

### 5.3 v1.2 版本更新與修復

**更新 1：修復白屏 Bug**

- **問題**：進入測驗或結果畫面時出現空白畫面
- **原因**：`quiz_view.py` 和 `result_view.py` 創建 canvas 後未調用 `pack()`
- **解決**：在創建 canvas 後加入 `self._canvas.pack(fill=tk.BOTH, expand=True)`

**更新 2：修復背景載入錯誤**

- **問題**：背景圖片無法載入，錯誤訊息 `Image.Resampling.FAST` 不存在
- **原因**：Pillow 函式庫沒有 `FAST` 這個 resampling 常數
- **解決**：改用 `Image.BILINEAR`（快速且品質好）

**更新 3：13 張專屬背景**

- **功能**：每個關卡（L0-L12）都有專屬的解鎖背景（bg1-bg13）
- **實作**：統一背景命名規則，更新 `trivia.json` 對應關係

**更新 4：App Icon**

- **功能**：程式視窗顯示鱷魚 emoji 🐊 作為 icon（呼應 ワニさん 教材）
- **實作**：生成多種尺寸 icon（16/32/64/128/256px），在 `app_controller.py` 中設定

**更新 5：自訂背景功能**

- **功能**：解鎖後可設為主選單、測驗、結果畫面的背景
- **實作**：創建 `background_helper.py` 統一背景處理，支援快取機制

**更新 6：文化小知識更新**

- **功能**：更換 13 個更生動有趣的日本文化冷知識
- **內容**：涵蓋語言、文化、禮儀、美食、生活等多元面向

---

## 六、系統特色與創新

### 6.1 特色功能

1. **多模式測驗**：支援四種測驗模式，涵蓋假名、單字的雙向學習
2. **成就解鎖系統**：透過遊戲化機制提升學習動機
3. **文化知識整合**：結合日本文化介紹，寓教於樂
4. **Kawaii 美學設計**：柔和配色與動畫效果，提升使用體驗
5. **錯題追蹤**：自動記錄錯誤，支援後續複習（可擴充功能）

### 6.2 創新點

1. **課程導向設計**：針對台大日文一課程內容，而非泛用日檢工具
2. **本地化資料**：使用台灣學生熟悉的中文翻譯
3. **跨平台音效**：優雅處理 macOS 系統音效（其他系統靜音降級）

---

## 七、未來展望

### 7.1 可擴充功能

1. **間隔重複演算法（Spaced Repetition）**：
   - 根據使用者的錯題記錄，智慧調整複習頻率
   - 實作類似 Anki 的記憶曲線演算法

2. **聽力測驗模式**：
   - 整合 Google TTS API 或錄製真人發音
   - 新增聽力辨識題型

3. **多人競賽模式**：
   - 透過網路連線實現即時對戰
   - 排行榜系統

4. **錯題本功能**：
   - 專門針對錯題進行複習測驗
   - 統計最常錯誤的單字

5. **跨平台支援**：
   - 移植至 Web 版本（Flask + JavaScript）
   - 開發手機 App（Kivy 或 React Native）

### 7.2 效能優化

1. **資料庫查詢最佳化**：建立複合索引加速歷史記錄查詢
2. **圖片快取機制**：預先載入背景圖片，減少開啟延遲
3. **程式碼重構**：進一步模組化，提升可測試性

---

## 八、參考資源

### 8.1 技術文件

- Python 官方文件：https://docs.python.org/3/
- tkinter 文件：https://docs.python.org/3/library/tkinter.html
- CustomTkinter 文件：https://customtkinter.tomschimansky.com/
- SQLite 官方文件：https://www.sqlite.org/docs.html
- Pillow (PIL) 文件：https://pillow.readthedocs.io/

### 8.2 學習資源

- 台大日文一（ワニさん）教材
- 日本國際交流基金會（JF）日本語教育資源

### 8.3 設計靈感

- Duolingo（遊戲化語言學習）
- Anki（間隔重複記憶）
- Quizlet（互動式單字卡）

---

## 九、組員心得感想

### 9.1 `[組員 1 姓名]` - `[學號]`

`[待填寫]`

---

### 9.2 `[組員 2 姓名]` - `[學號]`

`[待填寫]`

---

### 9.3 `[組員 3 姓名]` - `[學號]`

`[待填寫]`

---

### 9.4 `[組員 4 姓名]` - `[學號]`

`[待填寫]`

---

## 十、結語

Wani-Doko! 專案從構思到實作，歷經需求分析、系統設計、編碼開發、測試除錯等完整的軟體開發流程。透過 MVC 架構的實踐，我們深刻體會到模組化設計的重要性；透過 GUI 與資料庫的整合，我們學習到如何建構完整的使用者應用程式。

這個專案不僅是程式設計的練習，更是團隊合作、問題解決與自主學習能力的綜合訓練。我們期待這個系統能真正幫助到台大日文一的修課同學，也希望未來能持續優化，擴充更多實用功能。

感謝授課老師與助教的指導，以及組員們的通力合作！

---

**專案 GitHub**：`[待填寫]`

**展示影片**：`[待填寫]`

**最後更新**：2026-05-31（v1.2.1）
