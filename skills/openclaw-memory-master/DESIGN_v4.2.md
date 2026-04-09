# Memory-Master v4.2.0 综合设计文档

**版本**: v4.2.0  
**作者**: 小鬼 👻 + Jake  
**日期**: 2026-04-08  
**状态**: 🚧 开发中

---

## 📋 版本概览

### v4.2.0 核心功能

| 功能 | 参考来源 | 目标 | 优先级 |
|------|----------|------|--------|
| L0/L1/L2 分层加载 | 字节 OpenViking + MemGPT | 3 层记忆架构 | P0 |
| AAAK 压缩算法 | MemPalace | 90% 压缩率 | P0 |
| 知识图谱 | HippoRAG + ZEP | 实体关系检索 | P1 |
| 多路召回 | 自研创新 | 语义 + 关键词 + 图 | P1 |

### 性能目标

| 指标 | v4.1.0 | v4.2.0 目标 | 提升 |
|------|--------|-------------|------|
| 压缩率 | 47-60% | 90% | +50% |
| 检索准确率 | 85% | 92% | +7% |
| 响应时间 | <100ms | <80ms | -20% |
| Token 节省 | 70% | 85% | +15% |
| 记忆加载 | ~180ms | <100ms | -44% |

---

## 🏗️ 架构设计

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        Memory-Master v4.2                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Capture    │  │   Retrieve   │  │   Compact    │          │
│  │   Module     │  │   Module     │  │   Module     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                   │
│         └─────────────────┼─────────────────┘                   │
│                           │                                     │
│                  ┌────────▼────────┐                            │
│                  │  Memory Master  │                            │
│                  │    (Core)       │                            │
│                  └────────┬────────┘                            │
│                           │                                     │
│         ┌─────────────────┼─────────────────┐                  │
│         │                 │                 │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │ L0: Hot      │  │ L1: Warm     │  │ L2: Cold     │          │
│  │ Memory       │  │ Memory       │  │ Memory       │          │
│  │ (24h)        │  │ (7d)         │  │ (History)    │          │
│  │ In-Memory    │  │ On-Demand    │  │ Disk         │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                           │                                     │
│         ┌─────────────────┼─────────────────┐                  │
│         │                 │                 │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐          │
│  │ AAAK         │  │ Knowledge    │  │ Multi-Path   │          │
│  │ Compressor   │  │ Graph        │  │ Recall       │          │
│  │ (90%)        │  │ Engine       │  │ Fusion       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 模块设计

### 1. L0/L1/L2 分层加载系统

#### 设计灵感
- **字节 OpenViking**: L0/L1/L2 分层加载策略
- **MemGPT**: 操作系统级记忆架构
- **人类记忆**: 工作记忆 + 短期记忆 + 长期记忆

#### 分层策略

| 层级 | 时间范围 | 存储位置 | 加载策略 | 容量 |
|------|----------|----------|----------|------|
| L0 | 最近 24h | 内存 (Map) | 常驻 | ~100 条 |
| L1 | 最近 7d | 内存 + 磁盘 | 按需加载 | ~1000 条 |
| L2 | 历史 | 磁盘 | 懒加载 | 无限制 |

#### 文件结构

```
memory/
├── l0-hot/
│   ├── index.json          # L0 索引（内存映射）
│   └── sessions/
│       └── 2026-04-08/
│           └── session-xxx.json
├── l1-warm/
│   ├── index.json          # L1 索引
│   └── days/
│       ├── 2026-04-07/
│       │   └── day-summary.json
│       └── 2026-04-06/
│           └── day-summary.json
├── l2-cold/
│   ├── index.json          # L2 索引
│   └── months/
│       ├── 2026-04/
│       │   └── month-archive.json
│       └── 2026-03/
│           └── month-archive.json
└── metadata.json           # 全局元数据
```

#### 核心 API

```typescript
interface LayeredMemoryManager {
  // 写入（自动分层）
  write(content: string, options: WriteOptions): Promise<MemoryId>;
  
  // 读取（自动从合适层级加载）
  read(id: MemoryId): Promise<Memory>;
  
  // 检索（跨层检索）
  search(query: string, options: SearchOptions): Promise<SearchResult>;
  
  // 层级迁移（后台任务）
  migrate(): Promise<MigrationResult>;  // L0→L1, L1→L2
  
  // 缓存管理
  getL0Size(): number;
  getL1Size(): number;
  getL2Size(): number;
  clearL0(): void;
  preloadL1(timeRange: TimeRange): Promise<void>;
}
```

#### 实现文件
- `src/layered-manager.ts` - 分层管理器核心
- `src/l0-hot-store.ts` - L0 热存储
- `src/l1-warm-store.ts` - L1 温存储
- `src/l2-cold-store.ts` - L2 冷存储
- `src/migration-service.ts` - 层级迁移服务

