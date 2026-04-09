@echo off
chcp 65001 >nul
title 翻身文件箱 - 打包工具

echo ====================================
echo     📦 翻身文件箱 - 打包工具
echo ====================================
echo.
echo 正在安装打包工具...
echo.

pip install pyinstaller -q

echo.
echo 开始打包...
echo.

pyinstaller --onefile --windowed ^
    --name "翻身文件箱" ^
    --icon=icon.ico ^
    --add-data "converter.py;." ^
    --hidden-import PIL ^
    --hidden-import hashlib ^
    main_v2.py

echo.
echo ====================================
if exist "dist\翻身文件箱.exe" (
    echo ✅ 打包成功！
    echo.
    echo 📦 输出位置：dist\翻身文件箱.exe
    echo.
    echo 正在复制到当前目录...
    copy /Y "dist\翻身文件箱.exe" .
    echo.
    echo ✅ 完成！
    echo.
    echo 现在可以运行 "翻身文件箱.exe" 启动软件
) else (
    echo ❌ 打包失败
    echo 请检查错误信息
)
echo ====================================
echo.
pause
