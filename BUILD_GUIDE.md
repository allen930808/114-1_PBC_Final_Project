# 建立 Windows 執行檔教學

## 📦 方法一：自動打包腳本（推薦）

### 步驟 1：安裝 PyInstaller

在專案資料夾中執行：

```cmd
pip install pyinstaller
```

### 步驟 2：執行打包

**使用提供的 spec 檔案**（已設定好所有參數）：

```cmd
pyinstaller Wani-Doko.spec
```

### 步驟 3：找到執行檔

打包完成後，執行檔位於：

```
dist/Wani-Doko/Wani-Doko.exe
```

### 步驟 4：發布給組員

將整個 `dist/Wani-Doko/` 資料夾壓縮成 ZIP 檔：

```cmd
# 在 dist 資料夾中
# 右鍵點擊 Wani-Doko 資料夾 → 傳送到 → 壓縮的 (zipped) 資料夾
```

組員下載後解壓縮，直接雙擊 `Wani-Doko.exe` 即可執行！

---

## 📦 方法二：單一檔案模式（較慢但更方便）

如果想要打包成單一 .exe 檔案（所有東西都在一個檔案裡）：

```cmd
pyinstaller --onefile --noconsole --name "Wani-Doko" ^
    --add-data "data;data" ^
    --add-data "assets;assets" ^
    --add-data "config.json;." ^
    --hidden-import customtkinter ^
    --hidden-import PIL._tkinter_finder ^
    main.py
```

**優點**：只有一個 .exe 檔案，方便分享  
**缺點**：啟動較慢（每次執行都要解壓縮）

執行檔位於：`dist/Wani-Doko.exe`

---

## 🐛 常見問題排解

### 問題 1：打包後執行出現 "Failed to execute script"

**原因**：通常是資料檔案路徑問題

**解決方法**：使用 spec 檔案（方法一）確保所有檔案都被包含

### 問題 2：執行檔很大（超過 100MB）

**說明**：正常現象。PyInstaller 會包含整個 Python 環境和所有相依套件。

**優化方法**：
```cmd
# 安裝 UPX 壓縮工具（可選）
# 下載：https://upx.github.io/
# 將 upx.exe 放在系統 PATH 中，PyInstaller 會自動使用
```

### 問題 3：防毒軟體誤報

**說明**：PyInstaller 打包的程式有時會被誤判為病毒

**解決方法**：
1. 在防毒軟體中加入例外
2. 或告訴組員這是正常的誤報
3. 上傳到 VirusTotal 檢查：https://www.virustotal.com/

### 問題 4：CustomTkinter 元件顯示異常

**解決方法**：確認已加入 hidden imports

```cmd
pyinstaller Wani-Doko.spec --clean
```

### 問題 5：資料庫無法寫入

**原因**：執行檔可能被放在唯讀位置（如 C:\Program Files）

**解決方法**：告訴使用者將程式放在「文件」或「桌面」等可寫入的位置

---

## 📋 完整打包檢查清單

打包前確認：

- [ ] 所有 CSV 檔案都在 `data/` 資料夾
- [ ] 所有 PNG 圖片都在 `assets/backgrounds/` 資料夾
- [ ] `config.json` 和 `trivia.json` 存在
- [ ] 已安裝 PyInstaller：`pip install pyinstaller`
- [ ] 在本機測試過程式可正常執行

打包後測試：

- [ ] 執行 `dist/Wani-Doko/Wani-Doko.exe`
- [ ] 測試所有功能：主選單、測驗、結果、解鎖畫廊
- [ ] 確認圖片正常顯示
- [ ] 確認測驗記錄可正常儲存
- [ ] 在另一台沒有 Python 的電腦上測試

---

## 🎁 發布給組員

### 方法 A：Google Drive / OneDrive

1. 將 `dist/Wani-Doko/` 整個資料夾壓縮成 ZIP
2. 上傳到雲端硬碟
3. 分享連結給組員

### 方法 B：GitHub Releases

1. 在 GitHub 專案頁面點擊「Releases」
2. 點擊「Create a new release」
3. 上傳壓縮檔
4. 組員可以從 Releases 頁面下載

### 使用說明（給組員）

```
Wani-Doko 使用說明

1. 下載 Wani-Doko.zip 並解壓縮
2. 進入解壓縮後的資料夾
3. 雙擊 Wani-Doko.exe 執行程式
4. 如果 Windows 顯示「Windows 已保護您的電腦」：
   - 點擊「其他資訊」
   - 點擊「仍要執行」

注意事項：
- 第一次啟動可能較慢（5-10秒），請耐心等待
- 不要刪除 exe 檔案旁邊的其他資料夾和檔案
- 建議將整個資料夾放在桌面或文件資料夾中
```

---

## 🔍 進階選項

### 加入自訂圖示

1. 準備一個 `.ico` 檔案（256×256 或 512×512）
2. 放在專案根目錄，命名為 `icon.ico`
3. 在 `Wani-Doko.spec` 中修改：
   ```python
   icon='icon.ico',  # 原本是 None
   ```

### 減少檔案大小

在 spec 檔案中加入排除項：

```python
excludes=[
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'pytest',
],
```

### 加入版本資訊

建立 `version.txt`：

```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'NTU PBC'),
        StringStruct(u'FileDescription', u'Wani-Doko! 日文單字訓練系統'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'ProductName', u'Wani-Doko!'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

然後在打包時加上：

```cmd
pyinstaller Wani-Doko.spec --version-file version.txt
```

---

## ⏱️ 預估打包時間

- 安裝 PyInstaller：1 分鐘
- 第一次打包：3-5 分鐘
- 後續打包：1-2 分鐘
- 檔案大小：約 80-120 MB（含所有資料）

---

## 📞 需要幫助？

如果遇到問題：

1. 確認 Python 版本：`python --version`（需要 3.8+）
2. 確認 PyInstaller 版本：`pyinstaller --version`（建議 5.0+）
3. 刪除舊的 build 和 dist 資料夾後重新打包
4. 查看詳細錯誤訊息：`pyinstaller Wani-Doko.spec --log-level DEBUG`

---

**祝打包順利！🎉**
