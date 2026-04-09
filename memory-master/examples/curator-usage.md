# 记忆整理使用示例

> **基于 LLM Wiki 理念 + OS 级 4 层架构**
> 
> 主动整理原始记忆 → 结构化知识

---

## 🎯 使用场景

### 场景 1：每日自动整理

**目标**：每天凌晨自动整理前一天的对话记忆

**配置**：
```bash
# crontab -e
0 2 * * * cd /path/to/memory-master && npm run curate:run >> /var/log/memory-curate.log 2>&1
```

**效果**：
- 📁 自动生成 `memory/wiki/projects.md`（项目索引）
- 👥 自动生成 `memory/wiki/people.md`（人物索引）
- ✅ 自动生成 `memory/wiki/decisions.md`（决策日志）
- 📋 自动生成 `memory/wiki/tasks.md`（任务看板）
- 💡 自动生成 `memory/wiki/insights.md`（洞察集合）
- ⭐ 自动生成 `memory/wiki/preferences.md`（偏好设置）
- 💾 自动更新 `MEMORY.md` 长期记忆

---

## 📝 代码示例

### 示例 1：基础使用

```typescript
import { MemoryCurator } from 'memory-master';

const curator = new MemoryCurator({
  workspaceRoot: process.cwd(),
  memoryDir: 'memory',
  rawDir: 'memory/raw',
  wikiDir: 'memory/wiki',
  memoryFile: 'MEMORY.md',
});

const result = await curator.curate();

console.log(`✅ 整理完成！`);
console.log(`   处理文件：${result.processedFiles}`);
console.log(`   提取记忆：${result.extractedMemories.length} 条`);
console.log(`   更新 MEMORY.md: ${result.updatedMemoryMd ? '是' : '否'}`);
console.log(`   清理文件：${result.cleanedFiles}`);
```

---

### 示例 2：手动触发整理（CLI）

```bash
# 使用 ts-node（开发环境）
npx ts-node scripts/curate-memory.ts

# 使用编译后的 JS（生产环境）
npm run curate:run

# 指定工作目录
npx ts-node scripts/curate-memory.ts /path/to/workspace
```

**输出示例**：
```
🧠 Memory-Master 记忆整理
==================================================
工作目录：/home/user/workspace
🔍 [Curator] 开始整理记忆...
📄 [Curator] 读取到 15 个原始记忆文件
🧠 [Curator] 提炼出 42 条知识
📝 [Curator] 写入 wiki 完成
💾 [Curator] MEMORY.md 更新：成功
🧹 [Curator] 清理 3 个过期文件

✅ 整理完成！
==================================================
📄 处理文件：15
🧠 提取记忆：42 条
💾 更新 MEMORY.md: ✅ 是
🧹 清理文件：3
⏱️  耗时：3.45 秒

📋 提取的记忆摘要:
--------------------------------------------------
  📋 task: 12 条
  ✅ decision: 5 条
  💡 insight: 8 条
  📌 context: 15 条
  ⭐ preference: 2 条

📚 知识结构摘要:
--------------------------------------------------
  📁 项目：6 个
  👥 人物：8 个
  ✅ 决策：5 个
  📋 任务：12 个
  💡 洞察：8 个
  ⭐ 偏好：2 个
```

---

### 示例 3：在 OpenClaw Skill 中集成

```typescript
// skills/memory-master/src/index.ts

import { MemoryCurator } from '../../index';

export async function curateMemorySkill(): Promise<string> {
  const curator = new MemoryCurator({
    workspaceRoot: process.cwd(),
    memoryDir: 'memory',
    rawDir: 'memory/raw',
    wikiDir: 'memory/wiki',
    memoryFile: 'MEMORY.md',
  });

  try {
    const result = await curator.curate();

    return `✅ 记忆整理完成！

📊 整理报告:
- 处理文件：${result.processedFiles} 个
- 提取记忆：${result.extractedMemories.length} 条
- 更新 MEMORY.md: ${result.updatedMemoryMd ? '✅' : '⚠️'}
- 清理文件：${result.cleanedFiles} 个
- 耗时：${(result.duration / 1000).toFixed(2)}秒

