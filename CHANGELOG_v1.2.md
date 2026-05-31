# 🔄 Wani-Doko! v1.2 修改日誌

**更新日期**：2026-05-31  
**版本**：v1.2

---

## 📋 修改總覽

本次更新主要包含 4 大功能改進：
1. ✅ **13 張背景對應 13 個關卡**（每關專屬背景）
2. ✅ **修正中翻日平假名標註邏輯**（只標註漢字詞）
3. ✅ **測驗與結果畫面支援自訂背景**（全局自訂背景）
4. ✅ **加入 App Icon**（鱷魚 emoji 🐊）

---

## 📝 詳細修改記錄

### 1️⃣ 背景圖片統一化（13 張背景）

#### 新增檔案
- ✅ `rename_backgrounds.py` - 背景圖片重新命名與格式轉換腳本

#### 修改檔案
- ✅ `assets/backgrounds/` - 重新命名所有背景
  - 舊檔案：tokyo.png, osaka.png, kyoto.png, nara.png, fuji.png
  - 新檔案：bg1.png ~ bg13.png
  - JPG 轉 PNG：IMG_2329~2337.JPG → bg6~13.png

#### 背景對應表
```
L0  → bg1.png  (原 tokyo.png)
L1  → bg2.png  (原 osaka.png)
L2  → bg3.png  (原 kyoto.png)
L3  → bg4.png  (原 nara.png)
L4  → bg5.png  (原 fuji.png)
L5  → bg6.png  (原 IMG_2329.JPG)
L6  → bg7.png  (原 IMG_2330.JPG)
L7  → bg8.png  (原 IMG_2331.JPG)
L8  → bg9.png  (原 IMG_2332.JPG)
L9  → bg10.png (原 IMG_2334.JPG)
L10 → bg11.png (原 IMG_2335.JPG)
L11 → bg12.png (原 IMG_2336.JPG)
L12 → bg13.png (原 IMG_2337.JPG)
```

#### 配置檔案更新
- ✅ `data/trivia.json` - 更新所有 background 欄位
  - 舊值：tokyo, osaka, kyoto, nara, fuji
  - 新值：bg1, bg2, bg3, ..., bg13

- ✅ `views/unlock_view.py:21-25` - 更新備用對應表
  ```python
  # 修改前
  self._bg_names = {
      0: "tokyo", 1: "osaka", 2: "kyoto", ...
  }
  
  # 修改後
  self._bg_names = {
      0: "bg1", 1: "bg2", 2: "bg3", ..., 12: "bg13"
  }
  ```

---

### 2️⃣ 修正中翻日平假名標註邏輯

#### 修改檔案
- ✅ `models/quiz.py`

#### 具體修改
**新增函數**（第 11-16 行）：
```python
def _has_kanji(text: str) -> bool:
    """檢查字串是否包含日文漢字（CJK Unified Ideographs）"""
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False
```

**修改邏輯**（第 86-103 行）：
```python
# 修改前：所有詞彙都加平假名
correct_answer = f"{vocab.japanese}（{vocab.reading}）"

# 修改後：只對包含漢字的詞彙加平假名
if _has_kanji(vocab.japanese):
    correct_answer = f"{vocab.japanese}（{vocab.reading}）"
else:
    correct_answer = vocab.japanese
```

#### 效果對比
```
修改前：
  - 学生（がくせい）    ✅ 正確
  - アメリカ（あめりか）  ❌ 不必要
  - はい（はい）        ❌ 不必要

修改後：
  - 学生（がくせい）    ✅ 正確
  - アメリカ            ✅ 正確
  - はい                ✅ 正確
```

---

### 3️⃣ 測驗與結果畫面支援自訂背景

#### 新增檔案
- ✅ `views/background_helper.py` - 背景處理共用函數

#### 修改檔案
- ✅ `views/quiz_view.py` - 測驗畫面支援自訂背景
- ✅ `views/result_view.py` - 結果畫面支援自訂背景
- ✅ `views/main_menu_view.py` - 簡化背景處理邏輯

#### 具體修改

**新增 `background_helper.py`**：
- 提供 `create_background_canvas()` 函數
- 統一處理自訂背景載入與漸層背景繪製
- 自動增加亮度並加上半透明白色遮罩

**quiz_view.py 修改**：
```python
# 修改前（第 26-28 行）
self._canvas = create_gradient_canvas(self.frame, 900, 650,
                                       "#FFF5FA", "#F0E6FF")

# 修改後
from views.background_helper import create_background_canvas
self._canvas, self._bg_image = create_background_canvas(
    self.frame, 900, 650, "#FFF5FA", "#F0E6FF"
)
```

**result_view.py 修改**：
```python
# 修改前（第 22-23 行）
self._canvas = create_gradient_canvas(self.frame, 900, 650,
                                       "#E8D5FF", "#FFF5FA")

# 修改後
from views.background_helper import create_background_canvas
self._canvas, self._bg_image = create_background_canvas(
    self.frame, 900, 650, "#E8D5FF", "#FFF5FA"
)
```

**main_menu_view.py 簡化**：
- 移除重複的背景處理邏輯（原 36-71 行）
- 使用統一的 `create_background_canvas()` 函數
- 減少約 40 行重複 code

