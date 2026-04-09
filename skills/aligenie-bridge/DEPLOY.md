# 天猫精灵 × OpenClaw 公网部署指南

## 📦 部署方案对比

| 方案 | 成本 | 难度 | 适合场景 |
|------|------|------|---------|
| **阿里云/腾讯云** | ¥50-100/月 | ⭐⭐⭐ | 生产环境，稳定可靠 |
| **Vercel (推荐)** | 免费 | ⭐⭐ | 快速部署，自动 HTTPS |
| **Railway** | 免费/$5/月 | ⭐⭐ | 简单部署，自动 SSL |
| **ngrok (临时)** | 免费 | ⭐ | 仅测试，URL 会变 |

---

## 🚀 方案一：Vercel 部署（推荐 - 免费 + 自动 HTTPS）

### 步骤 1: 准备 Vercel 配置文件

创建 `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "server.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "server.js"
    }
  ],
  "env": {
    "OPENCLAW_URL": "http://your-server-ip:18789"
  }
}
```

### 步骤 2: 修改 server.js 支持 Vercel

```javascript
// 添加 Vercel 支持
module.exports = app;
```

### 步骤 3: 部署到 Vercel

```bash
# 安装 Vercel CLI
npm install -g vercel

# 登录
vercel login

# 部署
vercel --prod
```

### 步骤 4: 获得 HTTPS 域名

```
✅ https://your-project.vercel.app
```

---

## ☁️ 方案二：阿里云/腾讯云部署（生产环境）

### 步骤 1: 购买服务器

**推荐配置：**
- CPU: 1 核
- 内存：1GB
- 带宽：1Mbps
- 系统：Ubuntu 20.04 LTS

**价格：** 约 ¥50-100/月

### 步骤 2: 服务器初始化

```bash
# SSH 登录
ssh root@your-server-ip

# 更新系统
apt update && apt upgrade -y

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs npm

# 安装 Git
apt install -y git

# 安装 Nginx
apt install -y nginx

# 安装 Certbot（SSL 证书）
apt install -y certbot python3-certbot-nginx
```

### 步骤 3: 部署应用

```bash
# 创建应用目录
mkdir -p /var/www/aligenie-bridge
cd /var/www/aligenie-bridge

# 上传代码（方式任选）
# 方式 1: Git clone
git clone <your-repo> .

# 方式 2: SCP 上传
# 本地执行：scp -r ./skills/aligenie-bridge/* root@server:/var/www/aligenie-bridge/

# 安装依赖
npm install --production

# 安装 PM2（进程管理）
npm install -g pm2
```

### 步骤 4: 配置 PM2

```bash
# 创建 PM2 配置文件
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'aligenie-bridge',
    script: 'server.js',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '200M',
    env: {
      NODE_ENV: 'production',
      PORT: 3000,
      OPENCLAW_URL: 'http://localhost:18789'
    }
  }]
};
EOF

# 启动应用
pm2 start ecosystem.config.js

# 保存 PM2 配置（开机自启）
pm2 save
pm2 startup
```

### 步骤 5: 配置 Nginx 反向代理

```bash
# 创建 Nginx 配置
cat > /etc/nginx/sites-available/aligenie-bridge << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

# 启用配置
ln -s /etc/nginx/sites-available/aligenie-bridge /etc/nginx/sites-enabled/

# 测试配置
nginx -t

# 重启 Nginx
systemctl restart nginx
```

### 步骤 6: 配置 HTTPS（SSL 证书）

```bash
# 申请免费 SSL 证书（Let's Encrypt）
certbot --nginx -d your-domain.com

# 自动续期（添加到 crontab）
echo "0 3 1 * * certbot renew --quiet" | crontab -
```

### 步骤 7: 配置防火墙

```bash
# 启用防火墙
ufw enable

# 允许 SSH、HTTP、HTTPS
ufw allow OpenSSH
ufw allow 'Nginx Full'

# 查看状态
ufw status
```

---

## 🌐 方案三：Railway 部署（简单快速）

### 步骤 1: 注册 Railway

访问 https://railway.app 注册账号

### 步骤 2: 创建项目

1. New Project → Deploy from GitHub repo
2. 选择你的代码仓库
3. 添加环境变量：
   - `PORT`: 3000
   - `OPENCLAW_URL`: http://your-server-ip:18789

### 步骤 3: 部署

