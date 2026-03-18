# 📕 Xiaohongshu Assistant - 小红书运营助手

> ✍️ **6 种文案风格** | 📤 **一键发布** | 👤 **多账号管理** | 📊 **数据追踪**

[![Skills Count](https://img.shields.io/badge/skills-1-red.svg)](./)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Xiaohongshu](https://img.shields.io/badge/Xiaohongshu-Automation-ff2442.svg)](./)

---

## 📖 功能说明

小红书文案生成 + 自动发布一体化助手！支持 6 种文案风格，一键发布到小红书。

### 核心功能

#### 🎨 文案创作
- ✍️ **文案生成** - 6 种风格（casual/professional/story/小红书/知乎/微博）
- 🎯 **标题优化** - 爆款标题生成（5 个备选）
- 🏷️ **话题推荐** - 智能话题标签推荐（基于热门搜索）
- 😊 **emoji 推荐** - 根据内容自动推荐 emoji
- ⏰ **发布时段建议** - 根据内容类型推荐最佳发布时间

#### 📤 自动发布（新增）⭐
- 📤 **一键发布** - 生成文案后直接发布到小红书
- 🖼️ **图片上传** - 自动下载并上传图片（支持本地路径和 URL）
- 🏷️ **标签填入** - 自动识别 #标签 并填入
- 👤 **多账号管理** - 支持多个小红书账号切换
- 🔐 **登录管理** - Cookie 隔离，安全登录

#### 📊 数据追踪（新增）⭐
- 📈 **曝光追踪** - 追踪笔记曝光量
- ❤️ **互动统计** - 点赞/收藏/评论数
- 💬 **评论管理** - 自动回复评论
- 📉 **趋势分析** - 发布后数据走势

---

## 🚀 快速开始

### 前置条件

1. **安装 XiaohongshuSkills**（发布功能必需）

```bash
# 克隆仓库
cd C:\Users\shenz\.openclaw\workspace
git clone https://github.com/white0dew/XiaohongshuSkills.git

# 安装依赖
cd XiaohongshuSkills
pip install -r requirements.txt
```

2. **登录小红书账号**

```bash
cd XiaohongshuSkills
python scripts/cdp_publish.py login
```

在弹出的 Chrome 窗口扫码登录。

### 基础使用

#### 1. 文案生成

```
# 生成文案
用小红书风格写一篇好物分享
用 professional 风格写一篇评测
用 story 风格写一个使用体验

# 标题优化
帮我想 5 个吸引人的标题
优化这个标题：XXX

# 话题推荐
推荐话题标签
#AI #效率工具 #打工人
```

#### 2. 一键发布（新增）⭐

```
# 生成并发布
用小红书风格写一篇宣传文案并发布
发布笔记，标题：XXX，内容：XXX

# 检查登录状态
检查小红书登录状态
```

#### 3. 账号管理（新增）⭐

```
# 查看账号
查看我的小红书账号
账号列表

# 添加账号
添加账号 test_account 测试账号

# 切换账号
切换到账号 test_account
设置默认账号为 test_account
```

---

## 📊 示例输出

### 1️⃣ 文案生成

**输入**: `用小红书风格写一篇好物分享`

**输出**:
```
📕 **文案生成**（小红书风格）

👻 花 12 天整理了 43 个 OpenClaw 技能！
全部开源！免费！打工人必备！

🎯 都能做什么？

✍️ 内容创作类
- 公众号自动写文章（AI 降味，完全不像 AI 写的）
- 小红书文案生成（标题/文案/标签一键搞定）

💰 生活实用类
- 历史价格监控（双 11 必备）
- 多平台比价（京东/淘宝/拼多多）

💡 我最常用的是：
1️⃣ 价格监控 - 省了好几百
2️⃣ PPT 生成 - 3 分钟搞定

🔗 Gitee：gitee.com/Jake26602/OpenClaw-good-skill

#AI #开源 #效率工具 #打工人 #神器推荐
```

### 2️⃣ 一键发布（新增）⭐

**输入**: `用小红书风格写一篇宣传文案并发布`

**输出**:
```
✅ **发布成功**！

📕 标题：🔥 打工人摸鱼神器！我开源了 43 个 AI 技能
👤 账号：default
🎨 风格：小红书

💡 提示：请前往小红书查看发布效果
```

### 3️⃣ 账号管理（新增）⭐

**输入**: `查看我的小红书账号`

**输出**:
```
📕 **已配置账号**

👑 测试账号 (@test_account)
   发布：3 次 | 最后：2026-03-18

主账号 (@main_account)
   发布：15 次 | 最后：2026-03-17
```

---

## 📁 文件结构

```
xiaohongshu-assistant/
├── SKILL.md                  # 技能描述
├── README.md                 # 使用说明书
├── xiaohongshu_assistant.py  # 主程序
├── templates.py              # 文案模板库
├── xhs_publisher.py          # 发布模块 ⭐ NEW
├── xhs_accounts.py           # 账号管理 ⭐ NEW
└── xhs_accounts.json         # 账号配置（自动生成）
```

---

## 🔧 配置说明

### XiaohongshuSkills 集成

发布功能依赖 [XiaohongshuSkills](https://github.com/white0dew/XiaohongshuSkills) 项目。

**安装步骤**：

```bash
# 1. 克隆仓库
git clone https://github.com/white0dew/XiaohongshuSkills.git

# 2. 安装依赖
cd XiaohongshuSkills
pip install -r requirements.txt

# 3. 登录账号
python scripts/cdp_publish.py login
```

### 账号配置

账号信息存储在 `xhs_accounts.json`，格式如下：

```json
{
  "accounts": {
    "main_account": {
      "alias": "主账号",
      "notes": "日常工作用",
      "created": "2026-03-18T19:00:00",
      "last_login": "2026-03-18T19:00:00",
      "last_publish": "2026-03-18T19:30:00",
      "publish_count": 15
    }
  },
  "default": "main_account"
}
```

---

## 🎯 使用技巧

### 1. 文案风格选择

| 风格 | 适用场景 | 示例 |
|------|----------|------|
| **casual** | 日常分享 | 好物推荐、生活碎片 |
| **professional** | 专业评测 | 产品测评、技术分析 |
| **story** | 情感故事 | 使用体验、心路历程 |
| **小红书** | 爆款文案 | 种草笔记、开箱测评 |
| **知乎** | 深度解答 | 问题分析、经验分享 |
| **微博** | 短小精悍 | 快讯、短消息 |

### 2. 发布时段建议

| 内容类型 | 最佳时段 | 说明 |
|----------|----------|------|
| 职场干货 | 8:00-9:00 | 通勤时间 |
| 美食探店 | 11:00-13:00 | 午饭时间 |
| 生活分享 | 19:00-21:00 | 下班放松 |
| 学习成长 | 21:00-23:00 | 睡前学习 |

### 3. 话题标签策略

**数量**：5-10 个为佳  
**组合**：
- 2-3 个大流量标签（#AI #效率工具）
- 3-5 个精准标签（#OpenClaw #技能分享）
- 1-2 个长尾标签（#打工人摸鱼神器）

---

## 🛠️ 开发计划

- [x] 文案生成（6 种风格）
- [x] 标题优化
- [x] 话题推荐
- [x] emoji 推荐
- [x] 一键发布 ⭐ NEW
- [x] 多账号管理 ⭐ NEW
- [ ] 数据追踪 ⏳
- [ ] 自动回复评论 ⏳
- [ ] 竞品分析 ⏳
- [ ] 热门时段分析 ⏳

---

## ⚠️ 注意事项

1. **遵守平台规则** - 不要发布违规内容
2. **发布频率** - 建议每天 1-3 篇，避免频繁发布
3. **Cookie 安全** - 存储在本地，请勿泄露
4. **账号安全** - 多账号操作注意 IP 隔离

---

## 📝 更新日志

### v2.0.0 (2026-03-18) ⭐ MAJOR
- ✨ 新增一键发布功能（基于 XiaohongshuSkills）
- ✨ 新增多账号管理
- ✨ 新增登录状态检查
- ✨ 集成 CDP 自动化发布
- 🐛 修复文案生成 bug

### v1.2.0 (2026-03-18)
- ✨ 添加 6 种文案风格
- ✨ 创建 templates.py 模板库
- 🐛 修复 emoji 显示问题

### v1.0.0 (2026-03-16)
- 🎉 初始版本

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License

## 👻 关于

由 **小鬼** 👻 创建和维护

- **作者**: Jake's AI Assistant
- **版本**: 2.0.0
- **创建日期**: 2026-03-16
- **最后更新**: 2026-03-18

---

<div align="center">

**Made with 👻 by 小鬼**

[⬆ 返回顶部](#-xiaohongshu-assistant---小红书运营助手)

</div>
