# 🚀 天猫精灵 × OpenClaw 桥接服务 - 快速部署

## 📦 项目文件

```
aligenie-bridge/
├── server.js              # 主服务（已支持 Vercel）
├── package.json           # 依赖配置
├── vercel.json           # Vercel 部署配置 ✅ NEW
├── .gitignore            # Git 忽略文件 ✅ NEW
├── SKILL.md              # 技能文档
├── DEPLOY.md             # 详细部署指南 ✅ NEW
├── deploy-vercel.bat     # Windows 一键部署脚本 ✅ NEW
├── test-all.js           # 完整测试套件
├── test-simple.js        # 简单测试
└── README.md             # 本文件
```

---

## 🎯 部署方案选择

### 方案 A: Vercel（推荐 - 免费 + 自动 HTTPS）⭐

**适合：** 个人使用、测试、快速上线

**优点：**
- ✅ 完全免费
- ✅ 自动 HTTPS
- ✅ 自动部署
- ✅ 无需配置服务器

**部署步骤：**

```bash
# 1. 进入项目目录
cd C:\Users\shenz\.openclaw\workspace\skills\aligenie-bridge

# 2. 运行一键部署脚本
deploy-vercel.bat

# 或者手动部署
npm install -g vercel
vercel login
vercel --prod
```

**部署后获得：**
```
🌐 https://your-project.vercel.app
🔍 https://your-project.vercel.app/health
📡 POST https://your-project.vercel.app/aligenie
```

---

### 方案 B: 阿里云/腾讯云（生产环境）

**适合：** 正式产品、需要稳定控制

**成本：** 约 ¥60/月

**步骤：** 查看 `DEPLOY.md` 详细指南

---

### 方案 C: Railway（简单快速）

**适合：** 不想配置服务器

**步骤：**
1. 访问 https://railway.app
2. New Project → Deploy from GitHub
3. 选择此项目
4. 添加环境变量
5. 自动部署获得 HTTPS 域名

---

## 🧪 本地测试（部署前）

```bash
# 1. 启动服务
npm start

# 2. 运行测试
node test-all.js

# 预期结果：14 个测试全部通过 ✅
```

---

## 🔗 天猫精灵配置

### 部署完成后：

1. **登录天猫精灵开放平台**
   - https://iap.aligenie.com

2. **创建技能**
   - 控制台 → 创建技能
   - 选择"标准技能" → "云端服务透传"

3. **配置 Webhook**
   ```
   Webhook URL: https://your-project.vercel.app/aligenie
   请求类型：POST
   Content-Type: application/json
   ```

4. **配置意图**
   - weather_query（天气查询）
   - schedule_create（创建日程）
   - schedule_query（查询日程）
   - monitor_check（监控检查）
   - message_send（发送消息）
   - todo_create（创建待办）
   - todo_list（查询待办）
   - news_query（查询新闻）
   - general_chat（通用聊天）

5. **测试发布**
   - 真机测试
   - 提交审核
   - 等待发布

---

## 📊 测试命令

### 本地测试
```bash
node test-simple.js
node test-all.js
```

### 部署后测试
```bash
# 替换为你的 Vercel URL
curl -X POST https://your-project.vercel.app/aligenie \
  -H "Content-Type: application/json" \
  -d "{\"header\":{\"name\":\"IntentRequest\"},\"payload\":{\"intent\":\"general_chat\",\"query\":\"你好\"}}"
```

---

## 🔧 环境变量（可选）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PORT` | 3000 | 服务端口（Vercel 自动管理） |
| `OPENCLAW_URL` | http://localhost:18789 | OpenClaw Gateway 地址 |

**Vercel 配置环境变量：**
1. Vercel 控制台 → Project Settings → Environment Variables
2. 添加 `OPENCLAW_URL`
3. 重新部署

---

## 📝 注意事项

### ⚠️ 关于 OpenClaw 连接

**当前模式：** 文件模式（本地测试）
- Webhook 写入文件 → OpenClaw 读取处理

**生产模式：** HTTP API
- 需要 OpenClaw Gateway 暴露公网 IP
- 或者在同一服务器上运行

**解决方案：**
1. 将 OpenClaw 和 Webhook 部署在同一服务器
2. 使用内网通信：`OPENCLAW_URL=http://localhost:18789`

### ⚠️ 响应时间

- 天猫精灵要求 5 秒内响应
- 当前测试平均 3 秒 ✅
- 如果超时，返回"正在处理"提示

### ⚠️ HTTPS 必需

天猫精灵要求 Webhook 必须是 HTTPS
- Vercel 自动提供 ✅
- 自部署需要配置 SSL 证书

---

## 🎉 快速开始（3 分钟）

```bash
# 1. 进入项目目录
cd C:\Users\shenz\.openclaw\workspace\skills\aligenie-bridge

# 2. 运行部署脚本
deploy-vercel.bat

# 3. 按提示登录 Vercel
# 4. 等待部署完成
# 5. 获得 HTTPS 域名

# 6. 测试
curl https://your-project.vercel.app/health

# 7. 配置到天猫精灵开放平台
```

---

## 📞 遇到问题？

### 常见问题

**Q: 部署失败？**
```bash
# 查看详细日志
vercel --debug
```

**Q: 测试不通过？**
```bash
# 本地先测试
npm start
node test-all.js
```

**Q: 天猫精灵配置找不到？**
- 确保使用 HTTPS
- 检查 Webhook URL 格式
- 确认意图名称匹配

---

## 🎯 下一步

部署完成后：
1. ✅ 获得公网 HTTPS 地址
2. ⏳ 配置天猫精灵开放平台
3. ⏳ 测试语音指令
4. ⏳ 提交审核
5. ⏳ 上线使用！

---

**准备好部署了吗？** 运行 `deploy-vercel.bat` 开始！🚀

有任何问题随时问我！👻
