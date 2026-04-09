#!/usr/bin/env ts-node
/**
 * 记忆整理脚本
 * 
 * 用于 Cron 定时调用，执行记忆整理
 * 
 * 使用方式：
 *   npx ts-node scripts/curate-memory.ts
 *   # 或指定工作目录
 *   npx ts-node scripts/curate-memory.ts /path/to/workspace
 */

import { MemoryCurator } from '../src/curator';
import * as path from 'path';

async function main() {
  const workspaceRoot = process.argv[2] || process.cwd();

  console.log('🧠 Memory-Master 记忆整理');
  console.log('='.repeat(50));
  console.log(`工作目录：${workspaceRoot}`);
  console.log('');

  const curator = new MemoryCurator({
    workspaceRoot,
    memoryDir: 'memory',
    rawDir: 'memory/raw',
    wikiDir: 'memory/wiki',
    memoryFile: 'MEMORY.md',
    autoCompact: true,
    compactThreshold: 30,
    retentionDays: 90,
  });

  try {
    const result = await curator.curate();

    console.log('');
    console.log('✅ 整理完成！');
    console.log('='.repeat(50));
    console.log(`📄 处理文件：${result.processedFiles}`);
    console.log(`🧠 提取记忆：${result.extractedMemories.length} 条`);
    console.log(`💾 更新 MEMORY.md: ${result.updatedMemoryMd ? '✅ 是' : '⚠️ 否'}`);
    console.log(`🧹 清理文件：${result.cleanedFiles}`);
    console.log(`⏱️  耗时：${(result.duration / 1000).toFixed(2)}秒`);
    console.log('');

    // 输出提取的记忆摘要
    if (result.extractedMemories.length > 0) {
      console.log('📋 提取的记忆摘要:');
      console.log('-'.repeat(50));

      const byType: Record<string, number> = {};
      for (const item of result.extractedMemories) {
        byType[item.type] = (byType[item.type] || 0) + 1;
      }

      for (const [type, count] of Object.entries(byType)) {
        const icon = {
          'task': '📋',
          'decision': '✅',
          'insight': '💡',
          'context': '📌',
          'preference': '⭐',
        }[type] || '•';

        console.log(`  ${icon} ${type}: ${count} 条`);
      }
      console.log('');
    }

    // 输出知识摘要
    const knowledge = result.updatedKnowledge;
    console.log('📚 知识结构摘要:');
    console.log('-'.repeat(50));
    console.log(`  📁 项目：${knowledge.projects.length} 个`);
    console.log(`  👥 人物：${knowledge.people.length} 个`);
    console.log(`  ✅ 决策：${knowledge.decisions.length} 个`);
    console.log(`  📋 任务：${knowledge.tasks.length} 个`);
    console.log(`  💡 洞察：${knowledge.insights.length} 个`);
    console.log(`  ⭐ 偏好：${knowledge.preferences.length} 个`);
    console.log('');

    process.exit(0);
  } catch (error) {
    console.error('❌ 整理失败:', error);
    process.exit(1);
  }
}

main();
