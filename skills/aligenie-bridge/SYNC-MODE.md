# 🚀 天猫精灵同步回复模式部署指南

## 🎯 目标

让天猫精灵**直接回复** OpenClaw 的处理结果，而不是异步通知。

---

## 📐 架构对比

### 当前模式（异步）
```
天猫精灵 → Vercel Webhook → 文件 → OpenClaw → 企业微信
   ↓                                        ↑
立即回复"收到"                              1 分钟后通知结果
```

### 同步模式（新）
```
天猫精灵 → 公网服务器 Webhook → OpenClaw Gateway → 天猫精灵
   ↓                                              ↑
   └────────────── 等待 3-5 秒直接回复 ─────────────┘
```

---

## 🔧 部署方案

### 方案 A: 阿里云/腾讯云（推荐）

**配置要求：**
- CPU: 2 核
- 内存：4GB
- 带宽：3Mbps+
- 系统：Ubuntu 20.04 或 Windows Server

**成本：** 约 ¥100-150/月

**步骤：**

#### 1. 购买服务器
- 阿里云 ECS 或 腾讯云 CVM
- 选择公网 IP
- 开放端口：80, 443, 18789

#### 2. 安装 OpenClaw Gateway
```bash
# SSH 登录服务器
ssh root@your-server-ip

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs npm

# 安装 OpenClaw
npm install -g openclaw

# 配置 OpenClaw
openclaw setup

# 启动 Gateway（端口 18789）
openclaw gateway --port 18789
```

#### 3. 部署 Webhook 服务
```bash
# 创建应用目录
mkdir -p /var/www/aligenie-bridge
cd /var/www/aligenie-bridge

# 上传代码
git clone <your-repo> .
# 或 scp 上传

# 安装依赖
npm install --production

# 配置环境变量
export OPENCLAW_URL=http://localhost:18789
export PORT=3000

# 安装 PM2
npm install -g pm2

# 启动服务
pm2 start server.js --name aligenie-bridge
pm2 save
pm2 startup
```

#### 4. 配置 Nginx 反向代理
```bash
# 安装 Nginx
apt install -y nginx

# 创建配置
cat > /etc/nginx/sites-available/aligenie << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location /aligenie {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 30s;
    }
}
EOF

# 启用配置
ln -s /etc/nginx/sites-available/aligenie /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 5. 配置 HTTPS（SSL 证书）
```bash
# 安装 Certbot
apt install -y certbot python3-certbot-nginx

# 申请证书
certbot --nginx -d your-domain.com

# 自动续期
echo "0 3 1 * * certbot renew --quiet" | crontab -
```

#### 6. 配置 OpenClaw 自启
```bash
# 创建 systemd 服务
cat > /etc/systemd/system/openclaw-gateway.service << 'EOF'
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw
ExecStart=/usr/bin/openclaw gateway --port 18789
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
systemctl daemon-reload
systemctl enable openclaw-gateway
systemctl start openclaw-gateway
systemctl status openclaw-gateway
```

---

### 方案 B: 本地部署 + 内网穿透（测试用）

**工具：** ngrok 或 frp

**步骤：**

#### 1. 启动 OpenClaw Gateway
```bash
openclaw gateway --port 18789
```

#### 2. 启动 Webhook 服务
```bash
cd skills/aligenie-bridge
npm start
```

#### 3. 内网穿透（ngrok）
```bash
# 安装 ngrok
npm install -g ngrok

# 暴露两个端口
ngrok http 18789  # OpenClaw Gateway
ngrok http 3000   # Webhook 服务
```

#### 4. 修改 server.js
```javascript
const OPENCLAW_URL = 'https://your-openclaw.ngrok.io';
```

**缺点：** 
- ❌ ngrok 免费 URL 每次重启会变
- ❌ 不稳定，适合测试

---

### 方案 C:  Railway 部署（简单）

**步骤：**

1. 访问 https://railway.app
2. New Project → Deploy from GitHub
3. 添加两个服务：
   - OpenClaw Gateway（需要配置）
   - Webhook 服务
4. 配置内网通信
5. 获得公网 HTTPS 域名

**成本：** $5-10/月

---

## 📝 修改 server.js

部署到服务器后，设置环境变量：

```bash
# 在服务器上
export OPENCLAW_URL=http://localhost:18789
export PORT=3000