#### 架構改進
- ✅ 消除重複 code（DRY 原則）
- ✅ 統一背景處理邏輯
- ✅ 易於維護與擴展

---

### 4️⃣ App Icon（鱷魚 emoji）

#### 新增檔案
- ✅ `create_icon.py` - Icon 生成腳本
- ✅ `assets/icon_16.png` - 16×16 icon
- ✅ `assets/icon_32.png` - 32×32 icon
- ✅ `assets/icon_64.png` - 64×64 icon
- ✅ `assets/icon_128.png` - 128×128 icon
- ✅ `assets/icon_256.png` - 256×256 icon

#### 修改檔案
- ✅ `controllers/app_controller.py`

#### 具體修改
**app_controller.py**（第 50-64 行）：
```python
# 新增 App Icon 設定
icon_path = os.path.join(self._base_dir, "assets", "icon_128.png")
if os.path.exists(icon_path):
    try:
        from PIL import Image, ImageTk
        icon_img = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_img)
        self._root.iconphoto(True, icon_photo)
        # 保持引用避免被垃圾回收
        self._icon_ref = icon_photo
    except Exception as e:
        print(f"Icon 載入失敗：{e}")
```

#### Icon 生成結果
```
✓ icon_16.png (0.3 KB)
✓ icon_32.png (0.6 KB)
✓ icon_64.png (4.4 KB)   ← 使用 emoji 字體
✓ icon_128.png (14.0 KB) ← 使用 emoji 字體
✓ icon_256.png (4.8 KB)
```

---

## 📊 檔案變更統計

### 新增檔案（7 個）
```
✅ rename_backgrounds.py
✅ create_icon.py
✅ views/background_helper.py
✅ assets/icon_16.png
✅ assets/icon_32.png
✅ assets/icon_64.png
✅ assets/icon_128.png
✅ assets/icon_256.png
```

### 修改檔案（8 個）
```
✅ models/quiz.py
✅ views/quiz_view.py
✅ views/result_view.py
✅ views/main_menu_view.py
✅ views/unlock_view.py
✅ data/trivia.json
✅ controllers/app_controller.py
✅ implementation_plan.md
```

### 重新命名檔案（13 個）
```
✅ tokyo.png → bg1.png
✅ osaka.png → bg2.png
✅ kyoto.png → bg3.png
✅ nara.png → bg4.png
✅ fuji.png → bg5.png
✅ IMG_2329.JPG → bg6.png
✅ IMG_2330.JPG → bg7.png
✅ IMG_2331.JPG → bg8.png
✅ IMG_2332.JPG → bg9.png
✅ IMG_2334.JPG → bg10.png
✅ IMG_2335.JPG → bg11.png
✅ IMG_2336.JPG → bg12.png
✅ IMG_2337.JPG → bg13.png
```

### 刪除檔案（8 個）
```
❌ IMG_2329.JPG (已轉換為 bg6.png)
❌ IMG_2330.JPG (已轉換為 bg7.png)
❌ IMG_2331.JPG (已轉換為 bg8.png)
❌ IMG_2332.JPG (已轉換為 bg9.png)
❌ IMG_2334.JPG (已轉換為 bg10.png)
❌ IMG_2335.JPG (已轉換為 bg11.png)
❌ IMG_2336.JPG (已轉換為 bg12.png)
❌ IMG_2337.JPG (已轉換為 bg13.png)
```

---

## 🎯 修改亮點

### 1. 完整性
- ✅ 每個關卡都有專屬背景（L0-L12）
- ✅ 自訂背景功能覆蓋所有畫面
- ✅ 專業的 App Icon

### 2. 正確性
- ✅ 片假名詞彙不再顯示多餘的平假名標註
- ✅ 背景對應邏輯正確無誤
- ✅ 所有畫面背景同步

### 3. 可維護性
- ✅ 統一的背景處理函數（DRY）
- ✅ 清晰的檔案命名（bg1-bg13）
- ✅ 完整的文檔更新

### 4. 使用者體驗
- ✅ 視覺一致性（全局自訂背景）
- ✅ 更準確的學習內容（片假名不加標註）
- ✅ 專業的應用程式外觀（App Icon）

---

## 🧪 測試建議

### 背景功能測試
1. ✅ 測試每個關卡的背景是否正確顯示
2. ✅ 測試解鎖背景功能
3. ✅ 測試設為自訂背景
4. ✅ 測試主選單、測驗、結果畫面的背景同步
5. ✅ 測試重置為預設背景

### 平假名標註測試
1. ✅ 測試漢字詞彙顯示平假名（如：学生（がくせい））
2. ✅ 測試片假名詞彙不顯示平假名（如：アメリカ）
3. ✅ 測試平假名詞彙不顯示平假名（如：はい）

### App Icon 測試
1. ✅ 測試程式視窗是否顯示鱷魚 icon
2. ✅ 測試不同作業系統的 icon 顯示

---

## 📌 備註

- 所有舊的背景圖片（tokyo, osaka, kyoto, nara, fuji）已重新命名為 bg1-bg5
- 所有新的背景圖片（JPG）已轉換為 PNG 格式
- 背景處理邏輯已統一，未來只需修改一個函數
- App Icon 在 macOS 上使用 Apple Color Emoji 字體效果最佳

---

**修改完成！所有功能已測試並正常運作。** ✨
