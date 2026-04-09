@echo off
REM 科技晚报生成器 - 使用 Tavily 搜索真实新闻
REM 每天19:00执行

echo 🔍 正在搜索今日科技新闻...

REM 创建新闻目录（如果不存在）
if not exist "X:\小红书科技新闻" mkdir "X:\小红书科技新闻"

REM 获取当前日期
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)

REM 使用 OpenClaw 调用 tavily-search skill
echo 📰 搜索 AI 新闻...
openclaw run tavily-search "人工智能 最新新闻 今日" > "X:\小红书科技新闻\%mydate%_raw.txt"

echo ✅ 新闻搜索完成！
echo 📁 原始数据保存至: X:\小红书科技新闻\%mydate%_raw.txt

REM 生成小红书文案（简化版）
echo 📝 正在生成小红书文案...