# 或者在 PM2 配置中
# ecosystem.config.js
module.exports = {
  apps: [{
    name: 'aligenie-bridge',
    script: 'server.js',
    env: {
      OPENCLAW_URL: 'http://localhost:18789',
      PORT: 3000
    }
  }]
};
```

---

## 🧪 测试同步回复

### 本地测试（文件模式）
```bash
# 启动 Webhook
cd skills/aligenie-bridge
npm start

# 测试
node test-simple.js
```

预期响应时间：3-5 秒

### 服务器测试（HTTP 模式）
```bash
# SSH 登录服务器
ssh root@your-server-ip

# 测试本地调用
curl -X POST http://localhost:3000/aligenie \
  -H "Content-Type: application/json" \
  -d '{"header":{"name":"IntentRequest"},"payload":{"intent":"general_chat","query":"你好"}}'
```

预期响应：OpenClaw 的直接回复

---

## 🎯 天猫精灵配置

### 1. 访问 https://iap.aligenie.com

### 2. 创建技能
- 标准技能 → 云端服务透传

### 3. 配置 Webhook
```
Webhook URL: https://your-domain.com/aligenie
超时时间：30 秒（重要！）
```

### 4. 配置意图
9 个意图（已在文档中列出）

### 5. 测试
- 真机测试
- 确认响应时间 < 5 秒
- 提交审核

---

## 📊 响应时间优化

### 目标：< 5 秒

**优化建议：**

1. **OpenClaw 预热**
   - 保持 Gateway 常运行
   - 避免冷启动延迟

2. **简化响应**
   - 天气：简洁格式
   - 日程：关键信息
   - 聊天：简短回复

3. **服务器性能**
   - 选择离用户近的机房
   - 保证带宽充足（3Mbps+）

4. **超时处理**
   ```javascript
   // server.js
   const maxWait = 25000; // 25 秒超时
   ```

---

## ✅ 部署检查清单

- [ ] 服务器已购买（2 核 4G+）
- [ ] OpenClaw Gateway 已安装
- [ ] Webhook 服务已部署
- [ ] Nginx 反向代理已配置
- [ ] HTTPS 证书已申请
- [ ] 环境变量已设置（OPENCLAW_URL）
- [ ] 本地测试通过
- [ ] 响应时间 < 5 秒
- [ ] 天猫精灵配置完成
- [ ] 真机测试通过

---

## 🎉 完成后的效果

**你说：** "天猫精灵，查一下北京天气"

**等待 3-5 秒**

**天猫精灵回复：** "北京市今天晴转多云，气温 15-25°C，空气质量良好，适合外出。"

---

## 💰 成本估算

| 项目 | 方案 | 成本 |
|------|------|------|
| 服务器 | 阿里云 2 核 4G | ¥120/月 |
| 域名 | .com | ¥50/年 |
| SSL 证书 | Let's Encrypt | 免费 |
| **总计** | | **¥1,490/年** |

---

## 📞 遇到问题？

### 常见问题

**Q: 响应超时？**
- 检查 OpenClaw Gateway 是否运行
- 增加超时时间到 30 秒
- 优化 OpenClaw 响应速度

**Q: 无法连接 OpenClaw？**
- 检查 OPENCLAW_URL 环境变量
- 确认 Gateway 端口 18789 已开放
- 查看防火墙设置

**Q: 天猫精灵审核不通过？**
- 确保响应时间 < 5 秒
- 提供测试账号
- 检查意图配置

---

**准备好部署了吗？** 选择方案 A（阿里云）最稳定可靠！🚀

有任何问题随时问我！👻
