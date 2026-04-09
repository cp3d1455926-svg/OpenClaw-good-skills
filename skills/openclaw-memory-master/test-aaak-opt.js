/**
 * AAAK 优化测试 - 改进锚点识别
 */

const { AAAKCompressor } = require('./dist/aaak-compressor');

async function runOptimizedTest() {
  console.log('🧪 AAAK 优化测试...\n');

  const compressor = new AAAKCompressor({
    preserveOriginal: false,
    minAnchorWeight: 0.1,  // 降低阈值
  });

  const testText = `
Memory-Master 是一个 AI 记忆系统，由 Jake 和小鬼共同开发。
项目采用了分层架构，包括 L0 热存储、L1 温存储、L2 冷存储。
AAAK 压缩算法参考了 MemPalace 的研究成果。
OpenClaw 是强大的 Agent 框架。
`;

  console.log('📝 测试文本:');
  console.log(`   长度：${testText.length} 字符\n`);

  // 压缩
  const compressed = await compressor.compress(testText, 'opt-test-001');

  console.log('⚓ 锚点:');
  console.log(`   数量：${compressed.anchors.length}`);
  compressed.anchors.forEach((a, i) => {
    console.log(`   ${i+1}. "${a.text}" - 类型：${a.type}, 权重：${a.weight.toFixed(3)}`);
  });

  console.log('\n🧠 实体:');
  console.log(`   数量：${compressed.knowledge.entities.length}`);
  compressed.knowledge.entities.forEach((e, i) => {
    console.log(`   ${i+1}. ${e.name} (${e.type})`);
  });

  console.log('\n🔗 关系:');
  console.log(`   数量：${compressed.knowledge.relations.length}`);
  compressed.knowledge.relations.forEach((r, i) => {
    console.log(`   ${i+1}. ${r.from} → ${r.to} (${r.type})`);
  });
}

runOptimizedTest().catch(console.error);
