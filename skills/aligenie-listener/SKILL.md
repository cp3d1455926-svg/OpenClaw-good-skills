---
name: aligenie-listener
description: 天猫精灵输入监听器。检查 aligenie-input.txt 文件，调用 OpenClaw 处理，并写入响应结果。
---

# AliGenie Listener - 天猫精灵输入监听器

监听天猫精灵 Webhook 的输入文件，调用 OpenClaw 处理指令。

## 📐 工作原理

```
天猫精灵 → Vercel Webhook → aligenie-input.txt → 本监听器 → OpenClaw → aligenie-output.txt
```

## 🔄 使用方式

### 方式 1: Cron 定时检查

```bash
openclaw cron add --name "天猫精灵监听" --every 1m --system-event "检查 memory/aligenie-input.txt 文件，如果有新内容，调用 OpenClaw 处理并将结果写入 memory/aligenie-output.txt" --session main
```

### 方式 2: 手动触发

```bash
# 检查输入文件
cat memory/aligenie-input.txt

# 调用 OpenClaw 处理
# 结果会自动写入 output 文件
```

## 📁 文件格式

### 输入文件 (aligenie-input.txt)
```json
{
  "message": "查询北京天气",
  "timestamp": "2026-04-04T13:00:00Z",
  "source": "aligenie",
  "webhook": "aligenie-bridge"
}
```

### 输出文件 (aligenie-output.txt)
```
北京市今天晴转多云，气温 15-25°C，空气质量良好。
```

## ⚙️ 配置

### 环境变量（可选）
| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OPENCLAW_CHANNEL` | wecom | 输出消息的渠道 |

## 🎯 支持的指令

所有 OpenClaw 支持的指令都可以：
- 天气查询
- 日程管理
- 消息发送
- 待办事项
- 监控检查
- 通用聊天

## 📝 注意事项

1. **响应时间**：天猫精灵要求 5 秒内响应，Vercel Webhook 会先返回确认消息
2. **异步处理**：OpenClaw 处理完成后，通过企业微信发送结果给用户
3. **文件清理**：处理完成后自动删除输入文件

---

让天猫精灵真正调用 OpenClaw！👻
