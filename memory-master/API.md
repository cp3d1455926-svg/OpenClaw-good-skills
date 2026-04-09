# Memory-Master API 参考文档

> **完整 API 文档**
> 
> 版本：v4.0.0

---

## 📖 目录

1. [快速开始](#快速开始)
2. [核心 API](#核心-api)
3. [查询类型](#查询类型)
4. [记忆模型](#记忆模型)
5. [插件 API](#插件-api)
6. [错误处理](#错误处理)

---

## 快速开始

### 导入模块

```typescript
import { MemoryMaster } from 'memory-master';

const mm = new MemoryMaster({
  apiKey: process.env.BAILIAN_API_KEY,
  model: 'qwen3.5-plus',
});
```

### 基本使用

```typescript
// 捕捉记忆
await mm.capture('记住，我每天早上 7 点起床');

// 检索记忆
const result = await mm.retrieve('我什么时候起床？');
console.log(result.content); // "你每天早上 7 点起床"

// 压缩记忆
await mm.compact();
```

---

## 核心 API

### capture() - 捕捉记忆

捕捉一条新记忆。

**签名**：
```typescript
capture(
  content: string,
  options?: CaptureOptions
): Promise<CaptureResult>
```

**参数**：
```typescript
interface CaptureOptions {
  type?: '情景' | '语义' | '程序' | '人设'; // 记忆类型
  metadata?: {
    source?: string;      // 来源（会话 ID）
    timestamp?: number;   // 时间戳
    topic?: string;       // 主题
    project?: string;     // 项目
  };
  skipFilter?: boolean;   // 跳过敏感数据过滤（默认 false）
}
```

**返回**：
```typescript
interface CaptureResult {
  success: boolean;
  id: string;             // 记忆 ID
  type: string;           // 记忆类型
  filtered?: string[];    // 被过滤的敏感数据
  path: string;           // 存储路径
}
```

**示例**：
```typescript
const result = await mm.capture('记住，我每天早上 7 点起床', {
  type: '人设',
  metadata: {
    source: 'session-123',
    topic: '生活习惯',
  },
});

console.log(result);
// {
//   success: true,
//   id: 'mem-20260407-001',
//   type: '人设',
//   path: 'MEMORY.md'
// }
```

---

### retrieve() - 检索记忆

检索相关记忆。

**签名**：
```typescript
retrieve(
  query: string,
  options?: RetrieveOptions
): Promise<RetrieveResult>
```

**参数**：
```typescript
interface RetrieveOptions {
  type?: 'procedural' | 'temporal' | 'relational' | 'persona' | 'factual';
  limit?: number;         // 返回数量（默认 5）
  timeRange?: {
    start?: string;       // 开始日期
    end?: string;         // 结束日期
  };
  includeRaw?: boolean;   // 包含原始记录（默认 false）
}
```

**返回**：
```typescript
interface RetrieveResult {
  success: boolean;
  queryType: string;      // 查询类型
  memories: Memory[];     // 匹配的记忆
  knowledgeGraph?: {      // 知识图谱关联
    nodes: Node[];
    edges: Edge[];
  };
  timeMs: number;         // 查询耗时
}
```

**示例**：
```typescript
const result = await mm.retrieve('昨天讨论了什么？', {
  type: 'temporal',
  limit: 10,
});

console.log(result.memories);
// [
//   {
//     id: 'mem-20260406-001',
//     content: '讨论了 Memory-Master v3.2.0 发布',
//     type: '情景',
//     timestamp: 1712476800000,
//   },
//   ...
// ]
```

---

### compact() - 压缩记忆

压缩记忆，节省 token。

**签名**：
```typescript
compact(options?: CompactOptions): Promise<CompactResult>
```

**参数**：
```typescript
interface CompactOptions {
  force?: boolean;        // 强制压缩（默认 false）
  level?: 'L1' | 'L2' | 'L3'; // 压缩级别
  dryRun?: boolean;       // 仅预览，不执行（默认 false）
}
```

**返回**：
```typescript
interface CompactResult {
  success: boolean;
  compressed: number;     // 压缩的记忆数
  savedTokens: number;    // 节省的 token 数
  compressionRate: number; // 压缩率（0-1）
}
```

**示例**：
```typescript
const result = await mm.compact({
  level: 'L2',
  dryRun: true,
});

console.log(result);
// {
//   success: true,
//   compressed: 15,
//   savedTokens: 2340,
//   compressionRate: 0.52
// }
```

---

### filter() - 敏感数据过滤

检测并过滤敏感数据。

**签名**：
```typescript
filter(content: string): Promise<FilterResult>
```

**返回**：
```typescript
interface FilterResult {
  hasSensitive: boolean;
  filtered: string;       // 过滤后的内容
  detected: {
    type: string;         // 敏感数据类型
    value: string;        // 检测到的值（脱敏）
    position: number;     // 位置
  }[];
}
```

**示例**：
```typescript
const result = await mm.filter('我的密码是 123456，API Key 是 sk-xxx');

console.log(result);
// {
//   hasSensitive: true,
//   filtered: '我的密码是 [FILTERED]，API Key 是 [FILTERED]',
//   detected: [
//     { type: 'password', value: '12****', position: 5 },
//     { type: 'api_key', value: 'sk-***', position: 15 }
//   ]
// }
```

---

### query() - 复杂查询

执行复杂 QA，综合多个记忆生成深度回答。

**签名**：
```typescript
query(
  question: string,
  options?: QueryOptions
): Promise<QueryResult>
```

**参数**：
```typescript
interface QueryOptions {
  depth?: 'shallow' | 'deep'; // 查询深度（默认 'deep'）
  includeGraph?: boolean;     // 包含知识图谱（默认 true）
  writeBack?: boolean;        // 结果回写（默认 true）
}
```

**返回**：
```typescript
interface QueryResult {
  success: boolean;
  answer: string;         // 综合回答
  sources: Memory[];      // 引用的记忆
  knowledgeGraph?: {      // 知识图谱
    nodes: Node[];
    edges: Edge[];  };
  timeMs: number;         // 查询耗时
}
```

**示例**：
```typescript
const result = await mm.query(
  'Memory-Master 项目为什么选择 Karpathy 方法论？',
  { depth: 'deep' }
);

console.log(result.answer);
// "Memory-Master 选择 Karpathy 方法论是因为它解决了传统 RAG 
// 没有累积效应的问题..."
```

---

## 查询类型

### procedural - 流程查询

查询"如何做 XXX"。

**示例**：
```typescript
await mm.retrieve('如何安装 Memory-Master？', {
  type: 'procedural',
});
```

**返回**：
```
📋 安装流程：
1. 克隆仓库：git clone ...
2. 安装依赖：npm install
3. 配置 API Key：编辑 .env
4. 运行测试：npm test
```

---

### temporal - 时间查询

查询"什么时候/昨天/上周"。

**示例**：
```typescript
await mm.retrieve('昨天讨论了什么？', {
  type: 'temporal',
  timeRange: {
    start: '2026-04-06',
    end: '2026-04-06',
  },
});
```

**返回**：
```
📅 2026-04-06 的讨论记录：
1. Memory-Master v3.2.0 发布
2. 讨论了 5 阶段智能压缩
3. 敏感数据过滤测试通过率 100%
```

---

### relational - 关系查询

查询"XXX 和 YYY 有什么关系"。

**示例**：
```typescript
await mm.retrieve('Jake 和 Memory-Master 项目有什么关系？', {
  type: 'relational',
});
```

**返回**：
```
🔗 关系图谱：
Jake（人设）
  └── 创建者 → Memory-Master 项目（项目）
      └── 基于 → Karpathy 方法论（知识）
```

---

### persona - 偏好查询

查询"用户喜欢/偏好什么"。

**示例**：
```typescript
await mm.retrieve('我喜欢什么样的回答？', {
  type: 'persona',
});
```

**返回**：
```
🎯 你的偏好：
- 简洁明了，不要太长
- 喜欢用 emoji
- 偏好结构化回答（列表/表格）
```

---

### factual - 事实查询

查询"事实性问题"。

**示例**：
```typescript
await mm.retrieve('我下周要参加什么？', {
  type: 'factual',
});
```

**返回**：
```
📝 即将到来的事件：
- 2026-04-14：重要会议
- 2026-04-15：项目评审
```

---

## 主动整理 API（LLM Wiki 理念）

### MemoryCurator 类

记忆整理员，基于 LLM Wiki 理念 + OS 级 4 层架构，主动整理原始记忆 → 结构化知识。

**导入**：
```typescript
import { MemoryCurator } from 'memory-master';
```

**初始化**：
```typescript
const curator = new MemoryCurator({
  workspaceRoot: '/path/to/workspace',
  memoryDir: 'memory',
  rawDir: 'memory/raw',    // 原始每日记忆
  wikiDir: 'memory/wiki',  // 结构化知识
  memoryFile: 'MEMORY.md',
  autoCompact: true,       // 自动压缩
  compactThreshold: 30,    // 文件数量阈值
  retentionDays: 90,       // 保留天数
});
```

---

### curate() - 执行整理

执行完整整理流程。

**签名**：
```typescript
curate(): Promise<CurationResult>
```

**返回**：
```typescript
interface CurationResult {
  processedFiles: number;      // 处理的文件数
  extractedMemories: MemoryItem[];  // 提取的记忆项
  updatedKnowledge: CuratedKnowledge; // 更新的知识结构
  updatedMemoryMd: boolean;    // MEMORY.md 是否更新
  cleanedFiles: number;        // 清理的文件数
  duration: number;            // 耗时（毫秒）
}
```

**示例**：
```typescript
const result = await curator.curate();

console.log(`处理 ${result.processedFiles} 个文件`);
console.log(`提取 ${result.extractedMemories.length} 条记忆`);
console.log(`更新 MEMORY.md: ${result.updatedMemoryMd ? '是' : '否'}`);
console.log(`清理 ${result.cleanedFiles} 个过期文件`);
console.log(`耗时：${(result.duration / 1000).toFixed(2)}秒`);
```

---

### 知识结构（CuratedKnowledge）

整理后生成的结构化知识。

```typescript
interface CuratedKnowledge {
  projects: ProjectInfo[];    // 项目信息
  people: PersonInfo[];       // 人物信息
  decisions: DecisionInfo[];  // 决策信息
  tasks: TaskInfo[];          // 任务信息
  insights: InsightInfo[];    // 洞察信息
  preferences: PreferenceInfo[]; // 偏好信息
}
```

**项目信息**：
```typescript
interface ProjectInfo {
  name: string;              // 项目名称
  status: 'active' | 'paused' | 'completed';
  description: string;       // 项目描述
  lastUpdated: string;       // 最后更新日期
  relatedFiles?: string[];   // 相关文件
}
```

**人物信息**：
```typescript
interface PersonInfo {
  name: string;              // 人名
  role?: string;             // 角色
  context: string;           // 相关上下文
  lastMentioned: string;     // 最后提及日期
}
```

**决策信息**：
```typescript
interface DecisionInfo {
  id: string;                // 决策 ID
  date: string;              // 决策日期
  context: string;           // 决策背景
  decision: string;          // 决策内容
  reasoning: string;         // 决策理由
  alternatives?: string[];   // 其他选项
}
```

**任务信息**：
```typescript
interface TaskInfo {
  id: string;                // 任务 ID
  title: string;             // 任务标题
  status: 'pending' | 'in-progress' | 'completed' | 'cancelled';
  priority: 'high' | 'medium' | 'low';
  dueDate?: string;          // 截止日期
  context: string;           // 任务上下文
}
```

---

### 生成的 Wiki 文件

整理后会在 `memory/wiki/` 目录下生成以下文件：

| 文件 | 说明 |
|------|------| ---|
| `projects.md` | 项目索引（按状态分类） |
| `people.md` | 人物索引 |
| `decisions.md` | 决策日志 |
| `tasks.md` | 任务看板（按状态分类） |
| `insights.md` | 洞察集合（按分类） |
| `preferences.md` | 偏好设置（按分类） |

---

### Cron 定时整理

**Linux/macOS**：
```bash
# 每天凌晨 2 点自动整理
0 2 * * * cd /path/to/memory-master && npm run curate:run
```

**Windows 任务计划程序**：
```powershell
# 创建定时任务
$action = New-ScheduledTaskAction -Execute "npm" -Argument "run curate:run" -WorkingDirectory "C:\path\to\memory-master"
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -TaskName "MemoryMaster-Curate" -Action $action -Trigger $trigger
```

---

### 使用示例：完整工作流

```typescript
import { MemoryCurator } from 'memory-master';

async function dailyCuration() {
  const curator = new MemoryCurator({
    workspaceRoot: process.cwd(),
    memoryDir: 'memory',
    rawDir: 'memory/raw',
    wikiDir: 'memory/wiki',
    memoryFile: 'MEMORY.md',
    retentionDays: 90,
  });

  console.log('🧠 开始记忆整理...');
  
  const result = await curator.curate();
  
  console.log('✅ 整理完成！');
  console.log(`   处理文件：${result.processedFiles}`);
  console.log(`   提取记忆：${result.extractedMemories.length} 条`);
  console.log(`   更新 MEMORY.md: ${result.updatedMemoryMd ? '✅' : '⚠️'}`);
  console.log(`   清理文件：${result.cleanedFiles}`);
  console.log(`   耗时：${(result.duration / 1000).toFixed(2)}秒`);
}

// 手动执行
dailyCuration();
```

---

## 记忆模型

### Memory 接口

```typescript
interface Memory {
  id: string;             // 唯一 ID
  type: '情景' | '语义' | '程序' | '人设';
  content: string;        // 记忆内容
  timestamp: number;      // 创建时间戳
  metadata: {
    source?: string;
    topic?: string;
    project?: string;
  };
  references?: string[];  // 交叉引用 ID 列表
}
```

---

### 记忆类型详解

| 类型 | 说明 | 存储位置 | 加载策略 |
|------|------|---------|---------|
| **情景** | 具体事件、对话记录 | memory/YYYY-MM-DD.md | 按需加载 |
| **语义** | 提炼的知识、概念 | MEMORY.md#语义 | 按需加载 |
| **程序** | 操作技能、流程 | MEMORY.md#程序 | 常驻加载 |
| **人设** | 用户偏好、习惯 | MEMORY.md#人设 | 常驻加载 |

---

## 插件 API

### 插件接口

```typescript
interface Plugin {
  name: string;
  version: string;
  init(mm: MemoryMaster): Promise<void>;
  destroy(): Promise<void>;
}
```

---

### 注册插件

```typescript
import { TimeDecayPlugin } from 'memory-master-plugin-time-decay';

const plugin = new TimeDecayPlugin({
  decayDays: 30,    // 衰减周期
  minWeight: 0.1,   // 最小权重
});

await mm.registerPlugin(plugin);
```

---

### 内置插件

| 插件 | 说明 | 使用示例 |
|------|------|---------|
| **time-decay** | 时间衰减权重 | `new TimeDecayPlugin({ decayDays: 30 })` |
| **top-n-filter** | Top-5 过滤 | `new TopNFilterPlugin({ limit: 5 })` |
| **question** | question 类型支持 | `new QuestionPlugin()` |
| **role-index** | 角色维度索引 | `new RoleIndexPlugin({ roles: ['dev', 'user'] })` |
| **comment** | 双向链接 | `new CommentPlugin()` |
| **auto-evolve** | 自动进化 | `new AutoEvolvePlugin()` |

---

## 错误处理

### 错误类型

```typescript
enum MemoryError {
  NOT_FOUND = 'MEMORY_NOT_FOUND',      // 记忆不存在
  ALREADY_EXISTS = 'MEMORY_ALREADY_EXISTS', // 记忆已存在
  FILTER_FAILED = 'FILTER_FAILED',     // 过滤失败
  COMPACT_FAILED = 'COMPACT_FAILED',   // 压缩失败
  QUERY_FAILED = 'QUERY_FAILED',       // 查询失败
  PLUGIN_ERROR = 'PLUGIN_ERROR',       // 插件错误
}
```

---

### 错误处理示例

```typescript
import { MemoryError } from 'memory-master';

try {
  await mm.retrieve('不存在的记忆');
} catch (error) {
  if (error.code === MemoryError.NOT_FOUND) {
    console.log('记忆不存在');
  } else if (error.code === MemoryError.QUERY_FAILED) {
    console.log('查询失败:', error.message);
  } else {
    throw error;
  }
}
```

---

### 错误码对照表

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| `MEMORY_NOT_FOUND` | 记忆不存在 | 检查记忆 ID 是否正确 |
| `MEMORY_ALREADY_EXISTS` | 记忆已存在 | 使用 update() 而非 create() |
| `FILTER_FAILED` | 过滤失败 | 检查敏感数据格式 |
| `COMPACT_FAILED` | 压缩失败 | 检查磁盘空间 |
| `QUERY_FAILED` | 查询失败 | 检查 API Key 和网络 |
| `PLUGIN_ERROR` | 插件错误 | 检查插件版本兼容性 |

---

## 📚 相关文档

- [设计文档](./DESIGN_v4.md) - 架构设计详解
- [使用教程](./TUTORIAL.md) - 完整使用指南
- [快速上手](./QUICKSTART.md) - 5 分钟入门
- [插件系统](./PLUGINS.md) - 插件开发指南

---

*API 文档完成时间：2026-04-07 18:06*  
*版本：v4.0.0*  
*基于 Karpathy + Anthropic + Claude Code*
