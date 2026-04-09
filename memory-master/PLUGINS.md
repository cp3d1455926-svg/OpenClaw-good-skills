# Memory-Master 插件系统

> **扩展你的记忆系统**
> 
> 版本：v4.0.0

---

## 📖 目录

1. [插件概述](#插件概述)
2. [内置插件](#内置插件)
3. [使用插件](#使用插件)
4. [开发插件](#开发插件)
5. [插件市场](#插件市场)

---

## 插件概述

### 什么是插件？

插件是 Memory-Master 的**可选扩展模块**，用于增强核心功能。

**设计理念**：
- ✅ 核心层保持简单（零依赖）
- ✅ 插件层按需扩展（可组合）
- ✅ 热插拔（启用/禁用无需重启）

---

### 插件架构

```
┌─────────────────────────────────────────────────────────┐
│                   Memory-Master Core                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │  核心功能（必须安装）                              │  │
│  │  - 记忆捕捉                                       │  │
│  │  - 基础检索                                       │  │
│  │  - 时间树索引                                     │  │
│  │  - 敏感数据过滤                                   │  │
│  │  - 3 阶段压缩                                      │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  Memory-Master Plugins                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │ time-decay  │ │ top-n-filter│ │  question   │       │
│  │ 时间衰减    │ │ Top-5 过滤   │ │ question 类型│       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │ role-index  │ │   comment   │ │ auto-evolve │       │
│  │ 角色索引    │ │ 双向链接    │ │ 自动进化    │       │
│  └─────────────┘ └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────────────────────┘
```

---

### 插件分类

| 分类 | 说明 | 插件示例 |
|------|------|---------|
| **检索增强** | 增强检索能力 | time-decay, top-n-filter |
| **知识组织** | 增强知识组织 | role-index, comment |
| **查询扩展** | 新增查询类型 | question |
| **自动维护** | 自动维护质量 | auto-evolve |

---

## 内置插件

### 1. time-decay - 时间衰减权重

**功能**：旧记忆权重自动降低，避免干扰新任务。

**安装**：
```bash
npm install @memory-master/plugin-time-decay
```

**使用**：
```typescript
import { TimeDecayPlugin } from '@memory-master/plugin-time-decay';

const plugin = new TimeDecayPlugin({
  decayDays: 30,    // 衰减周期（天）
  minWeight: 0.1,   // 最小权重（0-1）
});

await mm.registerPlugin(plugin);
```

**效果**：
```
记忆权重 = 基础权重 × 时间衰减因子

时间衰减因子：
- 0-7 天：1.0（无衰减）
- 7-30 天：0.5（中度衰减）
- 30+ 天：0.1（重度衰减）
```

**适用场景**：
- ✅ 临时偏好（"今天想吃川菜"）
- ✅ 短期项目（"本周要完成 XXX"）
- ✅ 避免旧信息干扰新任务

---

### 2. top-n-filter - Top-N 过滤

**功能**：只返回最相关的 Top-N 条记忆，避免信息过载。

**安装**：
```bash
npm install @memory-master/plugin-top-n-filter
```

**使用**：
```typescript
import { TopNFilterPlugin } from '@memory-master/plugin-top-n-filter';

const plugin = new TopNFilterPlugin({
  limit: 5,         // 返回数量（默认 5）
  threshold: 0.7,   // 相似度阈值（0-1）
});

await mm.registerPlugin(plugin);
```

**效果**：
```
❌ 无过滤：返回 20 条记忆（信息过载）
✅ Top-5：返回 5 条最相关记忆（精准）

成本降低 60%，效果更好
```

**适用场景**：
- ✅ 检索结果太多
- ✅ 需要精准回答
- ✅ 节省 token

---

### 3. question - question 类型支持

**功能**：支持 question 类型（known unknowns），记录待验证的疑问。

**安装**：
```bash
npm install @memory-master/plugin-question
```

**使用**：
```typescript
import { QuestionPlugin } from '@memory-master/plugin-question';

const plugin = new QuestionPlugin();

await mm.registerPlugin(plugin);
```

**效果**：
```
📝 Questions（待验证的疑问）：
- [ ] "这个行为是否总是成立？"（2026-04-07 提出）
- [ ] "需要什么证据验证？"（2026-04-07 提出）

✅ 已验证：
- [x] "Memory-Master 基于 Karpathy 方法论" 
      → 验证通过（2026-04-07）
```

**适用场景**：
- ✅ 记录待验证的假设
- ✅ 跟踪 known unknowns
- ✅ 避免低信心信息污染

---

### 4. role-index - 角色维度索引

**功能**：按角色组织记忆（类似知乎文章的"分角色"设计）。

**安装**：
```bash
npm install @memory-master/plugin-role-index
```

**使用**：
```typescript
import { RoleIndexPlugin } from '@memory-master/plugin-role-index';

const plugin = new RoleIndexPlugin({
  roles: ['dev', 'user', 'pm'],  // 角色列表
  defaultRole: 'user',            // 默认角色
});

await mm.registerPlugin(plugin);
```

**效果**：
```
├── roles/
│   ├── dev/
│   │   ├── AGENTS.md       # 开发者角色描述
│   │   ├── skills/         # 开发者技能
│   │   └── experience/     # 开发者经验
│   ├── user/
│   │   ├── AGENTS.md       # 用户角色描述
│   │   ├── preferences/    # 用户偏好
│   │   └── habits/         # 用户习惯
│   └── pm/
│       ├── AGENTS.md       # 产品经理角色描述
│       └── projects/       # 项目信息
```

**适用场景**：
- ✅ 多角色协作
- ✅ 知识按角色隔离
- ✅ 不同视角的记忆

---

### 5. comment - 双向链接

**功能**：记忆之间的双向链接（类似知乎文章的"Comment 机制"）。

**安装**：
```bash
npm install @memory-master/plugin-comment
```

**使用**：
```typescript
import { CommentPlugin } from '@memory-master/plugin-comment';

const plugin = new CommentPlugin({
  autoLink: true,     // 自动发现关联（默认 true）
  maxDepth: 3,        // 最大链接深度（默认 3）
});

await mm.registerPlugin(plugin);
```

**效果**：
```
记忆 A（2026-04-06 Memory-Master 发布）
  ├── Comments:
  │   └── 记忆 B（2026-04-07 v4.0 设计）
  │       └── "基于本次发布进行了 v4.0 重构"
  └── References:
      └── 记忆 C（2026-04-05 项目启动）
          └── "项目启动于本日"

🔗 双向链接：A ↔ B ↔ C
```

**适用场景**：
- ✅ 追踪记忆演化历史
- ✅ 建立知识关联
- ✅ 支持复杂查询

---

### 6. auto-evolve - 自动进化

**功能**：从错误中自动进化（类似 EvoSkill）。

**安装**：
```bash
npm install @memory-master/plugin-auto-evolve
```

**使用**：
```typescript
import { AutoEvolvePlugin } from '@memory-master/plugin-auto-evolve';

const plugin = new AutoEvolvePlugin({
  learnFromErrors: true,   // 从错误中学习（默认 true）
  minConfidence: 0.8,      // 最小置信度（默认 0.8）
});

await mm.registerPlugin(plugin);
```

**效果**：
```
🔄 自动进化记录：

2026-04-07 18:00:
  错误：检索结果不准确
  原因：索引未更新
  学习：检索前先重建索引
  新规则：retrieve() → rebuildIndex() → retrieve()

2026-04-07 18:05:
  错误：压缩失败
  原因：磁盘空间不足
  学习：压缩前检查磁盘空间
  新规则：compact() → checkDiskSpace() → compact()
```

**适用场景**：
- ✅ 从错误中学习
- ✅ 自动优化流程
- ✅ 持续改进系统

---

## 使用插件

### 启用插件

```typescript
import { MemoryMaster } from 'memory-master';
import { TimeDecayPlugin } from '@memory-master/plugin-time-decay';

const mm = new MemoryMaster();

// 注册插件
await mm.registerPlugin(new TimeDecayPlugin({ decayDays: 30 }));

// 使用插件功能
const result = await mm.retrieve('xxx', {
  plugins: {
    'time-decay': { enabled: true },
  },
});
```

---

### 禁用插件

```typescript
// 禁用特定插件
await mm.unregisterPlugin('time-decay');

// 临时禁用
const result = await mm.retrieve('xxx', {
  plugins: {
    'time-decay': { enabled: false },
  },
});
```

---

### 插件配置

```typescript
// 全局配置
await mm.configurePlugin('time-decay', {
  decayDays: 60,    // 修改衰减周期
  minWeight: 0.2,   // 修改最小权重
});

// 单次配置
const result = await mm.retrieve('xxx', {
  plugins: {
    'time-decay': {
      decayDays: 7,  // 仅本次查询使用 7 天衰减
    },
  },
});
```

---

### 插件优先级

```typescript
// 设置插件优先级（数字越小优先级越高）
await mm.registerPlugin(new TimeDecayPlugin(), { priority: 1 });
await mm.registerPlugin(new TopNFilterPlugin(), { priority: 2 });

// 执行顺序：time-decay → top-n-filter
```

---

## 开发插件

### 插件接口

```typescript
interface Plugin {
  // 基本信息
  name: string;
  version: string;
  description?: string;
  
  // 生命周期
  init(mm: MemoryMaster): Promise<void>;
  destroy(): Promise<void>;
  
  // 钩子函数（可选）
  hooks?: {
    beforeCapture?: (content: string) => Promise<string>;
    afterCapture?: (result: CaptureResult) => Promise<void>;
    beforeRetrieve?: (query: string) => Promise<string>;
    afterRetrieve?: (result: RetrieveResult) => Promise<RetrieveResult>;
    beforeCompact?: () => Promise<void>;
    afterCompact?: (result: CompactResult) => Promise<void>;
  };
}
```

---

### 开发示例

```typescript
// my-plugin.ts
import { Plugin, MemoryMaster, CaptureResult } from 'memory-master';

export class MyPlugin implements Plugin {
  name = 'my-plugin';
  version = '1.0.0';
  description = '我的自定义插件';
  
  private mm?: MemoryMaster;
  
  async init(mm: MemoryMaster): Promise<void> {
    this.mm = mm;
    console.log('MyPlugin 已初始化');
  }
  
  async destroy(): Promise<void> {
    console.log('MyPlugin 已销毁');
  }
  
  hooks = {
    async beforeCapture(content: string): Promise<string> {
      // 在捕捉前处理内容
      return content.toUpperCase();
    },
    
    async afterCapture(result: CaptureResult): Promise<void> {
      // 在捕捉后执行
      console.log('捕捉完成:', result.id);
    },
  };
}
```

---

### 发布插件

**1. 准备 package.json**：
```json
{
  "name": "@memory-master/plugin-my-plugin",
  "version": "1.0.0",
  "description": "我的自定义插件",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "keywords": ["memory-master", "plugin"],
  "peerDependencies": {
    "memory-master": "^4.0.0"
  }
}
```

**2. 构建**：
```bash
npm run build
```

**3. 发布**：
```bash
npm publish --access public
```

**4. 添加到插件市场**：
编辑 [PLUGINS.md](#插件市场)，添加你的插件。

---

## 插件市场

### 官方插件

| 插件 | 版本 | 说明 | 安装 |
|------|------|------|------|
| **time-decay** | 1.0.0 | 时间衰减权重 | `npm install @memory-master/plugin-time-decay` |
| **top-n-filter** | 1.0.0 | Top-5 过滤 | `npm install @memory-master/plugin-top-n-filter` |
| **question** | 1.0.0 | question 类型 | `npm install @memory-master/plugin-question` |
| **role-index** | 1.0.0 | 角色索引 | `npm install @memory-master/plugin-role-index` |
| **comment** | 1.0.0 | 双向链接 | `npm install @memory-master/plugin-comment` |
| **auto-evolve** | 1.0.0 | 自动进化 | `npm install @memory-master/plugin-auto-evolve` |

---

### 社区插件

| 插件 | 作者 | 说明 | 安装 |
|------|------|------|------|
| *等你来提交!* | | | |

**提交社区插件**：
1. Fork 仓库
2. 添加你的插件到列表
3. 提交 PR

---

### 插件开发模板

```bash
# 使用模板创建插件
npx degit memory-master/plugin-template my-plugin
cd my-plugin
npm install
npm run dev
```

---

## 📚 相关文档

- [设计文档](./DESIGN_v4.md) - 架构设计详解
- [API 参考](./API.md) - 完整 API 文档
- [使用教程](./TUTORIAL.md) - 完整使用指南
- [快速上手](./QUICKSTART.md) - 5 分钟入门

---

*插件文档完成时间：2026-04-07 18:07*  
*版本：v4.0.0*  
*基于 Karpathy + Anthropic + Claude Code*
