/**
 * 知识图谱测试脚本
 */

const { KnowledgeGraph } = require('./dist/knowledge-graph');

async function runTest() {
  console.log('🧪 开始测试知识图谱引擎...\n');

  const graph = new KnowledgeGraph({
    basePath: 'memory/test-graph',
    autoSave: true,
  });

  try {
    // ========== 测试 1: 添加实体 ==========
    console.log('📝 测试 1: 添加实体');
    
    const jakeId = await graph.addEntity({
      type: 'Person',
      name: 'Jake',
      attributes: {
        age: 12,
        role: '开发者',
      },
    });
    console.log(`✅ 添加人物：Jake (${jakeId})`);

    const ghostId = await graph.addEntity({
      type: 'Person',
      name: '小鬼',
      attributes: {
        role: 'AI 助手',
      },
    });
    console.log(`✅ 添加人物：小鬼 (${ghostId})`);

    const memoryMasterId = await graph.addEntity({
      type: 'Project',
      name: 'Memory-Master',
      attributes: {
        version: '4.2.0',
        status: '开发中',
      },
    });
    console.log(`✅ 添加项目：Memory-Master (${memoryMasterId})`);

    const aaakId = await graph.addEntity({
      type: 'Skill',
      name: 'AAAK 压缩',
      attributes: {
        compressionRatio: '87%',
      },
    });
    console.log(`✅ 添加技能：AAAK 压缩 (${aaakId})\n`);

    // ========== 测试 2: 添加关系 ==========
    console.log('🔗 测试 2: 添加关系');
    
    await graph.addRelation({
      from: jakeId,
      to: memoryMasterId,
      type: 'works_on',
      description: 'Jake 开发 Memory-Master',
      weight: 1.0,
    });
    console.log(`✅ Jake works_on Memory-Master`);

    await graph.addRelation({
      from: ghostId,
      to: memoryMasterId,
      type: 'works_on',
      description: '小鬼开发 Memory-Master',
      weight: 1.0,
    });
    console.log(`✅ 小鬼 works_on Memory-Master`);

    await graph.addRelation({
      from: jakeId,
      to: ghostId,
      type: 'knows',
      description: 'Jake 知道小鬼',
      weight: 1.0,
    });
    console.log(`✅ Jake knows 小鬼`);

    await graph.addRelation({
      from: memoryMasterId,
      to: aaakId,
      type: 'uses_skill',
      description: 'Memory-Master 使用 AAAK 压缩',
      weight: 1.0,
    });
    console.log(`✅ Memory-Master uses_skill AAAK 压缩\n`);

    // ========== 测试 3: 查询实体 ==========
    console.log('🔍 测试 3: 查询实体');
    
    const persons = await graph.queryEntitiesByType('Person');
    console.log(`✅ 人物实体：${persons.length} 个`);
    persons.forEach(p => console.log(`   - ${p.name}`));

    const projects = await graph.queryEntitiesByType('Project');
    console.log(`✅ 项目实体：${projects.length} 个`);
    projects.forEach(p => console.log(`   - ${p.name}`));

    const skills = await graph.queryEntitiesByType('Skill');
    console.log(`✅ 技能实体：${skills.length} 个\n`);

    // ========== 测试 4: 搜索实体 ==========
    console.log('🔍 测试 4: 搜索实体');
    
    const searchResults = await graph.searchEntities('Memory', 10);
    console.log(`✅ 搜索 "Memory": ${searchResults.length} 个结果`);
    searchResults.forEach(r => console.log(`   - ${r.name} (${r.type})`));
    console.log();

    // ========== 测试 5: 获取邻居 ==========
    console.log('🕸️  测试 5: 获取邻居');
    
    const jakeNeighbors = await graph.getNeighbors({
      entityId: jakeId,
      direction: 'out',
    });
    console.log(`✅ Jake 的出边邻居：${jakeNeighbors.neighbors.length} 个`);
    jakeNeighbors.neighbors.forEach(n => {
      console.log(`   - ${n.relationType} -> ${n.entityId}`);
    });
    console.log();

    // ========== 测试 6: 图遍历 ==========
    console.log('🗺️  测试 6: 图遍历');
    
    const paths = await graph.traverse(jakeId, { maxDepth: 2 });
    console.log(`✅ 从 Jake 出发的路径：${paths.length} 条`);
    paths.slice(0, 5).forEach((p, i) => {
      console.log(`   ${i+1}. 长度 ${p.length}: ${p.nodes.join(' → ')}`);
    });
    console.log();

    // ========== 测试 7: 最短路径 ==========
    console.log('🎯 测试 7: 最短路径');
    
    const shortestPath = await graph.findShortestPath(jakeId, aaakId);
    if (shortestPath) {
      console.log(`✅ Jake → AAAK 压缩 最短路径:`);
      console.log(`   长度：${shortestPath.length}`);
      console.log(`   路径：${shortestPath.nodes.join(' → ')}`);
    } else {
      console.log('❌ 无路径');
    }
    console.log();

    // ========== 测试 8: 统计信息 ==========
    console.log('📊 测试 8: 统计信息');
    
    const stats = graph.getStats();
    console.log(`✅ 图谱统计:`);
    console.log(`   总实体：${stats.totalEntities}`);
    console.log(`   总关系：${stats.totalRelations}`);
    console.log(`   实体类型分布:`);
    for (const [type, count] of Object.entries(stats.entitiesByType)) {
      console.log(`     - ${type}: ${count}`);
    }
    console.log(`   关系类型分布:`);
    for (const [type, count] of Object.entries(stats.relationsByType)) {
      console.log(`     - ${type}: ${count}`);
    }
    console.log(`   平均每实体关系数：${stats.avgRelationsPerEntity.toFixed(2)}\n`);

    console.log('🎉 所有测试完成！\n');
  } catch (error) {
    console.error('❌ 测试失败:', error);
  } finally {
    graph.destroy();
  }
}

runTest().catch(console.error);
