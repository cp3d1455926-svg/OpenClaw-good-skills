# 天猫精灵 × OpenClaw 智能接入方案

## 🎯 目标
让天猫精灵通过语音调用 OpenClaw 的 skills，实现智能对话和任务执行。

## 📐 架构设计

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 天猫精灵     │────▶│ 天猫精灵云平台    │────▶│ Webhook 服务     │────▶│ OpenClaw Gateway│
│ (语音指令)   │     │ (云端服务透传)    │     │ (Node.js/Python) │     │ (执行 Skills)    │
└─────────────┘     └──────────────────┘     └─────────────────┘     └─────────────────┘
       ▲                                                                                    │
       │                                                                                    ▼
       │                                                                             ┌─────────────┐
       └────────────────────────────────────────────────────────────────────────────│  技能执行   │
                                                                                     │  - 查天气    │
                                                                                     │  - 发消息    │
                                                                                     │  - 定时任务  │
                                                                                     │  - 监控告警  │
                                                                                     └─────────────┘
```

## 🔧 实现方案

### 方案 A: 云端服务透传（推荐）

**优点：**
- ✅ 完整控制对话流程
- ✅ 支持复杂意图识别
- ✅ 可以调用任意 OpenClaw skill

**实现步骤：**

1. **注册天猫精灵开放平台**
   - 网址：https://iap.aligenie.com
   - 创建"标准技能" → 选择"云端服务透传"模板

2. **部署 Webhook 服务**
   ```
   需要：
   - 公网 HTTPS 服务器（阿里云/腾讯云）
   - Node.js 或 Python 运行时
   - 域名和 SSL 证书
   ```

3. **配置 OAuth 2.0（可选）**
   - 如果需要账户绑定

4. **实现意图处理**
   - 解析天猫精灵的 JSON 请求
   - 调用 OpenClaw Gateway API
   - 返回语音响应

### 方案 B: 简单 HTTP 触发（快速原型）

**优点：**
- ✅ 快速搭建
- ✅ 无需复杂配置

**实现：**
- 使用天猫精灵的"场景联动"或"智能家庭"功能
- 通过 HTTP 请求触发 OpenClaw 任务

---

## 💻 Webhook 服务代码示例

### Node.js 版本

```javascript
const express = require('express');
const axios = require('axios');
const app = express();
const PORT = 3000;

app.use(express.json());

// 天猫精灵 webhook 入口
app.post('/aligenie', async (req, res) => {
    const { header, payload } = req.body;
    const intent = payload.intent;
    const slots = payload.slots || {};
    
    let response = '';
    
    // 根据意图调用 OpenClaw
    switch (intent) {
        case 'weather_query':
            response = await callOpenClaw(`查询${slots.city || '北京'}的天气`);
            break;
        case 'schedule_create':
            response = await callOpenClaw(`创建日程：${slots.content}`);
            break;
        case 'monitor_check':
            response = await callOpenClaw('检查 DeepSeek 和 Kimi 的监控状态');
            break;
        default:
            response = await callOpenClaw(payload.query || '你好');
    }
    
    res.json({
        version: '2.0',
        response: {
            output: {
                text: response,
                type: 'PlainText'
            }
        }
    });
});

async function callOpenClaw(message) {
    try {
        const result = await axios.post('http://localhost:18789/agent', {
            message: message,
            channel: 'wecom'
        });
        return result.data.response || '处理完成';
    } catch (error) {
        return 'OpenClaw 暂时无法响应';
    }
}

app.listen(PORT, () => {
    console.log(`Webhook running on port ${PORT}`);
});
```

---

## 🎤 支持的语音指令示例

| 语音指令 | 触发的 Skill | 说明 |
|---------|------------|------|
| "让 OpenClaw 查一下天气" | weather | 查询天气 |
| "提醒我下午三点开会" | cron-mastery | 创建定时提醒 |
| "DeepSeek 有新模型吗" | auto-monitor | 检查监控状态 |
| "给 Jake 发个消息" | wecom-msg | 发送企业微信消息 |
| "运行一下那个监控脚本" | 自定义脚本 | 执行 PowerShell |

---

## 📋 下一步行动

### 立即可做（无需公网服务器）
1. ✅ 使用本地测试工具模拟天猫精灵请求
2. ✅ 创建 OpenClaw skill 来响应特定指令
3. ✅ 测试语音→文本→OpenClaw→响应的完整流程

### 需要公网服务器
1. ⏳ 购买云服务器和域名
2. ⏳ 部署 Webhook 服务
3. ⏳ 在天猫精灵开放平台配置
4. ⏳ 提交审核

---

## 🤖 让 OpenClaw 更智能的建议

1. **创建专用 Skill**
   - `aligenie-bridge` - 专门处理天猫精灵请求
   - 自动识别意图并路由到对应 skill

2. **添加上下文记忆**
   - 记住用户的偏好
   - 支持多轮对话

3. **主动通知**
   - DeepSeek/Kimi 新模型发布时，通过天猫精灵播放通知
   - 定时播报新闻/天气

4. **语音优化**
   - 返回适合语音播放的简洁响应
   - 添加语气词和停顿

---

## ❓ 你现在可以做什么？

**快速开始（推荐）：**
1. 我帮你创建一个本地测试的 Webhook 服务
2. 用 curl/Postman 模拟天猫精灵请求
3. 验证 OpenClaw 响应是否正常

**完整部署：**
1. 准备云服务器（阿里云/腾讯云）
2. 我帮你部署 Webhook 服务
3. 配置天猫精灵开放平台

你想先试哪个方案？👻
