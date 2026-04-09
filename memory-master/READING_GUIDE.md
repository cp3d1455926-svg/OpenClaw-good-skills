# 📚 AI Agent 记忆系统核心论文阅读指南

> **创建时间**: 2026-04-07 20:45  
> **地点**: 深圳  
> **目的**: 系统性阅读 50+ 篇 AI 记忆系统论文  
> **作者**: 小鬼 👻

---

## 🎯 阅读优先级

### 🔴 优先级 1: 必读综述 (3 篇) ⭐⭐⭐⭐⭐

这些论文提供了领域的全景图，必须精读！

#### 1. **Memory in the Age of AI Agents: A Survey**

**基本信息**:
- **arXiv**: 2512.13564
- **日期**: 2025-12-15 (v2: 2026-01-13)
- **作者**: Yuyang Hu, Shichun Liu, Yanwei Yue, Guibin Zhang + 46 位合作者
- **机构**: 多机构合作 (复旦大学等)
- **PDF**: https://arxiv.org/pdf/2512.13564.pdf

**核心贡献**:
1. 统一分类体系：Forms / Functions / Dynamics
2. 概念界定：Agent Memory vs LLM Memory vs RAG vs Context Engineering
3. 全面覆盖：2023-2026 年所有重要工作
4. 实践指南：Benchmarks + Open-Source Frameworks

**Forms (记忆形式)**:
- **Token-level Memory**: 显式离散存储 (我们的 MEMORY.md)
- **Parametric Memory**: 隐式权重存储 (LoRA 微调)
- **Latent Memory**: 隐藏状态存储 (KV Cache)

**Functions (记忆功能)**:
- **Factual Memory**: 事实知识 (我们的语义记忆)
- **Experiential Memory**: 经验技能 (我们的技能自进化)
- **Working Memory**: 工作记忆 (我们的短期记忆)

**Dynamics (记忆动态)**:
- **Formation**: 记忆形成 (我们的记忆捕捉)
- **Evolution**: 记忆演化/巩固/遗忘 (我们的记忆压缩)
- **Retrieval**: 检索策略 (我们的 5 种查询)