Railway 会自动构建和部署，获得 HTTPS 域名：
```
https://your-project.railway.app
```

---

## 🔧 部署脚本（一键部署到阿里云）

创建 `deploy.sh`:

```bash
#!/bin/bash

set -e

echo "🚀 开始部署天猫精灵桥接服务..."

# 变量配置
APP_NAME="aligenie-bridge"
APP_DIR="/var/www/$APP_NAME"
DOMAIN="your-domain.com"
EMAIL="your-email@example.com"

# 1. 安装依赖
echo "📦 安装系统依赖..."
apt update
apt install -y nodejs npm nginx certbot python3-certbot-nginx git

# 2. 创建应用目录
echo "📁 创建应用目录..."
mkdir -p $APP_DIR
cd $APP_DIR

# 3. 复制代码（假设代码在当前目录）
echo "📝 复制代码..."
cp -r /root/$APP_NAME/* $APP_DIR/

# 4. 安装 npm 依赖
echo "🔧 安装 npm 依赖..."
npm install --production

# 5. 安装 PM2
echo "⚙️ 安装 PM2..."
npm install -g pm2

# 6. 创建 PM2 配置
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: '$APP_NAME',
    script: 'server.js',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '200M',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    }
  }]
};
EOF

# 7. 启动应用
echo "▶️ 启动应用..."
pm2 start ecosystem.config.js
pm2 save
pm2 startup | tail -1 | bash

# 8. 配置 Nginx
echo "🌐 配置 Nginx..."
cat > /etc/nginx/sites-available/$APP_NAME << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

ln -s /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# 9. 配置 SSL
echo "🔒 配置 SSL..."
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email $EMAIL

# 10. 完成
echo "✅ 部署完成！"
echo "📍 访问地址：https://$DOMAIN"
echo "🔍 健康检查：https://$DOMAIN/health"
echo "📡 Webhook: POST https://$DOMAIN/aligenie"
```

使用：
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 📊 部署后检查清单

### ✅ 服务检查

```bash
# 检查 PM2 状态
pm2 status

# 查看日志
pm2 logs aligenie-bridge

# 检查 Nginx
systemctl status nginx

# 测试健康检查
curl https://your-domain.com/health
```

### ✅ 网络检查

```bash
# 检查端口监听
netstat -tlnp | grep :3000
netstat -tlnp | grep :80
netstat -tlnp | grep :443

# 检查防火墙
ufw status
```

### ✅ 功能测试

```bash
# 测试 Webhook
curl -X POST https://your-domain.com/aligenie \
  -H "Content-Type: application/json" \
  -d '{"header":{"name":"IntentRequest"},"payload":{"intent":"general_chat","query":"测试"}}'
```

---

## 🔗 天猫精灵开放平台配置

### 步骤 1: 注册开发者账号

访问 https://iap.aligenie.com 注册

### 步骤 2: 创建技能

1. 控制台 → 创建技能
2. 选择"标准技能" → "云端服务透传"
3. 填写技能信息

### 步骤 3: 配置 Webhook

```
Webhook URL: https://your-domain.com/aligenie
请求类型：POST
Content-Type: application/json
```

### 步骤 4: 配置意图

添加意图（参考 test-all.js 中的 intent 列表）

### 步骤 5: 测试发布

1. 真机测试（绑定测试账号）
2. 提交审核
3. 等待发布

---

## 💰 成本估算

| 项目 | 方案 | 成本 |
|------|------|------|
| **服务器** | Vercel | 免费 |
| **域名** | .com | ¥50/年 |
| **SSL 证书** | Let's Encrypt | 免费 |
| **总计** | | ¥50/年 |

| 项目 | 方案 | 成本 |
|------|------|------|
| **服务器** | 阿里云 1 核 1G | ¥60/月 |
| **域名** | .com | ¥50/年 |
| **SSL 证书** | Let's Encrypt | 免费 |
| **总计** | | ¥770/年 |

---

## 🎯 推荐方案

**个人使用/测试：** Vercel（免费 + 自动 HTTPS）

**生产环境：** 阿里云 + 独立域名（稳定可控）

---

## 📞 需要帮助？

部署遇到问题？
1. 查看 PM2 日志：`pm2 logs`
2. 查看 Nginx 日志：`tail -f /var/log/nginx/error.log`
3. 检查防火墙：`ufw status`

---

准备好部署了吗？告诉我你选哪个方案，我帮你具体配置！👻
