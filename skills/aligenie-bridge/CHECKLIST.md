# 📋 天猫精灵部署检查清单

## ✅ 准备阶段

- [ ] 代码已测试通过（14 个测试用例全部 ✅）
- [ ] 已创建 vercel.json 配置 ✅
- [ ] 已创建 .gitignore ✅
- [ ] 已创建 deploy-vercel.bat 脚本 ✅
- [ ] 已创建 README.md 部署指南 ✅
- [ ] 已创建 DEPLOY.md 详细文档 ✅
- [ ] server.js 已支持 Vercel ✅

---

## 🚀 部署到 Vercel（推荐）

### 步骤 1: 安装 Vercel CLI
```bash
npm install -g vercel
```

### 步骤 2: 登录 Vercel
```bash
vercel login
```

### 步骤 3: 部署
```bash
cd C:\Users\shenz\.openclaw\workspace\skills\aligenie-bridge
vercel --prod
```

### 步骤 4: 记录域名
```
✅ https://your-project.vercel.app
```

---

## 🔗 配置天猫精灵开放平台

### 1. 注册开发者账号
- [ ] 访问 https://iap.aligenie.com
- [ ] 注册/登录开发者账号

### 2. 创建技能
- [ ] 控制台 → 创建技能
- [ ] 选择"标准技能"
- [ ] 选择"云端服务透传"模板
- [ ] 填写技能名称（如：OpenClaw 智能助手）
- [ ] 填写技能描述

### 3. 配置 Webhook
- [ ] Webhook URL: `https://your-project.vercel.app/aligenie`
- [ ] 请求类型：POST
- [ ] Content-Type: application/json

### 4. 配置意图（Intent）
添加以下意图：

| 意图名称 | 说明 | 示例语句 |
|---------|------|---------|
| `weather_query` | 天气查询 | 查一下北京天气 |
| `schedule_create` | 创建日程 | 提醒我下午三点开会 |
| `schedule_query` | 查询日程 | 查看我的日程 |
| `monitor_check` | 监控检查 | DeepSeek 有新模型吗 |
| `message_send` | 发送消息 | 给 Jake 发消息 |
| `todo_create` | 创建待办 | 创建一个待办 |
| `todo_list` | 查询待办 | 查看我的待办 |
| `news_query` | 查询新闻 | 今天有什么新闻 |
| `general_chat` | 通用聊天 | 你好 |

### 5. 配置槽位（Slots）
- [ ] city（城市）- 用于天气查询
- [ ] time（时间）- 用于日程创建
- [ ] content（内容）- 用于日程/待办
- [ ] recipient（收件人）- 用于发消息

### 6. 真机测试
- [ ] 下载天猫精灵 APP
- [ ] 绑定测试账号
- [ ] 语音测试各意图
- [ ] 检查 Webhook 日志

### 7. 提交审核
- [ ] 填写技能信息
- [ ] 上传技能图标
- [ ] 提交审核
- [ ] 等待审核通过（1-3 个工作日）

---

## 🧪 测试清单

### 本地测试
- [ ] `npm start` 启动服务
- [ ] `node test-simple.js` 简单测试
- [ ] `node test-all.js` 完整测试（14 个用例）
- [ ] 所有测试通过 ✅

### 部署后测试
- [ ] `curl https://your-project.vercel.app/health` 健康检查
- [ ] `curl -X POST https://your-project.vercel.app/aligenie` Webhook 测试
- [ ] 天猫精灵 APP 语音测试

### 功能测试
- [ ] 天气查询：「查一下北京天气」
- [ ] 创建日程：「提醒我下午三点开会」
- [ ] 监控检查：「DeepSeek 有新模型吗」
- [ ] 发送消息：「给 Jake 发消息」
- [ ] 创建待办：「创建一个待办：买牛奶」
- [ ] 查询待办：「查看我的待办列表」
- [ ] 查询新闻：「今天有什么科技新闻」
- [ ] 通用聊天：「你好」「谢谢你」「你会做什么」

---

## 🔧 环境变量配置（可选）

如果连接真实的 OpenClaw Gateway：

### Vercel 环境变量
- [ ] Vercel 控制台 → Project Settings → Environment Variables
- [ ] 添加 `OPENCLAW_URL` = `http://your-server-ip:18789`
- [ ] 重新部署：`vercel --prod`

### 同一服务器部署
- [ ] OpenClaw Gateway 和 Webhook 部署在同一服务器
- [ ] 配置 `OPENCLAW_URL=http://localhost:18789`
- [ ] 内网通信，无需公网 IP

---

## 📊 监控和维护

### 日常检查
- [ ] Vercel Dashboard 查看使用量
- [ ] 检查错误日志
- [ ] 监控响应时间（应 < 5 秒）

### Vercel 日志
```bash
vercel logs your-project
```

### PM2 日志（自部署）
```bash
pm2 logs aligenie-bridge
```

### Nginx 日志（自部署）
```bash
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## 💰 成本统计

### Vercel 方案（推荐）
| 项目 | 成本 |
|------|------|
| 服务器 | 免费 |
| 域名（可选） | ¥50/年 |
| SSL 证书 | 免费 |
| **总计** | **¥0-50/年** |

### 阿里云方案
| 项目 | 成本 |
|------|------|
| 服务器（1 核 1G） | ¥60/月 |
| 域名 | ¥50/年 |
| SSL 证书 | 免费 |
| **总计** | **¥770/年** |

---

## ⚠️ 注意事项

### 必须项
- [ ] Webhook 必须是 HTTPS ✅（Vercel 自动提供）
- [ ] 响应时间 < 5 秒 ✅（当前平均 3 秒）
- [ ] 意图名称匹配 ✅

### 可选项
- [ ] 自定义域名（更专业）
- [ ] 连接真实 OpenClaw（完整功能）
- [ ] 添加更多意图（扩展功能）

---

## 🎯 完成标志

全部完成后，你应该能够：

✅ 对天猫精灵说：「查一下北京天气」→ 返回天气信息
✅ 对天猫精灵说：「提醒我下午三点开会」→ 创建日程
✅ 对天猫精灵说：「DeepSeek 有新模型吗」→ 检查监控
✅ 对天猫精灵说：「给 Jake 发消息」→ 发送企业微信消息

---

## 📞 遇到问题？

### 常见错误

**错误 1: Webhook 超时**
- 检查 Vercel 部署状态
- 查看日志：`vercel logs`
- 确保响应时间 < 5 秒

**错误 2: 意图不匹配**
- 检查意图名称是否一致
- 检查槽位配置
- 重新训练语义模型

**错误 3: 审核不通过**
- 检查技能描述是否完整
- 确保有测试账号
- 联系客服咨询

---

**祝你部署顺利！** 🎉

有任何问题随时问我！👻