---

### 2. AAAK 压缩算法

#### 设计灵感
- **MemPalace**: AAAK 压缩实现 30 倍压缩零丢失
- **AAAK 原理**: Abstract-Align-Anchor-Knowledge

#### AAAK 四阶段

```
原始记忆 → Abstract → Align → Anchor → Knowledge → 压缩结果
            ↓           ↓        ↓         ↓
         提取摘要    对齐上下文  锚定关键  结构化知识
```

##### Phase 1: Abstract (摘要提取)
- 提取核心信息
- 移除冗余描述
- 保留关键事实

##### Phase 2: Align (上下文对齐)
- 关联相关记忆
- 建立时间线
- 统一术语

##### Phase 3: Anchor (关键锚定)
- 识别关键实体
- 标记重要关系
- 锚定核心概念

##### Phase 4: Knowledge (知识结构化)
- 转换为结构化格式
- 建立索引
- 生成压缩表示

#### 压缩率目标

| 记忆类型 | 原始大小 | 压缩后 | 压缩率 |
|----------|----------|--------|--------|
| 对话记录 | 10KB | 1KB | 90% |
| 会议纪要 | 20KB | 2KB | 90% |
| 学习笔记 | 15KB | 1.5KB | 90% |
| 代码片段 | 50KB | 5KB | 90% |

#### 核心 API

```typescript
interface AAAKCompressor {
  // 压缩
  compress(content: string, options?: CompressOptions): Promise<CompressedMemory>;
  
  // 解压（无损还原）
  decompress(compressed: CompressedMemory): Promise<string>;
  
  // 压缩质量评估
  evaluateQuality(original: string, compressed: CompressedMemory): QualityReport;
  
  // 批量压缩
  batchCompress(contents: string[]): Promise<CompressedMemory[]>;
}

interface CompressedMemory {
  id: string;
  abstract: string;      // 摘要
  align: Alignment[];    // 对齐信息
  anchors: Anchor[];     // 锚点
  knowledge: Knowledge;  // 结构化知识
  metadata: Metadata;    // 元数据
  checksum: string;      // 校验和（验证无损）
}
```

#### 实现文件
- `src/aaak-compressor.ts` - AAAK 压缩核心
- `src/abstract-extractor.ts` - 摘要提取器
- `src/context-aligner.ts` - 上下文对齐器
- `src/anchor-identifier.ts` - 锚点识别器
- `src/knowledge-structurer.ts` - 知识结构化器
- `src/quality-validator.ts` - 质量验证器

---

### 3. 知识图谱引擎

#### 设计灵感
- **HippoRAG**: 图结构检索提升准确率 34%
- **ZEP**: 知识图谱自动构建
- **Ontology**: 类型化知识图谱

#### 图谱结构

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│  Entity  │──rel──→│  Entity  │──rel──→│  Entity  │
│ (Person) │  works  │(Project) │  uses   │ (Skill)  │
└──────────┘         └──────────┘         └──────────┘
     │                    │                    │
  has_skill           has_task          has_version
     │                    │                    │
     ▼                    ▼                    ▼
┌──────────┐         ┌──────────┐         ┌──────────┐
│  Skill   │         │   Task   │         │ Version  │
└──────────┘         └──────────┘         └──────────┘
```

#### 实体类型

| 类型 | 属性 | 关系 |
|------|------|------|
| Person | name, role, skills | works_on, knows, created |
| Project | name, status, deadline | has_task, uses_skill, owned_by |
| Task | title, status, priority | assigned_to, part_of, depends_on |
| Skill | name, version, category | used_by, improved_by |
| Memory | id, type, timestamp | about, references |
| Event | name, time, location | attended_by, related_to |

#### 核心 API

```typescript
interface KnowledgeGraph {
  // 实体操作
  addEntity(entity: Entity): Promise<EntityId>;
  getEntity(id: EntityId): Promise<Entity>;
  updateEntity(id: EntityId, updates: Partial<Entity>): Promise<void>;
  deleteEntity(id: EntityId): Promise<void>;
  
  // 关系操作
  addRelationship(from: EntityId, to: EntityId, rel: Relationship): Promise<void>;
  getRelationships(entityId: EntityId, type?: RelationType): Promise<Relationship[]>;
  
  // 图遍历
  traverse(startId: EntityId, options: TraverseOptions): Promise<Path[]>;
  findShortestPath(from: EntityId, to: EntityId): Promise<Path>;
  
  // 图检索
  searchEntities(query: string): Promise<Entity[]>;
  searchRelationships(query: string): Promise<Relationship[]>;
  
