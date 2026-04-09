/**
 * Memory-Master v4.0
 * 
 * 基于 Karpathy 方法论 + Anthropic 官方经验 + Claude Code 架构
 * 整合 30 篇行业最佳实践笔记
 * 
 * @author 小鬼 👻 + Jake
 * @version 4.0.0
 */

import { MemoryCapture, CaptureOptions, CaptureResult } from './capture';
import { MemoryRetriever, RetrieveOptions, RetrieveResult, Memory } from './retrieve';
import { MemoryCompactor, CompactOptions, CompactResult } from './compact';
import { filterSensitiveData, detectSensitiveData, runFilterTests } from './filter';
import { TokenOptimizer, TokenOptimizationReport, generateOptimizationReport, PrioritizedMemory } from './token-optimizer';
import { SkillEvolver } from './skill-evolver';
import { PerformanceMonitor, SkillCraftBenchmark, SkillsBenchBenchmark } from './benchmark';

/**
 * Memory-Master 主类
 */
export class MemoryMaster {
  private captureModule: MemoryCapture;
  private retrieveModule: MemoryRetriever;
  private compactor: MemoryCompactor;
  private tokenOptimizer: TokenOptimizer;
  private skillEvolver: SkillEvolver;
  private monitor: PerformanceMonitor;
  private skillCraftBenchmark: SkillCraftBenchmark;
  private skillsBenchBenchmark: SkillsBenchBenchmark;

  constructor(memoryDir: string = 'memory') {
    this.captureModule = new MemoryCapture(memoryDir);
    this.retrieveModule = new MemoryRetriever(memoryDir);
    this.compactor = new MemoryCompactor(memoryDir);
    this.tokenOptimizer = new TokenOptimizer(memoryDir);
    this.skillEvolver = new SkillEvolver(memoryDir);
    this.monitor = new PerformanceMonitor(memoryDir);
    this.skillCraftBenchmark = new SkillCraftBenchmark(memoryDir);
    this.skillsBenchBenchmark = new SkillsBenchBenchmark(memoryDir);
  }

  /**
   * 捕捉记忆
   */
  async capture(content: string, options?: CaptureOptions): Promise<CaptureResult> {
    const startTime = Date.now();
    const result = await this.captureModule.capture(content, options);
    
    // 记录性能
    this.monitor.recordResponseTime(Date.now() - startTime);
    
    return result;
  }

  /**
   * 检索记忆
   */
  async retrieve(query: string, options?: RetrieveOptions): Promise<RetrieveResult> {
    const startTime = Date.now();
    const result = await this.retrieveModule.retrieve(query, options);
    
    // 记录性能
    this.monitor.recordResponseTime(Date.now() - startTime);
    
    return result;
  }

  /**
   * 压缩记忆
   */
  async compact(options?: CompactOptions): Promise<CompactResult> {
    return this.compactor.compact(options);
  }

  /**
   * 过滤敏感数据
   */
  async filter(content: string) {
    return filterSensitiveData(content);
  }

  /**
   * 检测敏感数据
   */
  async detect(content: string) {
    return detectSensitiveData(content);
  }

  /**
   * Token 优化
   */
  async optimizeTokens(): Promise<TokenOptimizationReport> {
    // TODO: 实现记忆加载
    const memories: PrioritizedMemory[] = []; // 待实现
    return generateOptimizationReport(memories, this.tokenOptimizer);
  }

  /**
   * 记录经验
   */
  async recordExperience(
    context: string,
    action: string,
    result: 'success' | 'failure',
    feedback?: string
  ) {
    return this.skillEvolver.recordExperience(context, action, result, feedback);
  }

  /**
   * 技能蒸馏
   */
  async distillSkills() {
    return this.skillEvolver.distillSkills();
  }

  /**
   * 获取评测报告
   */
  async getBenchmarkReport(name?: string) {
    return this.monitor.generateBenchmarkReport(name);
  }

  /**
   * 运行 SkillCraft 评测
   */
  async runSkillCraftBenchmark(tasks: any[]) {
    return this.skillCraftBenchmark.evaluateToolUsage(tasks);
  }

  /**
   * 运行 SkillsBench 评测
   */
  async runSkillsBenchBenchmark(tasks: any[]) {
    return this.skillsBenchBenchmark.evaluateAcrossTasks(tasks);
  }

  /**
   * 运行测试
   */
  async test(): Promise<void> {
    console.log('🧪 Memory-Master v4.0 测试');
    console.log('=========================\n');
    
    // 运行过滤测试
    await runFilterTests();
    
    console.log('\n✅ 所有测试完成！');
  }
}

/**
 * 导出类型
 */
export {
  MemoryCapture,
  MemoryRetriever,
  MemoryCompactor,
  TokenOptimizer,
  SkillEvolver,
  PerformanceMonitor,
  SkillCraftBenchmark,
  SkillsBenchBenchmark,
  CaptureOptions,
  CaptureResult,
  RetrieveOptions,
  RetrieveResult,
  CompactOptions,
  CompactResult,
  TokenOptimizationReport,
  Memory,
};

/**
 * 导出工具函数
 */
export {
  filterSensitiveData,
  detectSensitiveData,
  runFilterTests,
  generateOptimizationReport,
};

export default MemoryMaster;
