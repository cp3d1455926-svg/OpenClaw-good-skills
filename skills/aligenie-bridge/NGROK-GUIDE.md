# 🚀 Ngrok 快速部署指南

## 🎯 目标

使用 ngrok 将本地 OpenClaw 暴露到公网，实现天猫精灵同步回复。

---

## 📋 步骤

### 步骤 1: 注册 ngrok 账号

访问 https://ngrok.com/signup 注册免费账号

### 步骤 2: 获取 Authtoken

登录后访问 https://dashboard.ngrok.com/get-started/your-authtoken
复制你的 Authtoken

### 步骤 3: 安装 ngrok

```bash
# 方式 1: 使用 npm（推荐）
npm install -g ngrok

# 方式 2: Windows 直接下载
# 访问 https://ngrok.com/download
# 下载并解压到 C:\ngrok\
```

### 步骤 4: 配置 Authtoken

```bash
ngrok config add-authtoken YOUR_AUTHTOKEN
```

### 步骤 5: 启动隧道

**方式 A: 启动两个独立隧道**

终端 1（OpenClaw Gateway）:
```bash
ngrok http 18789 --log=stdout
```

终端 2（Webhook 服务）:
```bash
ngrok http 3000 --log=stdout
```

**方式 B: 使用配置文件（推荐）**

创建 `C:\ngrok\ngrok.yml`:

```yaml
version: "2"
authtoken: YOUR_AUTHTOKEN

tunnels:
  openclaw:
    proto: http
    addr: 18789
    hostname: openclaw.ngrok-free.app
  
  webhook:
    proto: http
    addr: 3000
    hostname: webhook.ngrok-free.app
```

启动:
```bash
ngrok start --all --config C:\ngrok\ngrok.yml
```

### 步骤 6: 获得公网地址

启动后你会看到:
```
Forwarding: https://openclaw.ngrok-free.app -> http://localhost:18789
Forwarding: https://webhook.ngrok-free.app -> http://localhost:3000
```

### 步骤 7: 修改 server.js

设置环境变量:

**PowerShell:**
```powershell
$env:OPENCLAW_URL = "https://openclaw.ngrok-free.app"
```

**或修改 ecosystem.config.js:**
```javascript
module.exports = {
  apps: [{
    name: 'aligenie-bridge',
    script: 'server.js',
    env: {
      OPENCLAW_URL: 'https://openclaw.ngrok-free.app',
      PORT: 3000
    }
  }]
};
```

---

## 🧪 测试

### 测试 OpenClaw Gateway
```bash
curl https://openclaw.ngrok-free.app/health
```

### 测试 Webhook
```bash
curl -X POST https://webhook.ngrok-free.app/aligenie \
  -H "Content-Type: application/json" \
  -d '{"header":{"name":"IntentRequest"},"payload":{"intent":"general_chat","query":"你好"}}'
```

---

## 💰 成本

| 项目 | 免费版 | 付费版 |
|------|--------|--------|
| 隧道数量 | 1 个 | 不限 |
| 带宽 | 40GB/月 | 不限 |
| 自定义域名 | ❌ | ✅ |
| 静态 URL | ❌ | ✅ |
| **推荐** | **测试用** | **生产用** |

**免费版限制：**
- URL 每次重启会变（除非付费买静态 URL）
- 40GB/月带宽（个人用足够）
- 只有 1 个隧道（可以用 --url 参数绕过）

---

## 🔄 开机自启

### Windows 任务计划程序

1. 打开"任务计划程序"
2. 创建基本任务
3. 名称：ngrok-tunnel
4. 触发器：开机时
5. 操作：启动程序
   - 程序：`C:\ngrok\ngrok.exe`
   - 参数：`start --all --config C:\ngrok\ngrok.yml`
   - 起始于：`C:\ngrok\`
6. 完成

---

## ⚠️ 注意事项

### URL 变化问题

**免费版 ngrok：**
- 每次重启 ngrok，URL 都会变化
- 需要重新配置天猫精灵 Webhook URL

**解决方案：**
1. 付费购买静态 URL（$8/月）
2. 或者每次重启后更新天猫精灵配置
3. 或者使用 Cloudflare Tunnel（免费 + 固定域名）

### 带宽限制

- 免费版：40GB/月
- 监控用量：https://dashboard.ngrok.com/usage

### 延迟

- 国内访问 ngrok：约 100-200ms
- 天猫精灵响应时间：3-5 秒（符合要求）

---

## 🎯 完整流程

```
1. 启动 OpenClaw Gateway
   openclaw gateway --port 18789

2. 启动 Webhook 服务
   cd skills/aligenie-bridge
   npm start

3. 启动 ngrok
   ngrok start --all --config C:\ngrok\ngrok.yml

4. 复制 URL
   OpenClaw: https://xxxx.ngrok-free.app
   Webhook:  https://yyyy.ngrok-free.app

5. 设置环境变量
   $env:OPENCLAW_URL = "https://xxxx.ngrok-free.app"

6. 测试
   curl https://yyyy.ngrok-free.app/aligenie

7. 配置天猫精灵
   Webhook URL: https://yyyy.ngrok-free.app/aligenie
```

---

## 📊 与 Cloudflare Tunnel 对比

| 特性 | Ngrok | Cloudflare Tunnel |
|------|-------|-------------------|
| 安装难度 | ⭐⭐ | ⭐⭐⭐ |
| 配置复杂度 | ⭐ | ⭐⭐ |
| URL 稳定性 | ❌（免费） | ✅ |
| 带宽限制 | 40GB/月 | 无限制 |
| 国内速度 | 一般 | 较好 |
| 推荐场景 | 快速测试 | 长期使用 |

---

## 🎉 快速开始（5 分钟）

```bash
# 1. 安装 ngrok
npm install -g ngrok

# 2. 配置 authtoken
ngrok config add-authtoken YOUR_TOKEN

# 3. 启动隧道
ngrok http 18789
ngrok http 3000

# 4. 复制 URL 并配置
# 完成！
```

---

## 📞 遇到问题？

### Q: ngrok 命令找不到？
**A:** 确保 ngrok 已添加到 PATH，或使用完整路径

### Q: 隧道无法连接？
**A:** 检查本地服务是否已启动（18789 和 3000 端口）

### Q: URL 访问超时？
**A:** 检查防火墙，确保本地服务允许外部访问

---

**准备好开始了吗？** 

1. 访问 https://ngrok.com/signup 注册
2. 复制 Authtoken
3. 运行：`ngrok config add-authtoken YOUR_TOKEN`
4. 启动：`ngrok http 18789`

有任何问题随时问我！👻
