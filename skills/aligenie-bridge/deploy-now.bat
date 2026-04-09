@echo off
echo ==========================================
echo 🚀 天猫精灵桥接服务 - Vercel 部署
echo ==========================================
echo.
echo 步骤 1: 登录 Vercel
echo ------------------------
echo 请在打开的浏览器中登录你的 Vercel 账号
echo.
pause
vercel login
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 登录失败，请重试
    pause
    exit /b 1
)

echo.
echo ==========================================
echo 步骤 2: 部署到 Vercel
echo ------------------------
echo.
cd /d C:\Users\shenz\.openclaw\workspace\skills\aligenie-bridge
vercel --prod

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 部署失败
    pause
    exit /b 1
)

echo.
echo ==========================================
echo ✅ 部署完成！
echo ==========================================
echo.
echo 你的服务已上线！
echo.
echo 📍 访问地址：https://YOUR-PROJECT.vercel.app
echo 🔍 健康检查：https://YOUR-PROJECT.vercel.app/health
echo 📡 Webhook: POST https://YOUR-PROJECT.vercel.app/aligenie
echo.
echo ⚠️  重要提示：
echo 1. 将上面的 Webhook URL 配置到天猫精灵开放平台
echo 2. 如果需要连接真实的 OpenClaw，在 Vercel 设置环境变量 OPENCLAW_URL
echo 3. 测试 Webhook: curl -X POST https://YOUR-PROJECT.vercel.app/aligenie
echo.
echo 📋 下一步：
echo 1. 访问 https://iap.aligenie.com
echo 2. 创建技能 → 标准技能 → 云端服务透传
echo 3. Webhook URL 填写上面的地址
echo 4. 配置意图并提交审核
echo.
pause
