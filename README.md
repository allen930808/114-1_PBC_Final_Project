# Wani-Doko! (ワニどこ!) 

NTU 日文一單字訓練系統 | NTU Japanese 1 Vocabulary Trainer

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## 📖 專案簡介

Wani-Doko! 是一個針對台大日文一課程設計的互動式單字學習系統，提供：

- 🎯 **多模式測驗**：中翻日、日翻中、平假名、片假名練習
- 🏆 **成就系統**：達成 80% 正確率解鎖日本城市背景與文化小知識
- 🎨 **Kawaii 美學**：柔和配色、動畫效果、音效回饋
- 📊 **進度追蹤**：自動記錄測驗歷史與錯題
- 🗾 **文化學習**：13 個日本文化小知識

## 🚀 快速開始

### 系統需求

- **Python**：3.8 或以上版本
- **作業系統**：Windows 10/11、macOS 10.14+、Linux
- **螢幕解析度**：建議 1280×720 以上

### Windows 安裝步驟

#### 1. 安裝 Python

如果尚未安裝 Python，請至 [python.org](https://www.python.org/downloads/) 下載並安裝。

**重要**：安裝時請勾選「Add Python to PATH」！

驗證安裝：
```cmd
python --version
```

#### 2. 下載專案

**方法一：使用 Git**
```cmd
git clone https://github.com/[你的帳號]/wani-doko.git
cd wani-doko
```

**方法二：直接下載**
- 點擊 GitHub 頁面上的「Code」→「Download ZIP」
- 解壓縮到任意資料夾
- 使用命令提示字元（cmd）或 PowerShell 進入該資料夾

#### 3. 安裝相依套件

在專案資料夾中執行：

```cmd
pip install -r requirements.txt
```

如果遇到權限問題，可以加上 `--user`：
```cmd
pip install --user -r requirements.txt
```

#### 4. 執行程式

```cmd
python main.py
```

### macOS/Linux 安裝步驟

#### 1. 確認 Python 版本

```bash
python3 --version
```

#### 2. 下載專案

```bash
git clone https://github.com/[你的帳號]/wani-doko.git
cd wani-doko
```

#### 3. 安裝相依套件

```bash
pip3 install -r requirements.txt
```

#### 4. 執行程式

```bash
python3 main.py
```

## 🎮 使用說明

### 基本操作

1. **選擇單元**：點擊 L0～L12 任一單元按鈕
2. **選擇模式**：
   - 中 → 日：看中文選日文
   - 日 → 中：看日文選中文
   - あ 平假名：看羅馬拼音選平假名（僅 L0）
   - ア 片假名：看羅馬拼音選片假名（僅 L0）
3. **開始測驗**：點擊「開始測驗」按鈕
4. **答題**：點擊你認為正確的選項
5. **查看結果**：測驗結束後可查看分數、正確率、用時

### 解鎖系統

- 任一單元達成 **80% 以上正確率**即可解鎖該單元的背景與小知識
- 點擊主選單的「🔓 解鎖背景」查看已解鎖內容
- 點擊「觀看小知識與背景」可全螢幕欣賞日本城市美景與文化介紹

## 📁 專案結構

```
wani-doko/
├── main.py                    # 程式進入點
├── requirements.txt           # Python 相依套件
├── config.json                # 系統配置
├── models/                    # 資料模型
│   ├── database.py           # 資料庫管理
│   ├── vocabulary.py         # 單字資料結構
│   ├── quiz.py               # 測驗邏輯
│   └── user_progress.py      # 進度追蹤
├── views/                     # 使用者介面
│   ├── widgets.py            # UI 元件
│   ├── main_menu_view.py     # 主選單
│   ├── quiz_view.py          # 測驗畫面
│   ├── result_view.py        # 結果畫面
│   └── unlock_view.py        # 解鎖畫廊
├── controllers/               # 控制器
│   ├── app_controller.py     # 主控制器
│   ├── quiz_controller.py    # 測驗控制
│   └── progress_controller.py # 進度管理
├── data/                      # 資料檔案
│   ├── vocab_unit00.csv ~ vocab_unit12.csv
│   └── trivia.json           # 文化小知識
├── assets/backgrounds/        # 背景圖片
│   ├── tokyo.png, osaka.png, kyoto.png
│   ├── nara.png, fuji.png
└── wanidoko.db               # SQLite 資料庫（自動生成）
```

## 🔧 常見問題排解

### Windows 常見問題

#### 問題 1：`python` 指令找不到

**解決方法**：
- 重新安裝 Python，確認勾選「Add Python to PATH」
- 或使用 `py` 指令代替：`py main.py`

#### 問題 2：ModuleNotFoundError: No module named 'customtkinter'

**解決方法**：
```cmd
pip install customtkinter Pillow
```

#### 問題 3：視窗顯示模糊（高 DPI 螢幕）

**解決方法**：
- 在程式圖示上右鍵 → 內容 → 相容性
- 勾選「覆寫高 DPI 縮放行為」
- 選擇「系統（增強）」

#### 問題 4：中文顯示亂碼

**解決方法**：
- 確認 Windows 系統語言設定為「中文（台灣）」
- 或在命令提示字元執行：
  ```cmd
  chcp 65001
  python main.py
  ```

### macOS 常見問題

#### 問題 1：字體顯示異常

**說明**：程式使用 Hiragino Maru Gothic ProN 字體（macOS 內建），Windows 會自動降級使用系統字體。

#### 問題 2：沒有音效

**說明**：音效使用 macOS 的 `afplay` 指令，Windows 環境會自動靜音（不影響功能）。

### 通用問題

#### 問題：資料庫錯誤

**解決方法**：刪除 `wanidoko.db` 檔案，程式會自動重新建立。

#### 問題：圖片無法載入

**解決方法**：確認 `assets/backgrounds/` 資料夾中有 5 張 PNG 圖片。

## 🛠️ 技術細節

### 使用技術

- **程式語言**：Python 3.8+
- **GUI 框架**：tkinter + CustomTkinter
- **圖片處理**：Pillow (PIL)
- **資料庫**：SQLite3
- **架構模式**：MVC (Model-View-Controller)

### 進階技術應用（符合課程要求）

✅ **檔案 I/O**：CSV 單字載入、JSON 配置、圖片資源  
✅ **進階資料結構**：dict、set、tuple、datetime  
✅ **例外處理**：檔案載入、資料庫操作、圖片處理  
✅ **自定義類別**：12+ 個類別，含繼承與封裝  
✅ **圖形化介面**：完整的 GUI 應用程式  
✅ **資料庫**：SQLite3，含 3 張關聯資料表  

## 📊 資料庫結構

### quiz_results（測驗結果）
- id: 主鍵
- unit: 單元編號
- mode: 測驗模式
- score: 得分
- total: 總題數
- timestamp: 測驗時間

### wrong_answers（錯題記錄）
- id: 主鍵
- quiz_id: 對應測驗 ID（外鍵）
- japanese: 日文詞彙
- chinese: 中文意思
- user_answer: 使用者的錯誤答案

### unlocks（解鎖記錄）
- unit: 單元編號（主鍵）
- unlocked_at: 解鎖時間

## 🎨 截圖預覽

*(建議在此處加入專案截圖)*

## 📝 開發團隊

- **開發者**：`[組員姓名]`
- **課程**：NTU 商管程式設計（114-2）
- **指導老師**：`[老師姓名]`

## 📄 授權條款

本專案為台大商管程式設計課程期末專案，僅供教育用途。

## 🙏 致謝

- 台大日文一（ワニさん）教材
- CustomTkinter 開發團隊
- 所有測試使用者的寶貴回饋

---

**最後更新**：2026-05-31

**如有問題，請聯繫**：`[Email]`