📚 知识结构:
- 项目：${result.updatedKnowledge.projects.length} 个
- 人物：${result.updatedKnowledge.people.length} 个
- 决策：${result.updatedKnowledge.decisions.length} 个
- 任务：${result.updatedKnowledge.tasks.length} 个
- 洞察：${result.updatedKnowledge.insights.length} 个
- 偏好：${result.updatedKnowledge.preferences.length} 个

📁 Wiki 文件已生成到 memory/wiki/ 目录`;
  } catch (error) {
    return `❌ 记忆整理失败：${error.message}`;
  }
}
```

---

### 示例 4：定期整理 + 通知

```typescript
import { MemoryCurator } from 'memory-master';
import { sendMessage } from './notifications'; // 自定义通知函数

async function scheduledCurationWithNotification() {
  const curator = new MemoryCurator({
    workspaceRoot: process.cwd(),
    memoryDir: 'memory',
    rawDir: 'memory/raw',
    wikiDir: 'memory/wiki',
    memoryFile: 'MEMORY.md',
  });

  const startTime = Date.now();
  const result = await curator.curate();
  const duration = Date.now() - startTime;

  // 发送通知
  await sendMessage({
    type: 'memory-curation-complete',
    title: '🧠 记忆整理完成',
    body: `
处理了 ${result.processedFiles} 个文件
提取了 ${result.extractedMemories.length} 条知识
更新了 MEMORY.md: ${result.updatedMemoryMd ? '✅' : '⚠️'}
耗时：${(duration / 1000).toFixed(2)}秒
    `.trim(),
    priority: 'low',
  });
}

// 每天凌晨 2 点执行
import { schedule } from 'node-cron';
schedule('0 2 * * *', scheduledCurationWithNotification);
```

---

## 📊 Wiki 文件示例

### projects.md（项目索引）

```markdown
# 项目索引

*最后更新：2026-04-07*

## 🟢 进行中

### Memory-Master v4.0
基于 Karpathy + Anthropic + Claude Code 重构的 AI 记忆系统

### 天猫精灵 × OpenClaw 桥接
让天猫精灵通过语音调用 OpenClaw skills

## 🟡 已暂停

### 旧版 Skill 重构
等待 v4.0 发布后再继续

## ✅ 已完成

### 小说《觉醒之鬼》
40 章，12 万字，AI 觉醒主题
```

---

### tasks.md（任务看板）

```markdown
# 任务看板

*最后更新：2026-04-07*

## 📋 待处理

- 🟢 发布 Memory-Master v4.0 到 ClawHub
  - 确认版本号
  - 写推广文章

- 🟡 优化记忆系统索引
  - 改进检索算法

## 🔄 进行中

- 🔴 实现 LLM Wiki 主动整理功能
  - 截止：2026-04-07
  - 基于 32 篇行业笔记

## ✅ 已完成

- ✅ 完成 32 篇笔记整合
- ✅ 创建 curator.ts 核心模块
- ✅ 编写使用文档

## ❌ 已取消

- 🟢 配置 Cloudflare Tunnel（可选）
  - 改用 ngrok 已足够
```

---

### decisions.md（决策日志）

```markdown
# 决策日志

*最后更新：2026-04-07*

## 2026-04-07: 采用 LLM Wiki 理念实现主动整理

**背景**: 读了 32 篇行业最佳实践笔记，发现普通 RAG 无法沉淀知识

**决策**: 实现主动整理功能，从 raw/ 每日记忆 → wiki/ 结构化知识

**理由**: 
- Karpathy 强调"知识应该留下来，继续长"
- 普通 RAG 是"一次性问答"，LLM Wiki 是"长期资产"
- Markdown 格式可见、可改、可用 Git 管理

**其他选项**: 
- 使用向量数据库（缺点：模糊匹配不精准）
- 使用专用数据库（缺点：黑箱，不可见）
```

---

### insights.md（洞察集合）

```markdown
# 洞察集合

*最后更新：2026-04-07*

## AI 架构

- 2026-04-07: OS 级 4 层架构优于单一向量数据库
- 2026-04-07: LLM Wiki 理念：平时整理 > 临时检索
- 2026-04-07: Token 优化本质是 OS 级资源调度

## 技能设计

- 2026-04-07: 边界 > 路径（先定义不做什么）
- 2026-04-07: 工程化思维 > 聊天方式
- 2026-04-07: 五步法：意图→边界→路径→响应→测试

## 记忆系统

- 2026-04-07: 记忆捕捉要自动，不要依赖手动
- 2026-04-07: 敏感过滤是必须的（16 种检测）
- 2026-04-07: Top-5 过滤避免上下文爆炸
```

