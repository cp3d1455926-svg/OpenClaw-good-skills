# 🦞 OpenClaw 完全入门指南（Windows 篇）

> **最后更新**: 2026 年 3 月 30 日  
> **适用版本**: OpenClaw 最新版  
> **预计耗时**: 15-30 分钟

---

## 📖 什么是 OpenClaw？

OpenClaw 是一个**自托管的 AI 网关**，让你可以通过微信、Telegram、Discord 等聊天工具随时与 AI 助手对话。它运行在你自己的电脑上，数据完全由你掌控。

**核心特点**：
- 🏠 **自托管**：运行在你的硬件上，你的规则
- 💬 **多通道**：一个网关同时服务微信、Telegram、Discord 等
- 🤖 **原生支持 Agent**：内置工具调用、会话管理、多 Agent 路由
- 🔓 **开源**：MIT 许可，社区驱动

---

## 🎯 两种方式安装

### 方式一：WSL2（⭐ 强烈推荐）

WSL2 是 Windows 上的 Linux 子系统，OpenClaw 在 WSL2 上运行最稳定，功能最完整。

### 方式二：原生 Windows

支持原生 Windows，但部分功能可能受限。适合快速体验。

---

## 🚀 快速开始（WSL2 方式）

### 第一步：安装 WSL2

以**管理员身份**打开 PowerShell，运行：

```powershell
wsl --install
```

系统会自动安装 WSL2 和 Ubuntu 发行版。安装完成后**重启电脑**。

重启后，在开始菜单搜索 "Ubuntu" 并打开，设置用户名和密码。

### 第二步：启用 systemd（必需）

在 Ubuntu 终端中运行：

```bash
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```

然后回到 PowerShell 执行：

```powershell
wsl --shutdown
```

重新打开 Ubuntu，验证 systemd 是否启用：

```bash
systemctl --user status
```

### 第三步：安装 OpenClaw

在 Ubuntu 终端中运行：

```bash
# 一键安装脚本（推荐）
curl -fsSL https://openclaw.ai/install.sh | bash
```

安装脚本会自动：
- 检测并安装 Node.js（需要 Node 22.14+ 或 Node 24）
- 安装 OpenClaw CLI
- 启动配置向导

### 第四步：运行配置向导

```bash
openclaw onboard --install-daemon
```

向导会引导你完成：

1. **选择模型提供商**：Anthropic、OpenAI、Google、Kimi 等
2. **输入 API Key**：从你的模型提供商获取
3. **配置网关**：端口（默认 18789）、认证方式
4. **选择通道**：Telegram、微信等（可跳过，稍后配置）
5. **安装守护进程**：让 OpenClaw 开机自启

### 第五步：验证安装

```bash
# 检查网关状态
openclaw gateway status

# 打开控制面板
openclaw dashboard
```

这会打开浏览器访问 `http://127.0.0.1:18789/`，看到控制面板即表示安装成功！

### 第六步：发送第一条消息

在控制面板的聊天框中输入任意消息，AI 会立即回复。🎉

---

## 🪟 快速开始（原生 Windows 方式）

### 第一步：安装 Node.js