  // 自动构建
  extractFromText(text: string): Promise<ExtractionResult>;
  buildFromMemories(memoryIds: MemoryId[]): Promise<void>;
}
```

#### 实现文件
- `src/knowledge-graph.ts` - 知识图谱核心
- `src/entity-manager.ts` - 实体管理
- `src/relationship-manager.ts` - 关系管理
- `src/graph-traverser.ts` - 图遍历器
- `src/entity-extractor.ts` - 实体提取器（基于 LLM）
- `src/graph-store.ts` - 图存储（JSON/图数据库）

---

### 4. 多路召回融合

#### 设计灵感
- **混合检索**: 结合多种检索方式的优势
- **多路召回**: 搜索引擎常用策略

#### 召回路径

```
                    Query
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │ Semantic│  │Keyword │  │  Graph │
    │ Search  │  │ Search │  │ Search │
    │ (向量)  │  │ (BM25) │  │(遍历)  │
    └────┬───┘  └────┬───┘  └────┬───┘
         │            │            │
         │    Scores  │    Scores  │    Scores
         │    [0.85]  │    [0.72]  │    [0.91]
         │            │            │
         └────────────┼────────────┘
                      │
                      ▼
              ┌───────────────┐
              │  Fusion Rank  │
              │  (RRF/Borda)  │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Final Results │
              │   Top-K       │
              └───────────────┘
```

#### 融合算法

##### 1. RRF (Reciprocal Rank Fusion)
```
RRF(d) = Σ 1/(k + rank_i(d))
其中 k 是常数（通常 60），rank_i 是文档在第 i 路的结果排名
```

##### 2. Borda Count
```
Borda(d) = Σ (N - rank_i(d))
其中 N 是候选集大小
```

##### 3. 加权融合
```
Score(d) = w1*semantic + w2*keyword + w3*graph
其中 w1+w2+w3 = 1
```

#### 核心 API

```typescript
interface MultiPathRecall {
  // 多路检索
  search(query: string, options: MultiSearchOptions): Promise<MultiSearchResult>;
  
  // 融合排序
  fuse(results: SearchResult[], method: FusionMethod): Promise<FusedResult>;
  
  // 权重优化（基于反馈）
  optimizeWeights(feedback: Feedback[]): Promise<WeightConfig>;
}

interface MultiSearchOptions {
  semanticWeight?: number;    // 语义检索权重
  keywordWeight?: number;     // 关键词权重
  graphWeight?: number;       // 图检索权重
  fusionMethod?: FusionMethod; // 融合方法
  topK?: number;              // 返回数量
}

type FusionMethod = 'rrf' | 'borda' | 'weighted' | 'learned';
```

#### 实现文件
- `src/multi-path-recall.ts` - 多路召回核心
- `src/semantic-search.ts` - 语义检索（向量）
- `src/keyword-search.ts` - 关键词检索（BM25）
- `src/graph-search.ts` - 图检索
- `src/fusion-ranker.ts` - 融合排序器
- `src/weight-optimizer.ts` - 权重优化器

---

## 🔄 数据流

### 写入流程

```
用户输入
   │
   ▼
┌─────────────┐
│ 敏感数据过滤 │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ L0 热存储   │ ←── 立即可用
└──────┬──────┘
       │
       ▼ (后台异步)
┌─────────────┐
│ AAAK 压缩   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 知识图谱提取 │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ L1/L2 存储  │
└─────────────┘
```

### 检索流程

```
用户查询
   │
   ▼
┌─────────────┐
│ 查询分析    │
│ (类型/意图) │
└──────┬──────┘
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│ L0 检索 │   │ L1 检索 │   │ L2 检索 │
└────┬────┘   └────┬────┘   └────┬────┘
     │             │             │
     └─────────────┼─────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │ 多路召回融合    │
         │ (语义 + 关键词 + 图)│
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ 重要性评分排序  │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ 返回 Top-K 结果  │
         └─────────────────┘
```

---

## 📊 性能优化

### 1. 缓存策略

```typescript
interface CacheStrategy {
  // L0: 全量缓存（常驻内存）
  l0: {
    maxSize: 100;           // 最大条目数
    ttl: 24 * 60 * 60 * 1000; // 24 小时
    eviction: 'lru';        // 淘汰策略
  };
  
  // L1: 部分缓存（按需加载）
  l1: {
    maxSize: 1000;
    ttl: 7 * 24 * 60 * 60 * 1000; // 7 天
    preload: true;          // 预加载
  };
  
  // L2: 懒加载（磁盘）
  l2: {
    cache: false;           // 不缓存
    prefetch: true;         // 预取
  };
}
```

### 2. 索引优化

```typescript
interface IndexConfig {
  // 倒排索引（关键词检索）
  invertedIndex: {
    enabled: true;
    fields: ['content', 'tags', 'entities'];
    analyzer: 'zh';         // 中文分词
  };
  
  // 向量索引（语义检索）
  vectorIndex: {
    enabled: true;
    dimension: 768;         // 向量维度
    metric: 'cosine';       // 相似度度量
    hnsw: {                 // HNSW 参数
      m: 16,
      efConstruction: 200,
    };
  };
  
