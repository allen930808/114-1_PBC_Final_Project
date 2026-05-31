@echo off
chcp 65001 >nul
echo ====================================
echo Wani-Doko! 自動打包腳本
echo ====================================
echo.

echo [1/4] 檢查 PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller 未安裝，正在安裝...
    pip install pyinstaller
) else (
    echo ✓ PyInstaller 已安裝
)
echo.

echo [2/4] 清理舊的建置檔案...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo ✓ 清理完成
echo.

echo [3/4] 開始打包（這可能需要 3-5 分鐘）...
pyinstaller Wani-Doko.spec --clean
echo.

if errorlevel 1 (
    echo ✗ 打包失敗！請查看上方錯誤訊息
    pause
    exit /b 1
)

echo [4/4] 打包完成！
echo.
echo ====================================
echo 執行檔位置：dist\Wani-Doko\Wani-Doko.exe
echo ====================================
echo.
echo 接下來的步驟：
echo 1. 測試執行檔：雙擊 dist\Wani-Doko\Wani-Doko.exe
echo 2. 壓縮資料夾：右鍵點擊 dist\Wani-Doko 資料夾 → 傳送到 → 壓縮的資料夾
echo 3. 分享給組員：上傳壓縮檔到 Google Drive 或 GitHub Releases
echo.
pause
