# 🎨 自訂背景功能使用說明

## 功能概述

解鎖關卡後，可以將解鎖的背景圖片設為主選單背景。

## 使用步驟

### 1. 解鎖背景

- 完成任一關卡測驗，正確率達 80% 以上
- 會自動解鎖該關卡的背景圖片

### 2. 設定背景

1. 在主選單點擊「🗾 解鎖背景」
2. 點擊已解鎖的關卡（有 🌸 圖示的卡片）
3. 點擊「觀看小知識與背景」
4. 點擊「🎨 設為背景」按鈕
5. 點擊確定後，返回主選單查看效果

### 3. 恢復預設背景

- 在主選單點擊「🔄 預設背景」按鈕（僅在有自訂背景時顯示）
- 點擊確定後，進入其他畫面再返回主選單即可看到預設漸層背景

## 可用背景

| 背景名稱 | 對應關卡 | 主題 |
|---------|---------|------|
| Tokyo | L0, L3, L5, L7, L12 | 東京都市景觀 |
| Osaka | L1, L4, L8 | 大阪街景 |
| Kyoto | L2, L9 | 京都古都風情 |
| Nara | L6, L10 | 奈良鹿與神社 |
| Fuji | L11 | 富士山聖山 |

## 技術說明

- 背景設定儲存在 `config.json` 的 `custom_background` 欄位
- 使用 PIL 圖片處理：調整亮度 1.5 倍 + 半透明白色遮罩
- 確保文字在任何背景上都清晰可讀

## 故障排除

### 問題：背景無法顯示

**可能原因**：
1. 圖片檔案不存在
2. 圖片格式錯誤
3. PIL/Pillow 未安裝

**解決方法**：
```bash
# 檢查圖片是否存在
ls -la assets/backgrounds/

# 重新安裝 Pillow
pip install --upgrade Pillow

# 手動清除設定
# 編輯 config.json，將 "custom_background" 改為 null
```

### 問題：設為背景後主選單變空白

**原因**：已修正（v1.1.1）

**解決方法**：
- 更新到最新版本
- 或手動清除：編輯 `config.json`，設 `"custom_background": null`

### 問題：重置背景後沒有變化

**說明**：需要重新進入主選單才會生效

**操作**：
1. 點擊「成績紀錄」或「解鎖背景」
2. 再點擊返回主選單
3. 或重新啟動程式

## 開發者資訊

### 背景處理流程

```python
1. 載入圖片: Image.open('assets/backgrounds/{name}.png')
2. 調整大小: resize((900, 650))
3. 增加亮度: ImageEnhance.Brightness(img).enhance(1.5)
4. 轉換模式: convert('RGBA')
5. 混合遮罩: Image.alpha_composite(img, white_overlay)
6. 轉換顯示: ImageTk.PhotoImage(img)
```

### 漸層背景繪製

```python
# 50 步漸層從 #EEF2FF 到 #E0E7FF
for i in range(50):
    ratio = i / 50
    color = interpolate(top_color, bot_color, ratio)
    canvas.create_rectangle(...)
```

---

**最後更新**: 2026-05-31