  // 图索引（关系检索）
  graphIndex: {
    enabled: true;
    adjacencyList: true;    // 邻接表
    reverseIndex: true;     // 反向索引
  };
}
```

### 3. 批量操作

```typescript
// 批量写入（减少 I/O）
async batchWrite(items: WriteItem[]): Promise<WriteResult> {
  // 1. 分组（按层级）
  const grouped = this.groupByLayer(items);
  
  // 2. 批量压缩
  const compressed = await this.batchCompress(grouped.l1, grouped.l2);
  
  // 3. 批量存储
  await Promise.all([
    this.l0Store.write(grouped.l0),
    this.l1Store.write(compressed.l1),
    this.l2Store.write(compressed.l2),
  ]);
  
  // 4. 批量更新索引
  await this.indexManager.batchUpdate(items);
  
  // 5. 批量更新图谱
  await this.graphManager.batchExtract(items);
}
```

---

## 🧪 测试计划

### 单元测试

| 模块 | 测试覆盖 | 关键测试用例 |
|------|----------|--------------|
| LayeredManager | 95% | 层级迁移、缓存命中、边界条件 |
| AAAKCompressor | 95% | 压缩/解压、质量验证、边界情况 |
| KnowledgeGraph | 90% | 实体 CRUD、关系遍历、图检索 |
| MultiPathRecall | 90% | 各路检索、融合排序、权重优化 |

### 集成测试

1. **端到端写入测试**: 写入 → 压缩 → 存储 → 索引 → 图谱
2. **端到端检索测试**: 查询 → 多路召回 → 融合 → 排序 → 返回
3. **性能测试**: 1000 条记忆加载时间、检索延迟
4. **压力测试**: 并发写入、并发检索

### 基准测试

```typescript
interface BenchmarkSuite {
  // 压缩基准
  'AAAK compression ratio': () => measureCompressionRatio();
  'AAAK compression speed': () => measureCompressionSpeed();
  'AAAK decompression speed': () => measureDecompressionSpeed();
  
  // 检索基准
  'L0 retrieval latency': () => measureL0Latency();
  'L1 retrieval latency': () => measureL1Latency();
  'L2 retrieval latency': () => measureL2Latency();
  'Multi-path recall accuracy': () => measureRecallAccuracy();
  
  // 图谱基准
  'Graph traversal speed': () => measureGraphSpeed();
  'Entity extraction accuracy': () => measureExtractionAccuracy();
}
```

---

## 📅 开发计划

### Phase 1: L0/L1/L2 分层 (3 天)
- Day 1: 设计数据结构 + 实现 L0 热存储
- Day 2: 实现 L1 温存储 + L2 冷存储
- Day 3: 实现层级迁移 + 集成测试

### Phase 2: AAAK 压缩 (4 天)
- Day 1: 实现 Abstract 摘要提取
- Day 2: 实现 Align 上下文对齐
- Day 3: 实现 Anchor 锚定 + Knowledge 结构化
- Day 4: 质量验证 + 性能优化

### Phase 3: 知识图谱 (4 天)
- Day 1: 实体管理 + 关系管理
- Day 2: 图存储 + 图遍历
- Day 3: 实体提取（LLM）
- Day 4: 图检索 + 集成测试

### Phase 4: 多路召回 (3 天)
- Day 1: 语义检索 + 关键词检索
- Day 2: 图检索 + 融合排序
- Day 3: 权重优化 + 集成测试

### Phase 5: 集成与发布 (2 天)
- Day 1: 端到端测试 + 性能优化
- Day 2: 文档更新 + 发布 v4.2.0

**总计**: 16 天（约 2 周）

---

## 📈 验收标准

### 功能验收
- [ ] L0/L1/L2 分层正常工作
- [ ] AAAK 压缩率达到 90%
- [ ] 知识图谱正确提取实体和关系
- [ ] 多路召回融合提升检索准确率

### 性能验收
- [ ] 压缩率 ≥ 90%
- [ ] 检索准确率 ≥ 92%
- [ ] 平均响应时间 < 80ms
- [ ] Token 节省 ≥ 85%

### 质量验收
- [ ] 单元测试覆盖 ≥ 90%
- [ ] 集成测试全部通过
- [ ] 无严重 Bug
- [ ] 文档完整

---

## 🔮 未来展望 (v4.3.0+)

- **多模态记忆**: 支持图片、语音、视频记忆
- **自进化**: 基于用户反馈自动优化权重和策略
- **分布式**: 支持多设备同步和分布式存储
- **可视化**: 记忆图谱可视化界面
- **插件系统**: 支持第三方扩展

---

*设计文档版本：v4.2.0-draft*  
*创建时间：2026-04-08*  
*作者：小鬼 👻 + Jake*
