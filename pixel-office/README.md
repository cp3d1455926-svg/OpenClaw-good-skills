# 🦞 OpenClaw 像素办公室

**实时状态看板** - 把 OpenClaw 的工作状态可视化！

---

## 🚀 快速启动

### 方式一：仅前端（静态演示）

```bash
cd pixel-office
python -m http.server 8890
```

访问：http://localhost:8890

### 方式二：完整后端（实时同步 OpenClaw 状态）⭐

```bash
# 1. 安装依赖
cd pixel-office/backend
pip install -r requirements.txt

# 2. 启动后端
python app.py

# 3. 访问
http://localhost:19000
```

---

## 📡 API 端点

| 端点 | 说明 |
|------|------|
| `GET /api/status` | 获取当前状态 |
| `GET /api/openclaw/status` | 获取 OpenClaw 实时状态 |
| `POST /api/set_state` | 手动设置状态 |
| `GET /api/yesterday-memo` | 获取昨日小记 |
| `GET /api/skills` | 获取技能列表 |

---

## 🎯 状态映射

| OpenClaw 活动 | 办公室状态 | 龙虾位置 |
|--------------|-----------|---------|
| 待命 | `idle` | 🛋️ 休息区 |
| 写代码/文档 | `writing` | 💻 工作区 |
| 搜索/调研 | `researching` | 💻 工作区 |
| 执行命令 | `executing` | 💻 工作区 |
| 同步数据 | `syncing` | 💻 工作区 |
| 报错/异常 | `error` | 🐛 Bug 区 |

---

## 🔧 自动状态同步

后端会每 5 秒自动调用 `openclaw status` 命令，解析以下信息：

- ✅ Token 使用量（输入/输出）
- ✅ 当前模型
- ✅ 成本统计
- ✅ 上下文使用率

根据活动自动切换龙虾位置！

---

## 📦 项目结构

```
pixel-office/
├── index.html          # 前端主页面（对接后端 API）
├── index_v5.html       # 静态演示版
├── backend/
│   ├── app.py          # Flask 后端
│   ├── requirements.txt
│   └── state.json      # 状态缓存
├── memory/             # 记忆文件（自动读取）
└── README.md
```

---

## 🎨 功能特性

- ✅ **实时状态同步** - 每 5 秒自动更新
- ✅ **Token 统计** - 显示输入/输出 Token
- ✅ **昨日小记** - 自动读取 memory 文件
- ✅ **技能墙** - 43 个技能展示
- ✅ **技能详情** - 点击查看详细信息
- ✅ **状态切换** - 手动/自动两种方式
- ✅ **GitHub Star** - 显示仓库 Star 数

---

## 🛠️ 开发说明

### 添加新技能

编辑 `index.html` 中的 `SKILLS` 数组：

```javascript
const SKILLS = [
    { name: '新技能', icon: '🆕', desc: '描述', size: '5KB', version: 'v1.0', calls: 0 },
    // ...
];
```

### 自定义状态

编辑 `STATES` 配置：

```javascript
const STATES = {
    idle: { zone: 'lounge', emoji: '🛋️', text: '待命中...', color: '#4ecdc4' },
    // ...
};
```

### 修改区域布局

编辑 `CONFIG.zones`：

```javascript
zones: {
    lounge: { x: 0.15, y: 0.5, w: 0.25, h: 0.35, name: '休息区' },
    // ...
}
```

---

## 📸 截图

![像素办公室](docs/screenshot.png)

---

## 🎯 下一步计划

- [ ] WebSocket 实时推送（替代轮询）
- [ ] 多 Agent 协作支持
- [ ] 技能调用统计图表
- [ ] 主题切换（深色/浅色/赛博朋克）
- [ ] 桌面宠物版（Electron）
- [ ] 移动端适配

---

## 📄 许可证

MIT License

---

**🦞 Made with ❤️ for OpenClaw**
