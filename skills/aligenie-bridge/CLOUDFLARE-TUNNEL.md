# 🌩️ Cloudflare Tunnel 部署指南

## 🎯 目标

使用 Cloudflare Tunnel 将本地 OpenClaw Gateway 和 Webhook 服务暴露到公网，实现天猫精灵同步回复。

---

## 📋 前提条件

- [x] 本地 OpenClaw Gateway 已安装
- [x] Webhook 服务已配置
- [ ] Cloudflare 账号（免费）
- [ ] 域名（可选，可用免费域名）

---

## 🚀 快速开始

### 步骤 1: 注册 Cloudflare 账号

访问 https://dash.cloudflare.com/sign-up 注册免费账号

### 步骤 2: 安装 cloudflared

```bash
# 方式 1: 使用 npm（推荐）
npm install -g @cloudflare/cloudflared

# 方式 2: Windows 直接下载
# 访问 https://github.com/cloudflare/cloudflared/releases
# 下载 cloudflared-windows-amd64.exe
# 重命名为 cloudflared.exe 并放到 PATH 目录
```

### 步骤 3: 登录 Cloudflare

```bash
cloudflared tunnel login
```

这会打开浏览器让你登录 Cloudflare 账号

### 步骤 4: 创建隧道

```bash
cloudflared tunnel create openclaw
```

输出示例：
```
Created tunnel openclaw with id xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### 步骤 5: 配置隧道

创建配置文件 `C:\Users\shenz\.cloudflared\config.yml`:

```yaml
tunnel: openclaw
credentials-file: C:\Users\shenz\.cloudflared\xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.json

ingress:
  # OpenClaw Gateway
  - hostname: openclaw.your-domain.com
    service: http://localhost:18789
  
  # Webhook 服务
  - hostname: webhook.your-domain.com
    service: http://localhost:3000
  
  # 默认规则（404）
  - service: http_status:404
```

**如果没有域名：**
- 使用 Cloudflare 免费域名：`your-name.trycloudflare.com`
- 或者使用 ngrok（见下方备选方案）

### 步骤 6: 启动隧道

```bash
# 方式 1: 前台运行（测试用）
cloudflared tunnel run openclaw

# 方式 2: Windows 服务（生产用）
cloudflared service install
net start cloudflared
```

### 步骤 7: 配置 DNS

如果使用自定义域名：
```bash
cloudflared tunnel route dns openclaw openclaw.your-domain.com
cloudflared tunnel route dns openclaw webhook.your-domain.com
```

如果使用免费域名：
```
openclaw.trycloudflare.com
webhook.trycloudflare.com
```

---

## 🔧 修改 server.js

设置 `OPENCLAW_URL` 环境变量：

```bash
# Windows PowerShell
$env:OPENCLAW_URL = "https://openclaw.your-domain.com"

# 或在 ecosystem.config.js 中配置
module.exports = {
  apps: [{
    name: 'aligenie-bridge',
    script: 'server.js',
    env: {
      OPENCLAW_URL: 'https://openclaw.your-domain.com',
      PORT: 3000
    }
  }]
};
```

---

## 🧪 测试

### 测试 OpenClaw Gateway
```bash
curl https://openclaw.your-domain.com/health
```

### 测试 Webhook
```bash
curl -X POST https://webhook.your-domain.com/aligenie \
  -H "Content-Type: application/json" \
  -d '{"header":{"name":"IntentRequest"},"payload":{"intent":"general_chat","query":"你好"}}'
```

---

## 📊 完整架构

```
天猫精灵 → Cloudflare CDN → Cloudflare Tunnel → 本地服务
                              ↓
                      ┌───────────────┐
                      │ 你的电脑       │
                      ├───────────────┤
                      │ :18789        │
                      │ OpenClaw      │
                      │               │
                      │ :3000         │
                      │ Webhook       │
                      └───────────────┘
```

---

## 💰 成本

| 项目 | 成本 |
|------|------|
| Cloudflare Tunnel | 免费 |
| Cloudflare 域名 | 免费（trycloudflare.com） |
| 自定义域名（可选） | ¥50/年 |
| **总计** | **¥0-50/年** |

---

## ⚠️ 注意事项

### 带宽限制
- 免费版：无限制（合理使用）
- 免费版不支持 TCP，只支持 HTTP/HTTPS/WebSocket

### 延迟
- 国内访问 Cloudflare 约 50-150ms
- 天猫精灵响应时间：3-5 秒（符合 5 秒要求）

### 安全性
- ✅ 不需要暴露公网 IP
- ✅ 自动 HTTPS
- ✅ Cloudflare DDoS 防护
- ✅ 可以配置访问规则

---

## 🔄 开机自启

### Windows 服务方式

```bash
# 安装服务
cloudflared service install

# 启动服务
net start cloudflared

# 停止服务
net stop cloudflared

# 查看状态
sc query cloudflared
```

### Task Scheduler 方式

创建任务计划程序：
- 触发器：开机时
- 操作：`cloudflared tunnel run openclaw`
- 条件：只在 AC 电源时运行

---

## 🎯 备选方案：ngrok（如果没有域名）

如果不想配置 Cloudflare，可以用 ngrok：

### 安装 ngrok

```bash
# 访问 https://ngrok.com 注册并下载
# 或使用 npm
npm install -g ngrok
```

### 启动隧道

```bash
# 终端 1: OpenClaw Gateway
ngrok http 18789 --log=stdout

# 终端 2: Webhook 服务
ngrok http 3000 --log=stdout
```

### 获得地址

```
OpenClaw: https://abc123.ngrok.io
Webhook:  https://xyz789.ngrok.io
```

### 修改 server.js

```javascript
const OPENCLAW_URL = 'https://abc123.ngrok.io';
```

**缺点：** URL 每次重启会变

---

## 📋 部署检查清单

- [ ] Cloudflare 账号已注册
- [ ] cloudflared 已安装
- [ ] 隧道已创建
- [ ] 配置文件已创建
- [ ] DNS 已配置
- [ ] 隧道已启动
- [ ] OPENCLAW_URL 已设置
- [ ] 本地测试通过
- [ ] 公网测试通过
- [ ] 天猫精灵配置完成

---

## 🎉 完成后的效果

**你说：** "天猫精灵，查一下北京天气"

**等待 3-5 秒**

**天猫精灵回复：** "北京市今天晴转多云，气温 15-25°C，空气质量良好。"

---

## 📞 遇到问题？

### 常见问题

**Q: tunnel login 无法打开浏览器？**
- 手动访问 https://dash.cloudflare.com
- 登录后复制认证码
- 粘贴到终端

**Q: 域名无法解析？**
- 检查 DNS 配置
- 等待 DNS 传播（5-10 分钟）
- 使用 `nslookup your-domain.com` 检查

**Q: 隧道无法连接？**
- 检查防火墙
- 确认本地服务已启动
- 查看 cloudflared 日志

---

**准备好开始了吗？** 运行第一条命令：`npm install -g @cloudflare/cloudflared` 🚀

有任何问题随时问我！👻
