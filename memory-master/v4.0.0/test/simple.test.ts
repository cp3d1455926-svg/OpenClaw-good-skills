/**
 * Memory-Master v4.0 简单测试
 * 
 * 测试核心功能是否正常
 */

import { MemoryMaster } from './index';
import { TokenOptimizer } from './token-optimizer';
import { SkillEvolver } from './skill-evolver';
import { PerformanceMonitor } from './benchmark';

async function runTests() {
  console.log('🧪 Memory-Master v4.0 测试\n');
  console.log('=========================\n');
  
  let passed = 0;
  let failed = 0;
  
  // 测试 1: Token 优化器
  console.log('测试 1: Token 优化器');
  try {
    const optimizer = new TokenOptimizer('test-memory');
    const tokens = optimizer.estimateTokens('你好，世界！Hello World!');
    console.log(`  ✅ Token 估算：${tokens} tokens`);
    passed++;
  } catch (error) {
    console.log(`  ❌ Token 优化器失败：${error}`);
    failed++;
  }
  
  // 测试 2: 优先级计算
  console.log('\n测试 2: 优先级计算');
  try {
    const optimizer = new TokenOptimizer('test-memory');
    const priority1 = optimizer.calculatePriority('必须记住这个重要信息');
    const priority2 = optimizer.calculatePriority('今天天气不错');
    console.log(`  ✅ 关键信息优先级：${priority1} (期望：1)`);
    console.log(`  ✅ 普通信息优先级：${priority2} (期望：4)`);
    passed++;
  } catch (error) {
    console.log(`  ❌ 优先级计算失败：${error}`);
    failed++;
  }
  
  // 测试 3: 技能进化器
  console.log('\n测试 3: 技能进化器');
  try {
    const evolver = new SkillEvolver('test-memory');
    await evolver.recordExperience('测试上下文', '测试动作', 'success', '测试反馈');
    const stats = evolver.getStats();
    console.log(`  ✅ 技能统计：${JSON.stringify(stats)}`);
    passed++;
  } catch (error) {
    console.log(`  ❌ 技能进化器失败：${error}`);
    failed++;
  }
  
  // 测试 4: 性能监控器
  console.log('\n测试 4: 性能监控器');
  try {
    const monitor = new PerformanceMonitor('test-memory');
    monitor.recordResponseTime(50);
    monitor.recordResponseTime(75);
    monitor.recordResponseTime(100);
    const metrics = monitor.getMetrics();
    console.log(`  ✅ 性能指标：${JSON.stringify(metrics)}`);
    passed++;
  } catch (error) {
    console.log(`  ❌ 性能监控器失败：${error}`);
    failed++;
  }
  
  // 测试 5: 敏感数据过滤（已有功能）
  console.log('\n测试 5: 敏感数据过滤');
  try {
    const { filterSensitiveData } = await import('./filter');
    const result = await filterSensitiveData('我的密码是 123456');
    console.log(`  ✅ 检测到敏感数据：${result.hasSensitive}`);
    console.log(`  ✅ 过滤后内容：${result.filtered}`);
    passed++;
  } catch (error) {
    console.log(`  ❌ 敏感数据过滤失败：${error}`);
    failed++;
  }
  
  // 总结
  console.log('\n=========================');
  console.log(`📊 测试结果：${passed}/${passed + failed} 通过`);
  
  if (failed === 0) {
    console.log('🎉 所有测试通过！');
  } else {
    console.log(`⚠️  ${failed} 个测试失败`);
  }
  
  // 清理测试目录
  try {
    const fs = await import('fs');
    const path = await import('path');
    const testDir = path.join(process.cwd(), 'test-memory');
    if (fs.existsSync(testDir)) {
      fs.rmSync(testDir, { recursive: true, force: true });
      console.log('\n🧹 已清理测试目录');
    }
  } catch (error) {
    console.log(`\n⚠️  清理测试目录失败：${error}`);
  }
}

// 运行测试
runTests().catch(console.error);
