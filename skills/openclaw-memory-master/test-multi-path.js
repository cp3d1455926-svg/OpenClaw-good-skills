/**
 * 多路召回测试脚本
 */

const { MultiPathRecallManager } = require('./dist/multi-path-recall');

async function runTest() {
  console.log('🧪 开始测试多路召回融合...\n');

  const manager = new MultiPathRecallManager({
    fusionMethod: 'rrf',
    weights: {
      semantic: 0.4,
      keyword: 0.3,
      graph: 0.3,
    },
  });

  try {
    // ========== 测试 1: 添加记忆 ==========
    console.log('📝 测试 1: 添加记忆');
    
    const memories = [
      {
        id: 'mem-001',
        content: 'Memory-Master 是一个 AI 记忆系统，由 Jake 和小鬼共同开发',
        memory: { type: 'project', importance: 1.0 },
      },
      {
        id: 'mem-002',
        content: 'AAAK 压缩算法实现 87% 压缩率，包括 Abstract、Align、Anchor、Knowledge 四个阶段',
        memory: { type: 'algorithm', importance: 0.9 },
      },
      {
        id: 'mem-003',
        content: '知识图谱引擎支持实体管理、关系管理、图遍历等功能',
        memory: { type: 'feature', importance: 0.8 },
      },
      {
        id: 'mem-004',
        content: 'L0/L1/L2 分层存储系统提供热、温、冷三层记忆管理',
        memory: { type: 'architecture', importance: 0.95 },
      },
      {
        id: 'mem-005',
        content: '多路召回融合结合语义检索、关键词检索、图检索三种方式',
        memory: { type: 'feature', importance: 0.85 },
      },
    ];

    await manager.addMemories(memories);
    console.log(`✅ 添加了 ${memories.length} 条记忆\n`);

    // ========== 测试 2: 关键词检索 ==========
    console.log('🔍 测试 2: 关键词检索');
    
    const query1 = 'Memory-Master';
    console.log(`查询："${query1}"`);
    
    const results1 = await manager.recall(query1, {
      topK: 5,
      useSemantic: false,
      useKeyword: true,
      useGraph: false,
    });
    
    console.log(`结果：${results1.length} 条`);
    results1.forEach((r, i) => {
      console.log(`  ${i+1}. [${r.sources[0]?.source}] ${r.memoryId}: ${r.fusedScore.toFixed(4)}`);
    });
    console.log();

    // ========== 测试 3: 语义检索 ==========
    console.log('🔍 测试 3: 语义检索');
    
    const query2 = 'AI 记忆系统';
    console.log(`查询："${query2}"`);
    
    const results2 = await manager.recall(query2, {
      topK: 5,
      useSemantic: true,
      useKeyword: false,
      useGraph: false,
    });
    
    console.log(`结果：${results2.length} 条`);
    results2.forEach((r, i) => {
      console.log(`  ${i+1}. [${r.sources[0]?.source}] ${r.memoryId}: ${r.fusedScore.toFixed(4)}`);
    });
    console.log();

    // ========== 测试 4: 多路召回融合 ==========
    console.log('🔀 测试 4: 多路召回融合（RRF）');
    
    const query3 = '压缩算法';
    console.log(`查询："${query3}"`);
    
    const results3 = await manager.recall(query3, {
      topK: 5,
      useSemantic: true,
      useKeyword: true,
      useGraph: true,
    });
    
    console.log(`结果：${results3.length} 条`);
    results3.forEach((r, i) => {
      console.log(`  ${i+1}. ${r.memoryId}`);
      console.log(`      融合评分：${r.fusedScore.toFixed(4)}`);
      r.sources.forEach(s => {
        console.log(`      - ${s.source}: rank=${s.rank}, score=${s.score.toFixed(4)}`);
      });
    });
    console.log();

    // ========== 测试 5: 不同融合方法对比 ==========
    console.log('📊 测试 5: 融合方法对比');
    
    const query4 = '知识图谱';
    console.log(`查询："${query4}"\n`);
    
    const methods = ['rrf', 'borda', 'weighted', 'reciprocal'];
    
    for (const method of methods) {
      const testManager = new MultiPathRecallManager({
        fusionMethod: method,
        weights: { semantic: 0.4, keyword: 0.3, graph: 0.3 },
      });
      
      await testManager.addMemories(memories);
      
      const results = await testManager.recall(query4, {
        topK: 3,
        useSemantic: true,
        useKeyword: true,
        useGraph: true,
      });
      
      console.log(`  ${method.toUpperCase()}:`);
      results.forEach((r, i) => {
        console.log(`    ${i+1}. ${r.memoryId} (${r.fusedScore.toFixed(4)})`);
      });
      console.log();
    }

    // ========== 测试 6: 统计信息 ==========
    console.log('📊 测试 6: 统计信息');
    
    const stats = manager.getStats();
    console.log(`总记忆数：${stats.totalMemories}`);
    console.log(`BM25 统计:`);
    console.log(`  - 文档数：${stats.bm25Stats.totalDocuments}`);
    console.log(`  - 词项数：${stats.bm25Stats.totalTerms}`);
    console.log(`  - 平均长度：${stats.bm25Stats.avgDocLength.toFixed(2)}`);
    console.log(`融合方法：${stats.fusionMethod}`);
    console.log(`权重:`);
    console.log(`  - 语义：${stats.weights.semantic}`);
    console.log(`  - 关键词：${stats.weights.keyword}`);
    console.log(`  - 图：${stats.weights.graph}`);
    console.log();

    console.log('🎉 所有测试完成！\n');
  } catch (error) {
    console.error('❌ 测试失败:', error);
  }
}

runTest().catch(console.error);
