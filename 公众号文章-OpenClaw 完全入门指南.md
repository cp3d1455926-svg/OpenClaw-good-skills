# OpenClaw 完全入门指南

**副标题**: 从安装到配置，30 分钟打造你的超级 AI 助手

---

## 🚀 前言

你是不是经常想：
> "要是有一个 AI 助手，能帮我做所有事情就好了！"

**OpenClaw 就是这样一个神器。**

它是一个开源的 AI 助手框架，可以让你的 AI：
- 📝 自动写日记、记录记忆
- 📦 发布技能到 ClawHub
- 📰 自动推送新闻
- 💬 在多个平台聊天（微信、QQ、飞书、Discord...）
- 🔧 执行各种任务（文件处理、数据分析、网页搜索...）

**最重要的是：完全免费、开源、可定制！**

今天，我用 30 分钟，带你从零开始，搭建属于你的超级 AI 助手！

---

## 📋 目录

1. [什么是 OpenClaw](#什么是-openclaw)
2. [安装前的准备](#安装前的准备)
3. [安装 OpenClaw](#安装-openclaw)
4. [配置 AI 模型](#配置-ai-模型)
5. [配置消息平台](#配置消息平台)
6. [快速上手](#快速上手)
7. [技能系统](#技能系统)
8. [常见问题](#常见问题)

---

## 什么是 OpenClaw

### 🤖 官方定义

OpenClaw 是一个开源的 AI 助手框架，支持：
- 多平台消息接入（微信、QQ、飞书、Discord、Slack 等）
- 多 AI 模型支持（通义千问、Kimi、GPT-4 等）
- 技能系统（可扩展功能）
- 记忆系统（长期记忆、日记）
- 定时任务（自动推送、提醒）

### 💡 通俗解释

**OpenClaw = AI 助手的大脑 + 手脚**

- **大脑**: 接入各种 AI 模型（通义千问、Kimi 等）
- **手脚**: 可以执行各种任务（发消息、写文件、搜索网页等）
- **记忆**: 记住你说过的话、做过的事
- **技能**: 像手机 App 一样，可以安装各种功能

### 🎯 适用场景

| 场景 | 用途 |
|------|------|
| 个人助理 | 日程管理、提醒、笔记 |
| 客服机器人 | 自动回复、问题解答 |
| 内容创作 | 写文章、生成图片 |
| 数据分析 | 统计、报表、可视化 |
| 自动化 | 定时任务、批量处理 |

---

## 安装前的准备

### ✅ 系统要求

| 系统 | 支持 |
|------|------|
| Windows | ✅ 支持（Win10+） |
| macOS | ✅ 支持 |
| Linux | ✅ 支持 |

### 📦 需要安装

1. **Node.js** (v18 或更高版本)
   - 下载地址：https://nodejs.org/
   - 验证安装：`node --version`

2. **npm** (随 Node.js 一起安装)
   - 验证安装：`npm --version`

3. **AI 模型 API Key**（至少一个）
   - 通义千问：https://dashscope.aliyun.com/
   - Kimi：https://platform.moonshot.cn/
   - GPT-4：https://platform.openai.com/

4. **消息平台账号**（可选）
   - 微信/企业微信
   - QQ
   - 飞书
   - Discord
   - Slack

---

## 安装 OpenClaw

### 步骤 1：安装 OpenClaw

打开终端（命令行），执行：

```bash
npm install -g openclaw
```

**验证安装**：
```bash
openclaw --version
```

看到版本号就说明安装成功！✅

### 步骤 2：初始化项目

```bash
# 创建工作目录
mkdir my-ai-assistant
cd my-ai-assistant

# 初始化 OpenClaw
openclaw init
```

这会创建以下目录结构：

```
my-ai-assistant/
├── workspace/          # 工作目录
│   ├── memory/        # 记忆文件
│   ├── AGENTS.md      # 助手配置
│   ├── SOUL.md        # 人格设定
│   └── USER.md        # 用户信息
├── config.json        # 配置文件
└── skills/            # 技能目录
```

---

## 配置 AI 模型

### 步骤 1：编辑配置文件

打开 `config.json`，添加 AI 模型配置：

```json
{
  "models": {
    "default": "bailian/kimi-k2.5",
    "current": "bailian/qwen3.5-plus"
  },
  "apiKeys": {
    "bailian": "sk-your-api-key-here"
  }
}
```

### 步骤 2：获取 API Key

#### 通义千问（推荐）

1. 访问：https://dashscope.aliyun.com/
2. 注册/登录阿里云账号
3. 进入"API-KEY 管理"
4. 创建新的 API Key
5. 复制到配置文件

#### Kimi

1. 访问：https://platform.moonshot.cn/
2. 注册/登录
3. 进入"个人中心" → "API Key"
4. 创建并复制

### 步骤 3：验证配置

```bash
openclaw status
```

看到模型信息就说明配置成功！✅

---

## 配置消息平台

### 方式一：企业微信（推荐新手）

**优点**：配置简单、无需服务器

1. **创建企业**
   - 访问：https://work.weixin.qq.com/
   - 注册企业微信

2. **创建应用**
   - 进入"应用管理" → "创建应用"
   - 填写应用名称、头像等

3. **获取配置信息**
   - 企业 ID（CorpID）
   - 应用 AgentID
   - 应用 Secret

4. **配置到 OpenClaw**
   ```json
   {
     "channels": {
       "wecom": {
         "corpId": "your-corp-id",
         "agentId": "your-agent-id",
         "secret": "your-secret"
       }
     }
   }
   ```

### 方式二：飞书

1. **创建飞书应用**
   - 访问：https://open.feishu.cn/
   - 创建企业/个人应用

2. **获取配置**
   - App ID
   - App Secret
   - Verification Token

3. **配置到 OpenClaw**
   ```json
   {
     "channels": {
       "feishu": {
         "appId": "your-app-id",
         "appSecret": "your-app-secret",
         "verificationToken": "your-token"
         }
   }
   }
   ```

### 方式三：QQ（需要额外配置）

QQ 配置相对复杂，需要：
1. 安装 go-cqhttp
2. 配置 WebSocket
3. 连接 OpenClaw

**新手建议先用企业微信或飞书。**

---

## 快速上手

### 启动 OpenClaw

```bash
# 启动 Gateway（消息网关）
openclaw gateway start

# 查看状态
openclaw gateway status
```

### 第一次对话

1. 在配置的消息平台发送消息
2. OpenClaw 会自动回复
3. 开始聊天！

### 常用命令

```bash
# 查看状态
openclaw status

# 查看日志
openclaw logs

# 重启 Gateway
openclaw gateway restart

# 停止 Gateway
openclaw gateway stop

# 查看帮助
openclaw --help
```

---

## 技能系统

### 什么是技能？

技能 = OpenClaw 的"插件"或"App"

每个技能提供特定功能，比如：
- 📝 写日记
- 📰 推送新闻
- 📊 数据分析
- 🎨 生成图片
- 🔍 网页搜索

### 安装技能

#### 方式一：从 ClawHub 安装（推荐）

```bash
# 安装单个技能
clawhub install life-memory-logger

# 安装多个
clawhub install news-evening-digest data-analytics-assistant
```

#### 方式二：手动安装

1. 下载技能文件夹
2. 放到 `skills/` 目录
3. 重启 OpenClaw

### 已发布的热门技能

| 技能 | 功能 | 推荐指数 |
|------|------|----------|
| life-memory-logger | 生活记忆记录 | ⭐⭐⭐⭐⭐ |
| news-evening-digest | 新闻晚报推送 | ⭐⭐⭐⭐⭐ |
| data-analytics-assistant | 数据分析 | ⭐⭐⭐⭐⭐ |
| email-helper | 邮件助手 | ⭐⭐⭐⭐ |
| movie-recommender | 电影推荐 | ⭐⭐⭐⭐ |
| multi-source-research | 多源研究 | ⭐⭐⭐⭐⭐ |
| countdown-timer | 倒计时 | ⭐⭐⭐⭐ |
| book-recommender | 书籍推荐 | ⭐⭐⭐⭐ |
| goal-manager | 目标管理 | ⭐⭐⭐⭐⭐ |
| file-super-assistant | 文件处理 | ⭐⭐⭐⭐⭐ |

### 查看已安装技能

```bash
clawhub list
```

### 发布自己的技能

```bash
# 创建技能文件夹
mkdir my-skill
cd my-skill

# 创建 SKILL.md
echo "# My Skill" > SKILL.md

# 发布到 ClawHub
clawhub publish . --slug "my-skill" --name "My Skill" --version "1.0.0"
```

---

## 记忆系统

### 日记功能

OpenClaw 会自动记录每天的对话和任务：

**文件位置**: `memory/YYYY-MM-DD.md`

**内容包含**:
- 对话记录
- 完成的任务
- 创建的文件
- 统计数据
- 心情感受

### 长期记忆

**文件**: `MEMORY.md`

记录重要的、需要长期记住的事情：
- 用户偏好
- 重要事件
- 经验教训

### 查看记忆

```bash
# 查看今日日记
cat memory/2026-03-30.md

# 查看长期记忆
cat MEMORY.md
```

---

## 常见问题

### Q1: 安装失败怎么办？

**可能原因**:
- Node.js 版本太低
- 网络问题
- 权限问题

**解决方案**:
```bash
# 升级 Node.js
node --version  # 确保 v18+

# 使用管理员权限
npm install -g openclaw --force

# 使用国内镜像
npm config set registry https://registry.npmmirror.com
npm install -g openclaw
```

### Q2: API Key 无效？

**检查**:
1. API Key 是否正确复制
2. 是否有余额/额度
3. 模型名称是否正确

**解决**:
```json
{
  "models": {
    "default": "bailian/kimi-k2.5"
  },
  "apiKeys": {
    "bailian": "sk-正确 - 的 -API-Key"
  }
}
```

### Q3: 消息平台不回复？

**检查**:
1. Gateway 是否启动
2. 配置是否正确
3. 平台权限是否开通

**解决**:
```bash
# 查看 Gateway 状态
openclaw gateway status

# 查看日志
openclaw logs

# 重启 Gateway
openclaw gateway restart
```

### Q4: 技能不工作？

**检查**:
1. 技能是否正确安装
2. 技能配置是否完整
3. 是否有权限问题

**解决**:
```bash
# 查看已安装技能
clawhub list

# 重新安装技能
clawhub uninstall skill-name
clawhub install skill-name
```

### Q5: 如何更新 OpenClaw？

```bash
# 更新到最新版本
npm update -g openclaw

# 查看版本
openclaw --version
```

---

## 进阶配置

### 自定义 AI 人格

编辑 `SOUL.md`：

```markdown
# SOUL.md - Who You Are

- **Name**: 小鬼
- **Vibe**: 温暖、有趣、可靠
- **Emoji**: 👻
```

### 自定义用户信息

编辑 `USER.md`：

```markdown
# USER.md - About Your Human

- **Name**: momo
- **Timezone**: Asia/Shanghai
- **Notes**: 喜欢养虾、科技、AI
```

### 配置定时任务

编辑 `HEARTBEAT.md`：

```markdown
# HEARTBEAT.md

# 每天 20 点发送新闻晚报
- 如果当前时间在 20:00-21:00 之间，发送新闻晚报
```

---

## 资源链接

### 官方资源

- **官网**: https://openclaw.ai
- **文档**: https://docs.openclaw.ai
- **GitHub**: https://github.com/openclaw/openclaw
- **Discord**: https://discord.com/invite/clawd
- **ClawHub**: https://clawhub.com

### 社区资源

- **技能市场**: https://clawhub.com
- **教程**: https://docs.openclaw.ai/tutorials
- **问题反馈**: GitHub Issues

---

## 总结

恭喜你！完成了 OpenClaw 的入门教程！🎉

### ✅ 你现在可以：

1. 安装和配置 OpenClaw
2. 接入 AI 模型
3. 配置消息平台
4. 安装和使用技能
5. 管理记忆和日记

### 🚀 下一步：

1. **安装热门技能** - 让 AI 更强大
2. **配置消息平台** - 随时随地聊天
3. **定制 AI 人格** - 打造专属助手
4. **发布自己的技能** - 分享给社区

### 💡 小贴士：

- 遇到问题先看文档
- 多尝试不同的技能组合
- 加入社区获取帮助
- 定期备份配置文件

---

**作者**: momo & 小鬼（AI 虾）🦐👻  
**更新时间**: 2026-03-30  
**OpenClaw 版本**: 2026.3.2

---

## 📣 互动

**关注我（momo 养虾记）**，回复"**OpenClaw**"获取：
- 完整配置文件模板
- 技能安装脚本
- 常见问题解决方案
- 最新更新通知

**欢迎在评论区提问！** 👇

---

**⚠️ 免责声明**: 本文基于 OpenClaw 2026.3.2 版本编写，后续版本可能有变化。请以官方文档为准。
