# Ngrok 配置说明

## 📋 步骤

### 1. 注册 ngrok 账号
访问：https://ngrok.com/signup

### 2. 获取 Authtoken
登录后访问：https://dashboard.ngrok.com/get-started/your-authtoken
复制你的 Authtoken

### 3. 配置 Authtoken
在终端运行：
```bash
ngrok config add-authtoken 你的_AUTHTOKEN
```

### 4. 启动隧道
打开两个终端：

**终端 1（OpenClaw Gateway）：**
```bash
ngrok http 18789
```

**终端 2（Webhook 服务）：**
```bash
ngrok http 3000
```

### 5. 复制 URL
启动后会显示：
```
Forwarding: https://xxxx.ngrok-free.app -> http://localhost:18789
Forwarding: https://yyyy.ngrok-free.app -> http://localhost:3000
```

### 6. 设置 OPENCLAW_URL
```bash
$env:OPENCLAW_URL = "https://xxxx.ngrok-free.app"
```

---

## 🎯 快速测试

你现在可以：
1. 去 https://ngrok.com 注册
2. 复制 Authtoken
3. 告诉我，我帮你执行后续命令
