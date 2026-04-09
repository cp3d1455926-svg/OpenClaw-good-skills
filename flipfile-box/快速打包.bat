@echo off
chcp 65001 >nul
title 翻身文件箱 - 快速打包

echo ====================================
echo     📦 快速打包（无图标版）
echo ====================================
echo.

echo 正在安装 PyInstaller...
pip install pyinstaller -q

echo.
echo 正在打包...
echo.

pyinstaller --onefile --windowed --name "翻身文件箱" main_v2.py

echo.
if exist "dist\翻身文件箱.exe" (
    echo ✅ 打包成功！
    echo.
    echo 📦 位置：dist\翻身文件箱.exe
    echo.
    copy /Y "dist\翻身文件箱.exe" .
    echo ✅ 已复制到当前目录
) else (
    echo ❌ 打包失败
)
echo.
pause
