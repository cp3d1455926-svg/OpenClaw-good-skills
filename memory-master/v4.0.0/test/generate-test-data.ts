#!/usr/bin/env ts-node
/**
 * 生成测试数据
 * 
 * 运行方式：
 *   npx ts-node test/generate-test-data.ts
 */

import * as fs from 'fs';
import * as path from 'path';

function generateTestData() {
  console.log('📝 生成 Memory-Master v4.1 测试数据...\n');

  const memoryDir = path.join(process.cwd(), 'memory');
  const dailyDir = path.join(memoryDir, 'daily');
  const wikiDir = path.join(memoryDir, 'wiki');

  // 创建目录
  if (!fs.existsSync(dailyDir)) {
    fs.mkdirSync(dailyDir, { recursive: true });
  }
  if (!fs.existsSync(wikiDir)) {
    fs.mkdirSync(wikiDir, { recursive: true });
  }

  // ============================================================================
  // 生成今日记忆
  // ============================================================================
  const today = new Date().toISOString().split('T')[0];
  const todayContent = `# ${today} 记忆

## 情景记忆

### 上午工作

**ID**: mem_001

今天开始实现 Memory-Master v4.1 的新功能，非常兴奋！

- 重要性评分：5
- 情感：positive, intensity=4

---

### 项目进度会议

**ID**: mem_002

和项目团队讨论了 v4.1 的改进计划，大家一致认为需要添加重要性评分系统。

- 重要性评分：4
- 情感：positive, intensity=3

---

### 遇到技术难题

**ID**: mem_003

在实现动态 Top-K 时遇到了算法问题，有点沮丧。

- 重要性评分：3
- 情感：negative, intensity=2

---

### 成功解决

**ID**: mem_004

经过一番研究，终于找到了解决方案，太开心了！

- 重要性评分：5
- 情感：joy, intensity=5

---

### 代码审查

**ID**: mem_005

进行了代码审查，发现了一些需要优化的地方。

- 重要性评分：3
- 情感：neutral, intensity=1

---
`;

  fs.writeFileSync(path.join(dailyDir, `${today}.md`), todayContent, 'utf-8');
  console.log(`✅ 生成今日记忆：${today}.md`);

  // ============================================================================
  // 生成昨日记忆
  // ============================================================================
  const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString().split('T')[0];
  const yesterdayContent = `# ${yesterday} 记忆

## 情景记忆

### GitHub 调研

**ID**: mem_006

深入调研了 GitHub 上的 AI 记忆系统项目，发现了 10+ 标杆项目。

- 重要性评分：4
- 情感：positive, intensity=3

---

### 论文阅读

**ID**: mem_007

阅读了 Generative Agents、Mem0、MemoryBank 等 32 篇核心论文。

- 重要性评分：5
- 情感：positive, intensity=4

---

### 架构设计

**ID**: mem_008

基于调研结果，设计了 v4.1 的架构。

- 重要性评分：5
- 情感：positive, intensity=3

---
`;

  fs.writeFileSync(path.join(dailyDir, `${yesterday}.md`), yesterdayContent, 'utf-8');
  console.log(`✅ 生成昨日记忆：${yesterday}.md`);

  // ============================================================================
  // 生成 Wiki 记忆
  // ============================================================================
  
  // 项目索引
  const projectsContent = `# 项目索引

*最后更新：${today}*

## 🟢 进行中

### Memory-Master v4.1

基于 32 篇行业最佳实践笔记重构，实现重要性评分、情感维度、动态 Top-K 等功能。

### GitHub 调研

深入调研 10+ 标杆项目，分析 32 篇核心论文。

## ✅ 已完成

### Memory-Master v4.0

基于 Karpathy + Anthropic + Claude Code 重构，实现 LLM Wiki 主动整理功能。

### 32 篇笔记整合

完成 32 篇行业最佳实践笔记的汇总和分析。
`;

  fs.writeFileSync(path.join(wikiDir, 'projects.md'), projectsContent, 'utf-8');
  console.log(`✅ 生成项目索引：projects.md`);

  // 决策日志
  const decisionsContent = `# 决策日志

*最后更新：${today}*

## ${today}: 实现 v4.1 新功能

**背景**: 通过 GitHub/Gitee 调研发现行业最佳实践

**决策**: 实现重要性评分系统、情感维度、动态 Top-K、混合检索

**理由**: 
- Generative Agents 证明三维度评分有效
- MemoryBank 证明情感维度重要
- Mem0 证明动态 Top-K 节省 Token

**其他选项**: 
- 只实现评分系统（不够全面）
- 等待 v5.0 再实现（太慢）
`;

  fs.writeFileSync(path.join(wikiDir, 'decisions.md'), decisionsContent, 'utf-8');
  console.log(`✅ 生成决策日志：decisions.md`);

  // 任务看板
  const tasksContent = `# 任务看板

*最后更新：${today}*

## 🔄 进行中

- 🔴 **实现 v4.1 新功能** (截止：${today})
  - 重要性评分系统 ✅
  - 情感维度 ✅
  - 动态 Top-K ✅
  - 混合检索 ✅

## 📋 待处理

- 🟡 **编写测试用例**
  - 单元测试
  - 集成测试

- 🟢 **编写文档**
  - v4.1 使用示例
  - API 更新

## ✅ 已完成

- ✅ **GitHub/Gitee 调研**
  - 10+ 标杆项目
  - 32 篇核心论文

- ✅ **架构设计**
  - 三维度评分
  - 情感维度
  - 动态 Top-K
`;

  fs.writeFileSync(path.join(wikiDir, 'tasks.md'), tasksContent, 'utf-8');
  console.log(`✅ 生成任务看板：tasks.md`);

  // 洞察集合
  const insightsContent = `# 洞察集合

*最后更新：${today}*

## AI 架构

- ${today}: OS 级架构是最佳实践（MemGPT 证明）
- ${today}: 三维度评分更符合人类记忆（Generative Agents 证明）
- ${today}: 情感维度增强用户体验（MemoryBank 证明）

## 性能优化

- ${today}: 动态 Top-K 节省 8% Token（Mem0 数据）
- ${today}: 混合检索提升 13% 准确率
- ${today}: 响应时间控制在 75ms 以内

## 开发经验

- ${today}: 调研先行，避免重复造轮子
- ${today}: 文档和代码同等重要
- ${today}: 测试驱动开发提高效率
`;

  fs.writeFileSync(path.join(wikiDir, 'insights.md'), insightsContent, 'utf-8');
  console.log(`✅ 生成洞察集合：insights.md`);

  console.log('\n✅ 测试数据生成完成！\n');
  console.log('📁 生成的文件:');
  console.log(`   memory/daily/${today}.md`);
  console.log(`   memory/daily/${yesterday}.md`);
  console.log(`   memory/wiki/projects.md`);
  console.log(`   memory/wiki/decisions.md`);
  console.log(`   memory/wiki/tasks.md`);
  console.log(`   memory/wiki/insights.md`);
  console.log('\n现在可以运行测试了：');
  console.log('   npx ts-node test/v41-test.ts\n');
}

generateTestData();
