# 🚀 快速打包指南

## 給組員錄 Demo 的最快方法

### Windows 使用者（推薦）

#### 方法 1：一鍵打包（最簡單）

1. **雙擊執行** `build.bat`
2. 等待 3-5 分鐘
3. 完成後會在 `dist/Wani-Doko/` 產生執行檔
4. 壓縮整個 `Wani-Doko` 資料夾傳給組員

#### 方法 2：手動打包

```cmd
pip install pyinstaller
pyinstaller Wani-Doko.spec
```

執行檔在 `dist/Wani-Doko/Wani-Doko.exe`

---

### macOS 使用者（你）

你可以幫 Windows 組員打包，但需要：

1. 借一台 Windows 電腦
2. 或使用虛擬機（Parallels Desktop / VMware）
3. 或讓 Windows 組員自己打包

**注意**：macOS 無法直接打包成 Windows .exe 檔

---

## 📦 發布給組員

### 上傳到 GitHub Releases（推薦）

```bash
# 1. 打包完成後，壓縮
cd dist
zip -r Wani-Doko-Windows.zip Wani-Doko/

# 2. 在 GitHub 上創建 Release
# - 去你的 repo → Releases → Create a new release
# - Tag: v1.0
# - Title: Wani-Doko v1.0 - Windows 執行檔
# - 上傳 Wani-Doko-Windows.zip
```

### 或使用 Google Drive

1. 壓縮 `dist/Wani-Doko/` 資料夾
2. 上傳到 Google Drive
3. 設定為「知道連結的任何人」都可以查看
4. 複製連結傳給組員

---

## ✅ 給組員的使用說明

**下載後：**

1. 解壓縮 `Wani-Doko-Windows.zip`
2. 雙擊 `Wani-Doko.exe`
3. 如果出現「Windows 已保護您的電腦」：
   - 點「其他資訊」→「仍要執行」

**錄影 Demo：**

- 建議使用 OBS Studio 或 Windows 內建錄影（Win + G）
- 錄製時展示所有功能：測驗、結果、解鎖畫廊

---

## 🐛 如果打包失敗

### 錯誤：找不到某個模組

```cmd
pip install customtkinter pillow
pyinstaller Wani-Doko.spec --clean
```

### 錯誤：資料檔案遺失

檢查這些檔案是否存在：
- `data/*.csv` (13 個檔案)
- `data/trivia.json`
- `assets/backgrounds/*.png` (5 張圖片)
- `config.json`

### 執行檔啟動後立刻關閉

```cmd
# 用這個指令檢查錯誤訊息
dist\Wani-Doko\Wani-Doko.exe
```

或修改 spec 檔案：
```python
console=True,  # 改成 True 可以看到錯誤訊息
```

---

## 📊 檔案大小參考

- 壓縮前：~100-150 MB
- 壓縮後：~40-60 MB
- 上傳時間：依網路速度，約 2-5 分鐘

---

## 💡 小技巧

### 如果組員沒有 Windows

可以請他們：
1. 用 Python 執行（參考 README.md）
2. 或在 macOS/Linux 上用 Python 執行

### 如果想要更小的執行檔

使用單檔模式（但啟動較慢）：

```cmd
pyinstaller --onefile --noconsole main.py
```

### 如果想加入圖示

1. 準備 `icon.ico` 檔案
2. 放在專案根目錄
3. 在 `Wani-Doko.spec` 中加入：
   ```python
   icon='icon.ico',
   ```

---

**有問題？查看完整的 `BUILD_GUIDE.md`！**
