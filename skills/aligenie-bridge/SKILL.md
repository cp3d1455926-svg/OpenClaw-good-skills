---
name: aligenie-bridge
description: 天猫精灵 × OpenClaw 智能桥接服务。让天猫精灵通过语音调用 OpenClaw skills。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node"], "npm": ["express", "axios", "cors", "body-parser"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": ".",
              "label": "Install AliGenie Bridge (npm)",
              "workdir": "skills/aligenie-bridge",
            },
          ],
      },
  }
---

# AliGenie Bridge - 天猫精灵 × OpenClaw 桥接

让天猫精灵通过语音调用 OpenClaw 的 skills！

## 🚀 快速开始

### 1. 安装依赖

```bash
cd skills/aligenie-bridge
npm install
```

### 2. 启动服务

```bash
npm start
```

### 3. 测试 Webhook

```bash
curl -X POST http://localhost:3000/aligenie \
  -H "Content-Type: application/json" \
  -d '{
    "header": {"name": "IntentRequest"},
    "payload": {
      "intent": "general_chat",
      "query": "查询北京天气"
    }
  }'
```

## 📐 架构

```
天猫精灵 → 天猫精灵云平台 → Webhook 服务 → OpenClaw Gateway → Skills
```

## 🎤 支持的语音指令

| 意图 | 语音示例 | 触发的 Skill |
|------|---------|-------------|
| `weather_query` | "查一下北京天气" | weather |
| `schedule_create` | "提醒我下午三点开会" | cron-mastery |
| `monitor_check` | "DeepSeek 有新模型吗" | auto-monitor |
| `message_send` | "给 Jake 发消息" | wecom-msg |
| `todo_create` | "创建一个待办" | wecom-edit-todo |
| `general_chat` | 任意对话 | OpenClaw 默认 |

## 🔧 配置

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PORT` | 3000 | Webhook 服务端口 |
| `OPENCLAW_URL` | http://127.0.0.1:18789 | OpenClaw Gateway 地址 |

### 天猫精灵开放平台配置

1. 登录 https://iap.aligenie.com
2. 创建技能 → 标准技能 → 云端服务透传
3. 配置 Webhook URL：`https://your-domain.com/aligenie`
4. 配置意图和槽位
5. 提交审核

## 📁 文件结构

```
skills/aligenie-bridge/
├── server.js          # 主服务
├── package.json       # 依赖配置
├── SKILL.md          # 技能文档
└── README.md         # 详细说明
```

## 🧪 本地测试

使用 `test-webhook.js` 脚本模拟天猫精灵请求：

```bash
node test-webhook.js "查询天气"
```

## 🌐 部署到公网

### 方案 A: 阿里云/腾讯云

1. 购买云服务器（ECS/CVM）
2. 安装 Node.js
3. 部署服务
4. 配置 Nginx 反向代理 + HTTPS

### 方案 B: Vercel/Netlify（免费）

1. 部署到 Vercel
2. 自动获得 HTTPS 域名
3. 配置环境变量

### 方案 C: ngrok（临时测试）

```bash
ngrok http 3000
```

获得临时 HTTPS 地址用于测试。

## 📝 注意事项

1. **响应时间**：天猫精灵要求 5 秒内响应，超时需返回"正在处理"
2. **语音优化**：返回简洁、适合语音播放的文本
3. **错误处理**：优雅处理 OpenClaw 不可用的情况
4. **安全**：生产环境添加认证和限流

## 🤖 扩展

添加新意图：

1. 在 `buildOpenClawMessage()` 中添加意图映射
2. 在天猫精灵开放平台配置新意图
3. 测试并部署

## 📞 支持

遇到问题？查看文档：
- OpenClaw docs: `C:\Users\shenz\.openclaw\workspace\docs`
- 天猫精灵开放平台：https://iap.aligenie.com/docs

---

让天猫精灵变得更智能！👻
