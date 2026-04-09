/**
 * 简单测试脚本 - 验证 L0/L1/L2 分层系统
 */

const { LayeredMemoryManager } = require('./dist/layered-manager');

async function runTest() {
  console.log('🧪 开始测试 Layered Memory Manager...\n');

  const manager = new LayeredMemoryManager('memory/test-layered');

  try {
    // 测试 1: 写入
    console.log('📝 测试 1: 写入记忆');
    const id1 = await manager.write('这是第一条测试记忆', {
      type: 'test',
      tags: ['测试', 'L0'],
    });
    console.log(`✅ 写入成功：${id1}\n`);

    // 测试 2: 读取
    console.log('📖 测试 2: 读取记忆');
    const memory = await manager.read(id1);
    if (memory) {
      console.log(`✅ 读取成功:`);
      console.log(`   内容：${memory.content}`);
      console.log(`   层级：${memory.layer}`);
      console.log(`   类型：${memory.type}\n`);
    }

    // 测试 3: 搜索
    console.log('🔍 测试 3: 搜索记忆');
    const results = await manager.search('测试', { limit: 10 });
    console.log(`✅ 搜索结果：${results.length} 条`);
    for (const m of results) {
      console.log(`   - [${m.layer}] ${m.content}`);
    }
    console.log();

    // 测试 4: 统计
    console.log('📊 测试 4: 统计信息');
    const stats = manager.getStats();
    console.log(`   总记忆数：${stats.total}`);
    console.log(`   L0: ${stats.l0.size} 条`);
    console.log(`   L1: ${stats.l1.totalMemories} 条`);
    console.log(`   L2: ${stats.l2.totalMemories} 条\n`);

    console.log('🎉 测试完成！\n');
  } catch (error) {
    console.error('❌ 测试失败:', error);
  } finally {
    manager.destroy();
  }
}

runTest().catch(console.error);
