@echo off
echo 🚀 天猫精灵桥接服务 - Vercel 一键部署脚本
echo ==========================================
echo.

REM 检查 Vercel CLI 是否安装
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Vercel CLI 未安装
    echo.
    echo 正在安装...
    npm install -g vercel
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ 安装失败，请手动执行：npm install -g vercel
        pause
        exit /b 1
    )
)

echo ✅ Vercel CLI 已安装
echo.

REM 登录 Vercel
echo 📝 登录 Vercel...
vercel login
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 登录失败
    pause
    exit /b 1
)

echo ✅ 登录成功
echo.

REM 部署
echo 🚀 开始部署...
echo.
vercel --prod

if %ERRORLEVEL% NEQ 0 (
    echo ❌ 部署失败
    pause
    exit /b 1
)

echo.
echo ==========================================
echo ✅ 部署完成！
echo.
echo 📍 你的服务已上线
echo 🌐 访问地址：https://YOUR_PROJECT.vercel.app
echo 🔍 健康检查：https://YOUR_PROJECT.vercel.app/health
echo 📡 Webhook: POST https://YOUR_PROJECT.vercel.app/aligenie
echo.
echo ⚠️  重要提示：
echo 1. 将 Webhook URL 配置到天猫精灵开放平台
echo 2. 配置 OPENCLAW_URL 环境变量（如果需要连接真实的 OpenClaw）
echo 3. 测试 Webhook: curl -X POST https://YOUR_PROJECT.vercel.app/aligenie
echo.
pause