**与 Memory-Master 的对应**:
- ✅ Token-level → MEMORY.md + wiki/*.md
- ✅ Parametric → 技能蒸馏 (规划中)
- ✅ Latent → KV Cache 优化 (规划中)
- ✅ Factual → 语义记忆
- ✅ Experiential → 技能自进化
- ✅ Working → 情景记忆
- ✅ Formation → 记忆捕捉
- ✅ Evolution → 记忆压缩
- ✅ Retrieval → 5 种查询

**阅读重点**:
- [ ] 第 3 章：统一分类体系
- [ ] 第 4 章：Forms 详解
- [ ] 第 5 章：Functions 详解
- [ ] 第 6 章：Dynamics 详解
- [ ] 第 7 章：Benchmarks 对比
- [ ] 第 8 章：Open-Source Frameworks

**对我们的启发**:
1. 我们的 OS 级 4 层架构符合 Forms 分类
2. 我们的三维度评分符合 Dynamics 检索策略
3. 我们的 LLM Wiki 是 Token-level Memory 的创新

---

#### 2. **From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms**

**基本信息**:
- **Preprints**: 202601.0618
- **日期**: 2026-01
- **URL**: https://www.preprints.org/manuscript/202601.0618
- **主题**: 从存储到经验的演进

**核心洞察**:
> **记忆不是存储，而是经验。**

**关键发现**:
1. 时间覆盖偏差：2024-2025 年研究爆发
2. 经验阶段：2025 年下半年成为独立研究方向
3. 工作记忆组织：动态可塑的记忆间隔
4. 环境建模：从演示中推断世界规则

**工作记忆优化**:
- 隔离间隔记忆
- 关键决策节点回顾整合
- 自适应剪枝

**与 Memory-Master 的对应**:
- ✅ 动态可塑间隔 → 我们的每日记忆
- ✅ 关键节点整合 → 我们的决策日志
- ✅ 自适应剪枝 → 我们的记忆压缩

**阅读重点**:
- [ ] 第 2 章：从存储到经验的演进
- [ ] 第 3 章：工作记忆组织
- [ ] 第 4 章：环境建模
- [ ] 第 5 章：未来方向

**对我们的启发**:
1. v4.2 要实现自适应剪枝
2. 增强关键决策节点整合
3. 优化工作记忆间隔管理

---

#### 3. **AI Memory: Comprehensive Review** (Jean Memory)

**基本信息**:
- **来源**: https://www.jeanmemory.com/ai-memory-landscape-review.pdf
- **日期**: 2025
- **主题**: AI 记忆全景图

**核心洞察**:
> **仅仅能够调用工具是不够的。你必须构建足够智能的系统，知道何时使用什么工具，如何使用每个工具，然后摆脱干扰 AI 完成任务的污染上下文。**

**关键主题**:
1. 上下文工程：Shopify CEO Tobias Lütke 提出
2. 混合系统：2025 年行业趋势
3. GraphRAG 的局限：经常继承两者的弱点

**失败模式**:
- RAG 检索不相关文档污染上下文
- 函数调用增加延迟
- JSON 结构过度简化或变得笨重
- 上下文工程需要持续调优

**2024 年末基本架构**:
```
外部存储 + 检索 + 上下文注入
```

**与 Memory-Master 的对应**:
- ✅ 外部存储 → memory/ 目录
- ✅ 检索 → 5 种查询方式
- ✅ 上下文注入 → 检索结果注入
- ✅ 避免污染 → Top-5 过滤

**阅读重点**:
- [ ] 第 3 章：上下文工程
- [ ] 第 5 章：混合系统
- [ ] 第 7 章：GraphRAG 分析
- [ ] 第 9 章：最佳实践

**对我们的启发**:
1. 加强上下文工程管理
2. 实现智能工具调用
3. 避免记忆污染

---

### 🟠 优先级 2: 核心架构论文 (5 篇) ⭐⭐⭐⭐

#### 4. **A-MEM: Agentic Memory for LLM Agents**

**基本信息**:
- **arXiv**: 2502.12110
- **日期**: 2025-02
- **主题**: Agent 专用记忆架构

**核心创新**:
1. Agent 专用 (非通用 RAG)
2. 多 Agent 协作支持
3. 记忆共享机制

**与 Memory-Master 的对应**:
- ✅ Agent 专用 → 我们的 OpenClaw Skill 设计
- ⚠️ 多 Agent → v5.0 规划
- ⚠️ 记忆共享 → v5.0 规划

**阅读重点**:
- [ ] 第 3 章：A-MEM 架构设计
- [ ] 第 4 章：多 Agent 协作
- [ ] 第 5 章：实验评估

---

#### 5. **H-MEM: Hierarchical Memory for High-Efficiency Long-Term Reasoning**

**基本信息**:
- **arXiv**: 2507.22925
- **日期**: 2025-07
- **主题**: 分层记忆高效推理

**核心创新**:
1. L0/L1/L2 三层加载
2. 高效长程推理
3. Token 优化

**与 Memory-Master 的对应**:
- ✅ L0/L1/L2 → v4.2 要实现
- ✅ 高效推理 → 我们的三维度评分
- ✅ Token 优化 → 我们的 70% 节省

**阅读重点**:
- [ ] 第 3 章：分层架构设计
- [ ] 第 4 章：推理优化
- [ ] 第 5 章：Token 节省策略

**对我们的启发**:
1. v4.2 实现 L0/L1/L2
2. 目标：Token 节省 85%+
3. 增强长程推理能力

---

#### 6. **O-Mem: Omni Memory System**

**基本信息**:
- **arXiv**: 2511.13593
- **日期**: 2025-11
- **主题**: 全模态自进化记忆

**核心创新**:
1. 全模态支持 (文本/图像/音频)
2. 长周期支持
3. 自进化能力

**与 Memory-Master 的对应**:
- ✅ 自进化 → 我们的技能自进化
- ⚠️ 全模态 → v5.0 规划
- ✅ 长周期 → 我们的 90 天保留

**阅读重点**:
- [ ] 第 3 章：全模态架构
- [ ] 第 4 章：自进化机制
- [ ] 第 5 章：长周期实验

---

#### 7. **MIRIX: Multi-Agent Memory System**

**基本信息**:
- **arXiv**: 2507.07957
- **日期**: 2025-07
- **主题**: 多 Agent 记忆系统

**核心创新**:
1. 多 Agent 记忆协调
2. 共享/私有记忆分离
3. 冲突解决机制

**与 Memory-Master 的对应**:
- ⚠️ 多 Agent → v5.0 规划
- ⚠️ 记忆共享 → v5.0 规划
- ⚠️ 冲突解决 → v5.0 规划

**阅读重点**:
- [ ] 第 3 章：多 Agent 架构
- [ ] 第 4 章：记忆协调
- [ ] 第 5 章：冲突解决

---

#### 8. **MEM1: Learning to Synergize Memory and Reasoning**

**基本信息**:
- **arXiv**: 2506.xxxxx
- **日期**: 2025-06
- **主题**: 记忆与推理协同

**核心创新**:
1. 记忆推理协同
2. 强化学习优化
3. 高效长程任务

**与 Memory-Master 的对应**:
- ✅ 记忆推理协同 → 我们的三维度评分
- ⚠️ 强化学习 → v5.0 规划
- ✅ 长程任务 → 我们的 OS 级架构

**阅读重点**:
- [ ] 第 3 章：协同机制
- [ ] 第 4 章：强化学习
- [ ] 第 5 章：长程任务实验

---

### 🟡 优先级 3: 评估与基准 (3 篇) ⭐⭐⭐⭐

#### 9. **MemBench: Comprehensive Evaluation**

**基本信息**:
- **arXiv**: 2506.xxxxx
- **日期**: 2025-06
- **主题**: 全面记忆评估基准

**核心贡献**:
1. 综合评估指标
2. 多维度测试
3. 开源基准

**评估维度**:
- 存储容量
- 检索准确率
- 推理支持
- 持续学习
- 抗干扰能力

**与 Memory-Master 的对应**:
- ✅ 检索准确率 → 我们的 85%
- ✅ 推理支持 → 我们的三维度评分
- ✅ 持续学习 → 我们的技能自进化

---

#### 10. **Evaluating Memory Structure**

**基本信息**:
- **arXiv**: 2602.xxxxx
- **日期**: 2026-02
- **主题**: 记忆结构评估

**核心贡献**:
1. 结构评估方法
2. 记忆质量指标
3. 对比分析

---

#### 11. **LTMbenchmark: Long-Term Memory**

**基本信息**:
- **arXiv**: 240x.xxxxx
- **日期**: 2024
- **主题**: 长期对话记忆基准

**核心贡献**:
1. 动态对话基准
2. 长期记忆评估
3. 上下文管理

---

## 📖 阅读计划

### 第 1 周 (2026-04-08 to 2026-04-14)

**目标**: 完成优先级 1 的 3 篇综述

| 日期 | 论文 | 进度 |
|------|------|------|
| 04-08 | Memory in the Age of AI Agents | [ ] |
| 04-09 | Memory in the Age of AI Agents | [ ] |
| 04-10 | From Storage to Experience | [ ] |
| 04-11 | From Storage to Experience | [ ] |
| 04-12 | AI Memory: Comprehensive Review | [ ] |
| 04-13 | AI Memory: Comprehensive Review | [ ] |
| 04-14 | 整理阅读笔记 | [ ] |

### 第 2 周 (2026-04-15 to 2026-04-21)

**目标**: 完成优先级 2 的 5 篇架构论文

| 日期 | 论文 | 进度 |
|------|------|------|
| 04-15 | A-MEM | [ ] |
| 04-16 | H-MEM | [ ] |
| 04-17 | O-Mem | [ ] |
| 04-18 | MIRIX | [ ] |
| 04-19 | MEM1 | [ ] |
| 04-20 | 整理架构对比 | [ ] |
| 04-21 | 更新 v4.2 计划 | [ ] |

### 第 3 周 (2026-04-22 to 2026-04-28)

**目标**: 完成优先级 3 的 3 篇评估论文

| 日期 | 论文 | 进度 |
|------|------|------|
| 04-22 | MemBench | [ ] |
| 04-23 | Evaluating Memory Structure | [ ] |
| 04-24 | LTMbenchmark | [ ] |
| 04-25 | 整理评估指标 | [ ] |
| 04-26 | 设计 Memory-Master 评测 | [ ] |
| 04-27 | 实现评测基准 | [ ] |
| 04-28 | 运行评测 | [ ] |

---

## 📝 阅读笔记模板

### 论文基本信息

```markdown
**标题**: 
**arXiv**: 
**日期**: 
**作者**: 
**机构**: 
**PDF**: 
```

### 核心贡献

```markdown
1. 
2. 
3. 
```

### 与 Memory-Master 的对应

```markdown
✅ 已实现:
⚠️ 规划中:
❌ 不匹配:
```

### 关键启发

```markdown
1. 
2. 
3. 
```

### v4.2/v5.0 改进点

```markdown
- [ ] 
- [ ] 
- [ ] 
```

---

## 📊 论文统计

### 按类别

| 类别 | 论文数 | 已读 | 待读 |
|------|--------|------|------|
| **综述** | 3 | 0 | 3 |
| **架构** | 5 | 0 | 5 |
| **评估** | 3 | 0 | 3 |
| **应用** | 10 | 0 | 10 |
| **优化** | 8 | 0 | 8 |
| **多模态** | 5 | 0 | 5 |
| **多 Agent** | 6 | 0 | 6 |
| **总计** | 40 | 0 | 40 |

### 按优先级

| 优先级 | 论文数 | 完成时间 |
|--------|--------|---------|
| 🔴 P1 | 3 | 2026-04-14 |
| 🟠 P2 | 5 | 2026-04-21 |
| 🟡 P3 | 3 | 2026-04-28 |
| 🟢 P4 | 29 | 2026-05-31 |

---

## 🔗 资源链接

### 论文列表

1. **Agent-Memory-Paper-List**
   - GitHub: https://github.com/Shichun-Liu/Agent-Memory-Paper-List
   - Stars: 1.7k
   - 论文数：32+ 篇

2. **Awesome-Memory-Mechanism-for-Agent**
   - GitHub: https://github.com/SiyuanWan99/Awesome-Memory-Mechanism-for-Agent

3. **ai-agent-papers**
   - GitHub: https://github.com/masamasa59/ai-agent-papers

### 核心论文 PDF

1. **Memory in the Age of AI Agents**
   - PDF: https://arxiv.org/pdf/2512.13564.pdf

2. **From Storage to Experience**
   - PDF: https://www.preprints.org/manuscript/202601.0618/v1/download

3. **AI Memory: Comprehensive Review**
   - PDF: https://www.jeanmemory.com/ai-memory-landscape-review.pdf

---

## 💡 阅读建议

### 1. 先读综述，再读具体论文

**原因**:
- 综述提供全景图
- 理解领域演进
- 找到研究方向

### 2. 带着问题阅读

**问题清单**:
- 这篇论文解决了什么问题？
- 核心创新是什么？
- 与 Memory-Master 有什么关系？
- 我们可以学习什么？
- v4.2/v5.0 如何实现？

### 3. 做详细的阅读笔记

**笔记要点**:
- 核心贡献 (3 点)
- 与 Memory-Master 的对应
- 关键启发
- 改进点清单

### 4. 定期整理和分享

**整理频率**:
- 每天：记录阅读进度
- 每周：整理周笔记
- 每月：写综述文章

**分享渠道**:
- 知乎：《50 篇论文解读》系列
- 公众号：《AI 记忆系统前沿》
- GitHub: 更新 REFERENCES.md

---

## 🎯 预期成果

### 2026-04-14 (完成 P1)

- ✅ 理解领域全景
- ✅ 掌握统一分类体系
- ✅ 更新 REFERENCES.md

### 2026-04-21 (完成 P2)

- ✅ 理解核心架构
- ✅ 实现 L0/L1/L2 分层
- ✅ 实现多路召回检索

### 2026-04-28 (完成 P3)

- ✅ 掌握评估方法
- ✅ 实现 Memory-Master 评测基准
- ✅ 发布评测报告

### 2026-05-31 (完成 P4)

- ✅ 全面掌握领域
- ✅ v5.0 规划完成
- ✅ 发表学术综述文章

---

*阅读指南创建时间：2026-04-07 20:45*  
*地点：深圳*  
*作者：小鬼 👻*  
*状态：准备好学习了！📚*