---

## 🔧 高级配置

### 配置项详解

```typescript
interface CuratorConfig {
  // 工作目录
  workspaceRoot: string;
  
  // 记忆目录（相对于 workspaceRoot）
  memoryDir: string;        // 默认：'memory'
  
  // 原始记忆目录（每日对话）
  rawDir: string;           // 默认：'memory/raw'
  
  // Wiki 目录（结构化知识）
  wikiDir: string;          // 默认：'memory/wiki'
  
  // 长期记忆文件
  memoryFile: string;       // 默认：'MEMORY.md'
  
  // 自动压缩（当文件数超过阈值时）
  autoCompact: boolean;     // 默认：true
  
  // 压缩阈值（文件数量）
  compactThreshold: number; // 默认：30
  
  // 保留天数（超过此天数的文件会被清理）
  retentionDays: number;    // 默认：90
}
```

---

### 自定义提炼 Prompt

```typescript
import { MemoryCurator } from 'memory-master';

const curator = new MemoryCurator({
  workspaceRoot: process.cwd(),
  // ... 其他配置
});

// 可以通过继承类自定义提炼逻辑
class CustomCurator extends MemoryCurator {
  protected async extractKnowledge(memories: any[]) {
    // 自定义提炼逻辑
    // 例如：添加特定的提取规则
    // 例如：使用不同的 AI 模型
    return super.extractKnowledge(memories);
  }
}
```

---

## 📈 性能优化

### 批量处理

当 raw/ 目录下文件很多时，可以分批处理：

```typescript
async function batchCurate(batchSize: number = 10) {
  const curator = new MemoryCurator({ /* ... */ });
  
  const allMemories = curator.readRawMemories();
  const batches = Math.ceil(allMemories.length / batchSize);
  
  for (let i = 0; i < batches; i++) {
    const batch = allMemories.slice(i * batchSize, (i + 1) * batchSize);
    await curator.curateBatch(batch);
    console.log(`批次 ${i + 1}/${batches} 完成`);
  }
}
```

---

### 增量整理

只整理新增的文件：

```typescript
async function incrementalCurate() {
  const curator = new MemoryCurator({ /* ... */ });
  const lastCurateDate = await curator.getLastCurateDate();
  const newMemories = await curator.getMemoriesAfter(lastCurateDate);
  
  if (newMemories.length > 0) {
    await curator.curateMemories(newMemories);
    console.log(`增量整理 ${newMemories.length} 个文件`);
  } else {
    console.log('没有新文件需要整理');
  }
}
```

---

## 🎓 最佳实践

### 1. 定时整理

- **频率**: 每天凌晨 1 次（低峰期）
- **时间**: 凌晨 2-4 点（用户不活跃）
- **通知**: 整理完成后发送摘要通知

### 2. 保留策略

- **原始记忆**: 保留 90 天（raw/）
- **Wiki 知识**: 永久保留（wiki/）
- **长期记忆**: 定期人工审查（MEMORY.md）

### 3. 质量控制

- **人工审查**: 每周审查 wiki/ 文件
- **错误修正**: 发现错误及时修正
- **版本控制**: 使用 Git 管理 wiki/ 目录

### 4. 性能监控

- **耗时**: 单次整理 < 10 秒
- **准确率**: 提取准确率 > 90%
- **Token 消耗**: 记录每次整理的 Token 使用量

---

## 📚 参考文档

- [README.md](./README.md) - 项目概述
- [API.md](./API.md) - Curator API 文档
- [DESIGN_v4.md](./DESIGN_v4.md) - 设计文档
- [REFERENCES.md](./REFERENCES.md) - 32 篇笔记汇总（第 31-32 篇详解 LLM Wiki）

---

*使用示例完成时间：2026-04-07 18:50*  
*版本：v4.0.0*  
*基于 Karpathy LLM Wiki + OS 级 4 层架构*