访问 [Node.js 官网](https://nodejs.org/) 下载并安装 **Node 22 LTS** 或 **Node 24**。

安装完成后验证：

```powershell
node --version
# 应显示 v22.x.x 或 v24.x.x
```

### 第二步：安装 OpenClaw

以**管理员身份**打开 PowerShell，运行：

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

### 第三步：运行配置向导

```powershell
openclaw onboard --install-daemon
```

### 第四步：验证安装

```powershell
# 检查网关状态
openclaw gateway status

# 打开控制面板
openclaw dashboard
```

---

## 📱 配置聊天通道

### Telegram（最快，5 分钟搞定）

1. **创建 Bot**
   - 在 Telegram 搜索 `@BotFather`
   - 发送 `/newbot`
   - 按提示设置 Bot 名称和用户名
   - 保存 Bot Token（类似 `123456:ABC-DEF1234...`）

2. **配置 Token**
   
   编辑配置文件 `~/.openclaw/openclaw.json`（WSL2 中）：
   
   ```json5
   {
     "channels": {
       "telegram": {
         "enabled": true,
         "botToken": "你的 Bot Token"
       }
     }
   }
   ```

3. **重启网关**
   
   ```bash
   openclaw gateway restart
   ```

4. **配对设备**
   
   - 在 Telegram 搜索你的 Bot 用户名
   - 发送 `/start`
   - 在终端查看配对码并批准：
   
   ```bash
   openclaw pairing list telegram
   openclaw pairing approve telegram <配对码>
   ```

5. **开始聊天**
   
   在 Telegram 中给 Bot 发消息，即可与 AI 对话！

### 微信（企业微信）

如果你在企业微信环境，可以配置企业微信通道：

```json5
{
  "channels": {
    "wecom": {
      "enabled": true,
      "corpId": "企业 ID",
      "agentId": "应用 ID",
      "secret": "应用 Secret"
    }
  }
}
```

---

## 🛠️ 常用命令速查

### 网关管理

```bash
# 查看状态
openclaw gateway status

# 启动网关
openclaw gateway start

# 停止网关
openclaw gateway stop

# 重启网关
openclaw gateway restart

# 查看日志
openclaw logs --follow
```

### 会话管理

```bash
# 列出所有会话
openclaw sessions list

# 查看会话历史
openclaw sessions history <sessionKey>

# 终止会话
openclaw sessions stop <sessionKey>
```

### 设备配对

```bash
# 查看待批准的设备
openclaw devices list

# 批准设备
openclaw devices approve <requestId>

# 撤销设备
openclaw devices revoke --device <deviceId>
```

### 配置管理

```bash
# 编辑配置
openclaw configure

# 检查配置问题
openclaw doctor

# 应用配置并重启
openclaw config apply
```

---

## 📂 重要文件位置

### WSL2 环境

| 文件/目录 | 路径 |
|-----------|------|
| 配置文件 | `~/.openclaw/openclaw.json` |
| 工作空间 | `~/.openclaw/workspace/` |
| 记忆文件 | `~/.openclaw/workspace/memory/` |
| 日志文件 | `~/.openclaw/logs/` |

### 原生 Windows

| 文件/目录 | 路径 |
|-----------|------|
| 配置文件 | `C:\Users\<用户名>\.openclaw\openclaw.json` |
| 工作空间 | `C:\Users\<用户名>\.openclaw\workspace\` |
| 日志文件 | `C:\Users\<用户名>\.openclaw\logs\` |

---

## 🔧 高级配置

### 修改默认模型

编辑 `~/.openclaw/openclaw.json`：

```json5
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-sonnet-4-5-20250929"
    }
  }
}
```

### 配置允许列表（安全加固）

只允许特定用户访问：

```json5
{
  "channels": {
    "telegram": {
      "dmPolicy": "allowlist",
      "allowFrom": ["你的 Telegram 用户 ID"]
    }
  }
}
```

### 启用 Tailscale 远程访问

```bash
openclaw gateway --tailscale serve
```

然后通过 Tailscale MagicDNS 访问：`https://<your-hostname>/`

### 配置技能（Skills）

安装推荐技能：

```bash
openclaw skills install weather
openclaw skills install web-search
openclaw skills install browser
```

---

## 🐛 常见问题

### 1. `openclaw` 命令找不到

**原因**：npm 全局目录不在 PATH 中

**解决**：

```powershell
# 找到全局目录
npm prefix -g

# 将结果添加到 PATH（添加到 ~/.bashrc 或 $PROFILE）
export PATH="$(npm prefix -g)/bin:$PATH"
```

### 2. 网关启动失败

**检查**：

```bash
# 查看详细错误
openclaw gateway run

# 检查配置
openclaw doctor
```

**常见原因**：
- API Key 无效或过期
- 端口被占用（默认 18789）
- 配置文件语法错误

### 3. Telegram Bot 不回复

**排查步骤**：

1. 检查 Bot Token 是否正确
2. 确认 Bot 已批准你的消息（`openclaw pairing list`）
3. 查看网关日志（`openclaw logs --follow`）
4. 如果是群聊，检查是否需要 @提及

### 4. WSL2 网络问题

**重置 WSL 网络**：

```powershell
wsl --shutdown
# 重新打开 Ubuntu
```

**检查 WSL IP**：

```bash
hostname -I
```

---

## 📚 下一步学习

- [官方文档](https://docs.openclaw.ai)
- [技能市场](https://clawhub.com) - 安装更多技能
- [Discord 社区](https://discord.com/invite/clawd)
- [GitHub 仓库](https://github.com/openclaw/openclaw)

### 推荐技能

```bash
# 天气查询
openclaw skills install weather

# 网页搜索
openclaw skills install web-search

# 浏览器自动化
openclaw skills install agent-browser

# 文件处理
openclaw skills install file-super-assistant

# 新闻摘要
openclaw skills install news-digest-aggregator
```

---

## 💡 最佳实践

1. **使用 WSL2**：功能最完整，问题最少
2. **定期备份**：备份 `~/.openclaw/` 目录
3. **启用日志**：遇到问题先查日志
4. **安全加固**：生产环境务必配置 allowFrom
5. **使用 Tailscale**：远程访问最安全的方式

---

## 🎉 恭喜！

你已经成功安装并配置了 OpenClaw！现在你可以：

- ✅ 在浏览器控制面板与 AI 对话
- ✅ 通过 Telegram 随时随地访问 AI
- ✅ 安装各种技能扩展功能
- ✅ 配置多个 Agent 处理不同任务

**有问题？** 查看日志 `openclaw logs --follow` 或访问官方文档。

祝你使用愉快！🦞
