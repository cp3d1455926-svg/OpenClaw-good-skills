# ✅ 部署成功！

## 📍 服务地址

**生产环境 URL：**
```
https://aligenie-bridge.vercel.app
```

## 🔗 重要链接

| 用途 | URL |
|------|-----|
| **Webhook** | `https://aligenie-bridge.vercel.app/aligenie` |
| **健康检查** | `https://aligenie-bridge.vercel.app/health` |
| **Vercel 控制台** | https://vercel.com/cp3d1455926-4819s-projects/aligenie-bridge |

## 📋 下一步：配置天猫精灵

1. **访问** https://iap.aligenie.com
2. **登录** 天猫精灵开放平台
3. **创建技能**
   - 控制台 → 创建技能
   - 选择"标准技能" → "云端服务透传"
4. **配置 Webhook**
   ```
   Webhook URL: https://aligenie-bridge.vercel.app/aligenie
   请求类型：POST
   Content-Type: application/json
   ```
5. **配置意图**（9 个）
   - weather_query
   - schedule_create
   - schedule_query
   - monitor_check
   - message_send
   - todo_create
   - todo_list
   - news_query
   - general_chat
6. **测试发布**
   - 真机测试
   - 提交审核

## 🧪 测试命令

```bash
# 测试健康检查
curl https://aligenie-bridge.vercel.app/health

# 测试 Webhook
curl -X POST https://aligenie-bridge.vercel.app/aligenie \
  -H "Content-Type: application/json" \
  -d "{\"header\":{\"name\":\"IntentRequest\"},\"payload\":{\"intent\":\"general_chat\",\"query\":\"你好\"}}"
```

## ⚠️ 注意事项

1. **国内访问 Vercel 可能较慢** - 这是正常的，天猫精灵服务器可以正常访问
2. **OpenClaw 连接** - 当前是文件模式，如需连接真实 OpenClaw，需要在 Vercel 设置环境变量 `OPENCLAW_URL`
3. **日志查看** - https://vercel.com/cp3d1455926-4819s-projects/aligenie-bridge → Deployments → 查看日志

## 🎉 恭喜！

你的服务已经部署成功，可以开始配置天猫精灵了！
