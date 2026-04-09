/**
 * Layered Memory Manager 测试脚本
 * 
 * 测试 L0/L1/L2 分层存储系统
 * 
 * @author 小鬼 👻 + Jake
 * @version 4.2.0
 */

import { LayeredMemoryManager } from '../src/layered-manager';

async function runTests() {
  console.log('🧪 开始测试 Layered Memory Manager...\n');

  const manager = new LayeredMemoryManager('memory/test-layered');

  try {
    // ========== 测试 1: 基础写入 ==========
    console.log('📝 测试 1: 基础写入');
    const id1 = await manager.write('这是第一条测试记忆', {
      type: 'test',
      tags: ['测试', 'L0'],
    });
    console.log(`✅ 写入记忆：${id1}`);

    const id2 = await manager.write('这是第二条测试记忆', {
      type: 'test',
      tags: ['测试', 'L0'],
    });
    console.log(`✅ 写入记忆：${id2}\n`);

    // ========== 测试 2: 读取记忆 ==========
    console.log('📖 测试 2: 读取记忆');
    const memory1 = await manager.read(id1);
    if (memory1) {
      console.log(`✅ 读取成功:`);
      console.log(`   ID: ${memory1.id}`);
      console.log(`   内容：${memory1.content}`);
      console.log(`   层级：${memory1.layer}`);
      console.log(`   类型：${memory1.type}`);
    } else {
      console.log('❌ 读取失败');
    }
    console.log();

    // ========== 测试 3: 搜索记忆 ==========
    console.log('🔍 测试 3: 搜索记忆');
    const results = await manager.search('测试', { limit: 10 });
    console.log(`✅ 搜索结果：${results.length} 条`);
    for (const memory of results) {
      console.log(`   - [${memory.layer}] ${memory.content}`);
    }
    console.log();

    // ========== 测试 4: 批量写入 ==========
    console.log('📦 测试 4: 批量写入');
    const batchIds = await manager.batchWrite(
      Array.from({ length: 10 }, (_, i) => ({
        content: `批量测试记忆 ${i + 1}`,
        options: {
          type: 'batch-test',
          tags: ['批量', '测试'],
        },
      }))
    );
    console.log(`✅ 批量写入 ${batchIds.length} 条记忆`);
    console.log(`   IDs: ${batchIds.slice(0, 3).join(', ')}...\n`);

    // ========== 测试 5: 按类型筛选 ==========
    console.log('🏷️  测试 5: 按类型筛选');
    const byType = await manager.getByType('test', 10);
    console.log(`✅ 类型 'test' 的记忆：${byType.length} 条`);
    console.log();

    // ========== 测试 6: 按标签筛选 ==========
    console.log('🏷️  测试 6: 按标签筛选');
    const byTags = await manager.getByTags(['测试'], 10);
    console.log(`✅ 标签 '测试' 的记忆：${byTags.length} 条`);
    console.log();

    // ========== 测试 7: 统计信息 ==========
    console.log('📊 测试 7: 统计信息');
    const stats = manager.getStats();
    console.log('✅ 分层统计:');
    console.log(`   L0 (热存储):`);
    console.log(`     - 数量：${stats.l0.size}/${stats.l0.maxSize}`);
    console.log(`     - 内存：${(stats.l0.memoryUsage / 1024).toFixed(2)} KB`);
    console.log(`   L1 (温存储):`);
    console.log(`     - 数量：${stats.l1.totalMemories}`);
    console.log(`     - 天数：${stats.l1.totalDays}`);
    console.log(`     - 缓存：${stats.l1.cacheUsage}`);
    console.log(`   L2 (冷存储):`);
    console.log(`     - 数量：${stats.l2.totalMemories}`);
    console.log(`     - 月数：${stats.l2.totalMonths}`);
    console.log(`     - 归档：${stats.l2.archivedMonths}`);
    console.log(`   总计：${stats.total} 条记忆\n`);

    // ========== 测试 8: 删除记忆 ==========
    console.log('🗑️  测试 8: 删除记忆');
    const deleted = await manager.delete(id1);
    console.log(`✅ 删除 ${deleted ? '成功' : '失败'}: ${id1}`);
    
    const memoryAfterDelete = await manager.read(id1);
    console.log(`   验证：${memoryAfterDelete ? '❌ 仍存在' : '✅ 已删除'}\n`);

    // ========== 测试 9: 跨层搜索 ==========
    console.log('🔍 测试 9: 跨层搜索');
    const crossLayerResults = await manager.search('测试', {
      limit: 20,
      layers: ['L0', 'L1', 'L2'],
    });
    console.log(`✅ 跨层搜索结果：${crossLayerResults.length} 条`);
    
    const layerCount: Record<string, number> = { L0: 0, L1: 0, L2: 0 };
    for (const memory of crossLayerResults) {
      layerCount[memory.layer]++;
    }
    console.log(`   L0: ${layerCount.L0} 条`);
    console.log(`   L1: ${layerCount.L1} 条`);
    console.log(`   L2: ${layerCount.L2} 条\n`);

    // ========== 测试 10: 性能测试 ==========
    console.log('⚡ 测试 10: 性能测试');
    const perfStart = Date.now();
    
    // 写入 100 条记忆
    const perfIds = await manager.batchWrite(
      Array.from({ length: 100 }, (_, i) => ({
        content: `性能测试记忆 ${i + 1} - ${'x'.repeat(100)}`,
        options: {
          type: 'perf-test',
          tags: ['性能', '测试'],
        },
      }))
    );
    
    const writeTime = Date.now() - perfStart;
    console.log(`✅ 写入 100 条记忆：${writeTime}ms (${(writeTime / 100).toFixed(2)}ms/条)`);
    
    // 搜索测试
    const searchStart = Date.now();
    await manager.search('性能', { limit: 50 });
    const searchTime = Date.now() - searchStart;
    console.log(`✅ 搜索记忆：${searchTime}ms\n`);

    // ========== 最终统计 ==========
    console.log('📊 最终统计');
    const finalStats = manager.getStats();
    console.log(`   总记忆数：${finalStats.total} 条`);
    console.log(`   L0: ${finalStats.l0.size} 条`);
    console.log(`   L1: ${finalStats.l1.totalMemories} 条`);
    console.log(`   L2: ${finalStats.l2.totalMemories} 条`);
    console.log();

    console.log('🎉 所有测试完成！\n');
  } catch (error) {
    console.error('❌ 测试失败:', error);
  } finally {
    // 清理
    manager.destroy();
    console.log('✅ 测试资源已清理\n');
  }
}

// 运行测试
runTests().catch(console.error);
