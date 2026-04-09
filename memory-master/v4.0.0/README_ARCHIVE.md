# Memory-Master v4.0.0 存档

> **存档日期**: 2026-04-07  
> **版本**: v4.0.0  
> **状态**: ⚠️ 历史版本，已归档

---

## 📦 版本信息

### 核心功能
- ✅ LLM Wiki 主动整理
- ✅ OS 级 4 层架构
- ✅ 记忆整理员（Curator）
- ✅ 技能自进化
- ✅ Token 优化（65% 节省）
- ✅ 敏感过滤（16 种检测）

### 性能指标
- **检索准确率**: 75%
- **Token 节省**: 65%
- **响应时间**: 70ms
- **记忆加载**: 180ms

### 文件大小
- **源代码**: ~86KB (11 个文件)
- **文档**: ~55KB (8 个文件)
- **总计**: ~155KB

---

## 📁 目录结构

```
v4.0.0/
├── src/                      # 源代码
│   ├── index.ts              # MemoryMaster 主类
│   ├── capture.ts            # 记忆捕捉
│   ├── retrieve.ts           # 记忆检索
│   ├── compact.ts            # 记忆压缩
│   ├── filter.ts             # 敏感过滤
│   ├── token-optimizer.ts    # Token 优化
│   ├── skill-evolver.ts      # 技能自进化
│   ├── benchmark.ts          # 评测基准
│   └── curator.ts            # 记忆整理员 ⭐
├── scripts/                  # 脚本
│   └── curate-memory.ts      # 整理脚本 ⭐
├── examples/                 # 示例
│   └── curator-usage.md      # 整理功能示例
├── test/                     # 测试
│   └── simple.test.ts        # 简单测试
├── memory/                   # 记忆目录（运行时生成）
├── package.json              # 项目配置
├── tsconfig.json             # TS 配置
├── README.md                 # 项目概述
├── QUICKSTART.md             # 快速上手
├── TUTORIAL.md               # 使用教程
├── API.md                    # API 参考
├── PLUGINS.md                # 插件系统
├── DESIGN_v4.md              # 设计文档
├── REFERENCES.md             # 32 篇笔记汇总
├── SKILL.md                  # ClawHub 技能描述
├── IMPLEMENTATION_COMPLETE.md # 实现报告
├── PUBLISH_GUIDE.md          # 发布指南
├── RESEARCH_REPORT.md        # 调研报告
└── TEST_REPORT.md            # 测试报告
```

---

## 🚀 使用方法

### 1. 安装依赖
```bash
cd v4.0.0
npm install
```

### 2. 编译
```bash
npm run build
```

### 3. 运行测试
```bash
npm test
```

### 4. 使用整理功能
```bash
# 开发环境
npm run curate

# 生产环境
npm run curate:run
```

---

## 📊 与 v4.1.0 的对比

| 功能 | v4.0.0 | v4.1.0 | 差异 |
|------|--------|--------|------|
| **重要性评分** | ❌ | ✅ | v4.1 新增 |
| **情感维度** | ❌ | ✅ | v4.1 新增 |
| **动态 Top-K** | ❌ | ✅ | v4.1 新增 |
| **混合检索** | ❌ | ✅ | v4.1 新增 |
| **LLM Wiki** | ✅ | ✅ | 相同 |
| **OS 级架构** | ✅ | ✅ | 相同 |
| **Curator** | ✅ | ✅ | 相同 |
| **检索准确率** | 75% | 85% | v4.1 +13% |
| **Token 节省** | 65% | 70% | v4.1 +8% |
| **文件大小** | 155KB | 207KB | v4.1 +33% |

---

## ⚠️ 注意事项

### 1. 这是历史版本
- v4.0.0 已被 v4.1.0 替代
- 建议使用最新的 v4.1.0
- 保留此版本用于：
  - 历史对比
  - 稳定性验证
  - 回退测试

### 2. 不向后兼容
- v4.1.0 的新功能在 v4.0.0 中不可用
- 记忆文件格式相同，可以共享
- 配置文件兼容

### 3. 维护状态
- ⚠️ **不再主动维护**
- ✅ 严重 bug 仍会修复
- ❌ 不再添加新功能

---

## 🔄 升级建议

### 升级到 v4.1.0

**收益**:
- ✅ 检索准确率 +13%
- ✅ Token 节省 +8%
- ✅ 重要性评分系统
- ✅ 情感维度
- ✅ 动态 Top-K
- ✅ 混合检索

**成本**:
- ✅ 零成本，完全向后兼容
- ✅ 配置文件可选更新

**方法**:
```bash
# 回到主目录
cd ..

# 使用 v4.1.0（当前版本）
# 所有新功能立即可用
```

---

## 📚 核心功能说明

### 1. LLM Wiki 主动整理 ⭐

**理念**: 基于 Karpathy LLM Wiki 理念，主动整理原始记忆 → 结构化知识

**使用**:
```typescript
import { MemoryCurator } from './src/curator';

const curator = new MemoryCurator({
  workspaceRoot: process.cwd(),
  memoryDir: 'memory',
  rawDir: 'memory/raw',
  wikiDir: 'memory/wiki',
});

await curator.curate();
```

**输出**:
- 📁 projects.md - 项目索引
- 👥 people.md - 人物索引
- ✅ decisions.md - 决策日志
- 📋 tasks.md - 任务看板
- 💡 insights.md - 洞察集合
- ⭐ preferences.md - 偏好设置

---

### 2. OS 级 4 层架构 ⭐

```
┌─────────────────────────────────────┐
│ L1: 短期工作记忆 (Token 优化器)      │
├─────────────────────────────────────┤
│ L2: 情景记忆 (每日记忆 + 技能进化)    │
├─────────────────────────────────────┤
│ L3: 语义长期记忆 (MEMORY.md + wiki)  │
├─────────────────────────────────────┤
│ L4: 程序性肌肉记忆 (技能蒸馏)        │
└─────────────────────────────────────┘
```

---

### 3. 记忆捕捉

```typescript
import { MemoryMaster } from './src/index';

const mm = new MemoryMaster();

await mm.capture('记住，我每天早上 7 点起床', {
  type: '人设',
});
```

---

### 4. 记忆检索

```typescript
const result = await mm.retrieve('我什么时候起床？');
console.log(result.memories[0].content);
// 输出："你每天早上 7 点起床"
```

---

## 🎯 适用场景

### 适合使用 v4.0.0
- ✅ 需要稳定性，不需要新功能
- ✅ 资源受限环境（小 33%）
- ✅ 历史对比研究
- ✅ 回退测试

### 适合使用 v4.1.0
- ✅ 生产环境（推荐）
- ✅ 需要最高准确率
- ✅ 需要情感分析
- ✅ 需要动态 Top-K

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- **主项目**: `../` (v4.1.0 当前版本)
- **文档**: 查看根目录的 README.md
- **升级指南**: 查看 ../VERSION_ARCHIVE.md

---

*Memory-Master v4.0.0 存档*  
*存档日期：2026-04-07*  
*状态：历史版本，已归档*  
*建议：使用最新的 v4.1.0*
