# 🔄 更新說明 v1.1

## 📅 更新日期：2026-05-31

---

## ✨ 新功能與修正

### 1. ✅ 修正：移除個人紀錄共享問題

**問題**：組員下載專案後會看到原開發者的測驗紀錄

**解決方案**：
- 將 `wanidoko.db` 從 Git 追蹤中移除
- 每位使用者執行程式時會自動建立自己的資料庫
- 已在 `.gitignore` 中排除所有 `.db` 檔案

**影響**：
- ✅ 每個人都有獨立的測驗紀錄
- ✅ 不會互相干擾
- ✅ 資料庫會在首次執行時自動建立

---

### 2. ✅ 新增：中翻日模式顯示平假名標註

**需求**：中翻日測驗時，選項應顯示「漢字（平假名）」格式

**實作**：
- 修改 `models/quiz.py` 的題目生成邏輯
- 中翻日模式選項格式：`祖母（そぼ）`
- 其他模式維持不變

**範例**：

**修改前**：
```
題目：奶奶（自稱）
選項：祖母 / 祖父 / 母 / 父
```

**修改後**：
```
題目：奶奶（自稱）
選項：祖母（そぼ）/ 祖父（そふ）/ 母（はは）/ 父（ちち）
```

---

### 3. ✅ 新增：自訂背景功能

**需求**：解鎖背景後可以設為主選單背景

**新增檔案**：
- `models/config_manager.py` - 配置管理器

**修改檔案**：
- `config.json` - 新增 `custom_background` 欄位
- `views/unlock_view.py` - 新增「設為背景」按鈕
- `views/main_menu_view.py` - 支援載入自訂背景

**使用方式**：

1. **設定背景**：
   - 進入「解鎖背景」
   - 點擊已解鎖的單元
   - 點擊「🎨 設為背景」按鈕
   - 重新進入主選單即可看到效果

2. **重置背景**：
   - 主選單會顯示「🔄 預設背景」按鈕（僅在有自訂背景時顯示）
   - 點擊即可恢復預設漸層背景

3. **背景清單**：
   - Tokyo（東京）- 現代都市風景
   - Osaka（大阪）- 熱鬧街道
   - Kyoto（京都）- 古都寺廟
   - Nara（奈良）- 鹿與神社
   - Fuji（富士山）- 聖山風景

**技術細節**：
- 背景圖片會自動增加亮度（1.3 倍）
- 加上半透明白色遮罩確保文字清晰可讀
- 背景設定儲存在 `config.json`，不會影響其他使用者
- Footer 會顯示當前使用的背景名稱

---

## 📝 檔案變更清單

### 新增檔案
```
✅ models/config_manager.py       - 配置檔案管理器
✅ requirements.txt               - Python 相依套件清單
✅ README.md                      - 完整專案說明
✅ Wani-Doko.spec                 - PyInstaller 打包配置
✅ build.bat                      - Windows 一鍵打包腳本
✅ BUILD_GUIDE.md                 - 詳細打包教學
✅ QUICK_BUILD.md                 - 快速打包指南
```

### 修改檔案
```
✅ .gitignore                     - 排除資料庫和建置檔案
✅ config.json                    - 新增 custom_background 欄位
✅ models/quiz.py                 - 中翻日選項加上平假名
✅ views/unlock_view.py           - 新增設為背景功能
✅ views/main_menu_view.py        - 支援自訂背景載入與重置
```

### 刪除追蹤
```
❌ wanidoko.db                    - 從 Git 移除（改為本地生成）
```

---

## 🚀 部署步驟

### 提交變更到 GitHub

```bash
cd "/Users/allen/Desktop/Final Project"

# 1. 查看變更
git status

# 2. 新增所有新檔案
git add models/config_manager.py requirements.txt README.md \
        Wani-Doko.spec build.bat BUILD_GUIDE.md QUICK_BUILD.md \
        WRITTEN_REPORT.md CHANGELOG.md

# 3. 提交變更
git commit -m "v1.1: Fix shared database, add furigana, add custom background feature"

# 4. 推送到 GitHub
git push origin main
```

### 通知組員更新

**訊息範本**：

```
📢 Wani-Doko! 已更新至 v1.1！

✨ 新功能：
1. 修正資料庫共享問題 - 每個人都有自己的紀錄了！
2. 中翻日模式會顯示平假名標註（例如：祖母（そぼ））
3. 可以自訂主選單背景（解鎖後設定）

🔄 如何更新：
git pull origin main

或重新 clone：
git clone [你的 repo 連結]

📖 詳細說明請看：
- CHANGELOG.md（變更說明）
- README.md（安裝與使用說明）
```

---

## 🐛 疑難排解

### Q1: 更新後資料庫錯誤

**解決方法**：
```bash
# 刪除舊的資料庫（如果存在）
rm wanidoko.db

# 重新執行程式，會自動建立新資料庫
python main.py
```

### Q2: 自訂背景無法顯示

**檢查項目**：
1. 確認 `assets/backgrounds/` 資料夾中有圖片
2. 確認 `config.json` 中 `custom_background` 的值是正確的檔名
3. 嘗試重新設定背景

**重置方法**：
```bash
# 手動編輯 config.json
# 將 "custom_background": "xxx" 改為 "custom_background": null
```

### Q3: 平假名標註顯示亂碼

**原因**：CSV 檔案編碼問題

**解決方法**：
```bash
# 確認 CSV 檔案是 UTF-8 編碼
file -I data/vocab_unit*.csv

# 如果不是 UTF-8，需要轉換編碼
```

---

## 📊 版本比較

| 功能 | v1.0 | v1.1 |
|------|------|------|
| 資料庫 | 共享（有問題） | 獨立 ✅ |
| 中翻日選項 | 只有漢字 | 漢字+平假名 ✅ |
| 背景設定 | 固定漸層 | 可自訂 ✅ |
| 跨平台文件 | 無 | 完整 ✅ |
| 打包工具 | 無 | 一鍵打包 ✅ |

---

## 💡 未來可能的功能

以下功能可視需求加入：

- [ ] 匯出錯題本為 PDF
- [ ] 背景圖片模糊度調整
- [ ] 更多背景主題選擇
- [ ] 背景輪播模式
- [ ] 音效開關設定
- [ ] 深色模式

---

**有問題歡迎隨時回報！**

---

## 📞 聯絡資訊

- **GitHub Issues**: [專案 Issues 頁面]
- **Email**: `[待填寫]`

---

**最後更新**: 2026-05-31 by `[你的名字]`
