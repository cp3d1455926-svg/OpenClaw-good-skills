/**
 * Memory-Master 评测基准模块
 * 
 * 基于 SkillCraft / SkillsBench 论文
 * - 基础评测指标
 * - 性能监控
 * - 质量报告
 */

import * as fs from 'fs';
import * as path from 'path';

/**
 * 评测指标
 */
export interface Metrics {
  // 准确性指标
  retrievalAccuracy?: number;     // 检索准确率
  relevanceScore?: number;        // 相关性评分
  
  // 性能指标
  avgResponseTime?: number;       // 平均响应时间（ms）
  p95ResponseTime?: number;       // P95 响应时间（ms）
  p99ResponseTime?: number;       // P99 响应时间（ms）
  
  // 效率指标
  tokenSavingsRate?: number;      // Token 节省率
  compressionRate?: number;       // 压缩率
  
  // 质量指标
  userSatisfaction?: number;      // 用户满意度
  errorRate?: number;             // 错误率
}

/**
 * 评测结果
 */
export interface BenchmarkResult {
  id: string;
  name: string;
  timestamp: number;
  metrics: Metrics;
  details?: Record<string, any>;
}

/**
 * 性能监控器
 */
export class PerformanceMonitor {
  private metricsFile: string;
  private responseTimes: number[] = [];

  constructor(memoryDir: string = 'memory') {
    this.metricsFile = path.join(memoryDir, '.metrics.json');
  }

  /**
   * 记录响应时间
   */
  recordResponseTime(timeMs: number): void {
    this.responseTimes.push(timeMs);
    
    // 每 100 次记录保存一次
    if (this.responseTimes.length >= 100) {
      this.saveMetrics();
      this.responseTimes = [];
    }
  }

  /**
   * 记录检索准确性
   */
  recordRetrievalAccuracy(isRelevant: boolean): void {
    const metrics = this.loadMetrics();
    
    if (!metrics.retrievalAccuracy) {
      metrics.retrievalAccuracy = { total: 0, relevant: 0 };
    }
    
    metrics.retrievalAccuracy.total++;
    if (isRelevant) {
      metrics.retrievalAccuracy.relevant++;
    }
    
    this.saveMetrics(metrics);
  }

  /**
   * 记录 Token 使用
   */
  recordTokenUsage(original: number, optimized: number): void {
    const metrics = this.loadMetrics();
    
    if (!metrics.tokenUsage) {
      metrics.tokenUsage = { total: 0, saved: 0, count: 0 };
    }
    
    metrics.tokenUsage.total += original;
    metrics.tokenUsage.saved += (original - optimized);
    metrics.tokenUsage.count++;
    
    this.saveMetrics(metrics);
  }

  /**
   * 记录错误
   */
  recordError(errorType: string): void {
    const metrics = this.loadMetrics();
    
    if (!metrics.errors) {
      metrics.errors = {};
    }
    
    metrics.errors[errorType] = (metrics.errors[errorType] || 0) + 1;
    
    this.saveMetrics(metrics);
  }

  /**
   * 获取当前指标
   */
  getMetrics(): Metrics {
    const metrics = this.loadMetrics();
    
    // 计算响应时间统计
    const responseTimeMetrics = this.calculateResponseTimeStats();
    
    // 计算检索准确率
    const retrievalAccuracy = metrics.retrievalAccuracy ?
      metrics.retrievalAccuracy.relevant / metrics.retrievalAccuracy.total : 0;
    
    // 计算 Token 节省率
    const tokenSavingsRate = metrics.tokenUsage && metrics.tokenUsage.count > 0 ?
      metrics.tokenUsage.saved / metrics.tokenUsage.total : 0;
    
    // 计算错误率
    const totalOps = metrics.totalOperations || 0;
    const totalErrors = metrics.errors ?
      Object.values(metrics.errors).reduce((sum: number, count: any) => sum + (count as number), 0) : 0;
    const errorRate = totalOps > 0 ? totalErrors / totalOps : 0;
    
    return {
      retrievalAccuracy,
      tokenSavingsRate,
      errorRate,
      ...responseTimeMetrics,
    };
  }

  /**
   * 计算响应时间统计
   */
  private calculateResponseTimeStats(): {
    avgResponseTime?: number;
    p95ResponseTime?: number;
    p99ResponseTime?: number;
  } {
    if (this.responseTimes.length === 0) {
      return {};
    }
    
    const sorted = [...this.responseTimes].sort((a, b) => a - b);
    const len = sorted.length;
    
    return {
      avgResponseTime: sorted.reduce((a, b) => a + b, 0) / len,
      p95ResponseTime: sorted[Math.floor(len * 0.95)],
      p99ResponseTime: sorted[Math.floor(len * 0.99)],
    };
  }

  /**
   * 生成评测报告
   */
  generateBenchmarkReport(name: string = 'Memory-Master Benchmark'): BenchmarkResult {
    const metrics = this.getMetrics();
    
    return {
      id: this.generateId(),
      name,
      timestamp: Date.now(),
      metrics,
    };
  }

  /**
   * 保存评测报告
   */
  saveBenchmarkReport(report: BenchmarkResult): void {
    const reportsFile = path.join(path.dirname(this.metricsFile), 'benchmarks.json');
    let reports: BenchmarkResult[] = [];
    
    if (fs.existsSync(reportsFile)) {
      reports = JSON.parse(fs.readFileSync(reportsFile, 'utf-8'));
    }
    
    reports.push(report);
    fs.writeFileSync(reportsFile, JSON.stringify(reports, null, 2), 'utf-8');
  }

  /**
   * 加载指标
   */
  private loadMetrics(): any {
    if (!fs.existsSync(this.metricsFile)) {
      return {};
    }
    
    return JSON.parse(fs.readFileSync(this.metricsFile, 'utf-8'));
  }

  /**
   * 保存指标
   */
  private saveMetrics(metrics?: any): void {
    const data = metrics || {
      retrievalAccuracy: { total: 0, relevant: 0 },
      tokenUsage: { total: 0, saved: 0, count: 0 },
      errors: {},
      totalOperations: 0,
    };
    
    fs.writeFileSync(this.metricsFile, JSON.stringify(data, null, 2), 'utf-8');
  }

  /**
   * 生成 ID
   */
  private generateId(): string {
    return `benchmark-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`;
  }

  /**
   * 清理旧报告
   */
  cleanupOldReports(days: number = 30): void {
    const reportsFile = path.join(path.dirname(this.metricsFile), 'benchmarks.json');
    
    if (!fs.existsSync(reportsFile)) {
      return;
    }
    
    const reports = JSON.parse(fs.readFileSync(reportsFile, 'utf-8'));
    const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
    
    const filtered = reports.filter((r: BenchmarkResult) => r.timestamp > cutoff);
    
    if (filtered.length !== reports.length) {
      fs.writeFileSync(reportsFile, JSON.stringify(filtered, null, 2), 'utf-8');
    }
  }
}

/**
 * SkillCraft 风格评测
 */
export class SkillCraftBenchmark {
  private monitor: PerformanceMonitor;

  constructor(memoryDir: string = 'memory') {
    this.monitor = new PerformanceMonitor(memoryDir);
  }

  /**
   * 评测工具使用能力
   */
  async evaluateToolUsage(
    tasks: Array<{
      name: string;
      context: string;
      expectedTool: string;
    }>
  ): Promise<{
    accuracy: number;
    efficiency: number;
    report: string;
  }> {
    let correct = 0;
    let totalSteps = 0;
    let optimalSteps = 0;
    
    for (const task of tasks) {
      // 模拟执行
      const result = await this.executeTask(task);
      
      if (result.toolUsed === task.expectedTool) {
        correct++;
      }
      
      totalSteps += result.steps;
      optimalSteps += result.optimalSteps;
    }
    
    const accuracy = tasks.length > 0 ? correct / tasks.length : 0;
    const efficiency = optimalSteps > 0 ? optimalSteps / totalSteps : 0;
    
    return {
      accuracy,
      efficiency,
      report: this.generateSkillCraftReport(accuracy, efficiency),
    };
  }

  /**
   * 执行任务（模拟）
   */
  private async executeTask(task: {
    name: string;
    context: string;
    expectedTool: string;
  }): Promise<{
    toolUsed: string;
    steps: number;
    optimalSteps: number;
  }> {
    // TODO: 实际执行任务
    // 这里只是模拟
    return {
      toolUsed: task.expectedTool,
      steps: 3,
      optimalSteps: 2,
    };
  }

  /**
   * 生成 SkillCraft 报告
   */
  private generateSkillCraftReport(accuracy: number, efficiency: number): string {
    const accuracyLevel = accuracy >= 0.9 ? '优秀' : accuracy >= 0.7 ? '良好' : '需改进';
    const efficiencyLevel = efficiency >= 0.9 ? '优秀' : efficiency >= 0.7 ? '良好' : '需改进';
    
    return `
SkillCraft 评测报告
==================

工具使用准确率：${(accuracy * 100).toFixed(1)}% (${accuracyLevel})
执行效率：${(efficiency * 100).toFixed(1)}% (${efficiencyLevel})

建议：
${accuracy < 0.7 ? '- 加强工具选择训练' : ''}
${efficiency < 0.7 ? '- 优化执行流程，减少冗余步骤' : ''}
${accuracy >= 0.7 && efficiency >= 0.7 ? '- 表现良好，继续保持' : ''}
`.trim();
  }
}

/**
 * SkillsBench 风格评测
 */
export class SkillsBenchBenchmark {
  private monitor: PerformanceMonitor;

  constructor(memoryDir: string = 'memory') {
    this.monitor = new PerformanceMonitor(memoryDir);
  }

  /**
   * 跨任务技能评测
   */
  async evaluateAcrossTasks(
    tasks: Array<{
      category: string;
      name: string;
      difficulty: 'easy' | 'medium' | 'hard';
    }>
  ): Promise<{
    byCategory: Record<string, number>;
    byDifficulty: Record<string, number>;
    overall: number;
    report: string;
  }> {
    const results = await this.executeTasks(tasks);
    
    // 按类别统计
    const byCategory: Record<string, { correct: number; total: number }> = {};
    const byDifficulty: Record<string, { correct: number; total: number }> = {};
    
    for (const result of results) {
      // 按类别
      if (!byCategory[result.category]) {
        byCategory[result.category] = { correct: 0, total: 0 };
      }
      byCategory[result.category].total++;
      if (result.success) {
        byCategory[result.category].correct++;
      }
      
      // 按难度
      if (!byDifficulty[result.difficulty]) {
        byDifficulty[result.difficulty] = { correct: 0, total: 0 };
      }
      byDifficulty[result.difficulty].total++;
      if (result.success) {
        byDifficulty[result.difficulty].correct++;
      }
    }
    
    // 计算准确率
    const categoryAccuracy = Object.fromEntries(
      Object.entries(byCategory).map(([cat, data]) => [
        cat,
        data.total > 0 ? data.correct / data.total : 0,
      ])
    );
    
    const difficultyAccuracy = Object.fromEntries(
      Object.entries(byDifficulty).map(([diff, data]) => [
        diff,
        data.total > 0 ? data.correct / data.total : 0,
      ])
    );
    
    const totalCorrect = results.filter(r => r.success).length;
    const overall = results.length > 0 ? totalCorrect / results.length : 0;
    
    return {
      byCategory: categoryAccuracy,
      byDifficulty: difficultyAccuracy,
      overall,
      report: this.generateSkillsBenchReport(categoryAccuracy, difficultyAccuracy, overall),
    };
  }

  /**
   * 执行任务（模拟）
   */
  private async executeTasks(
    tasks: Array<{ category: string; name: string; difficulty: string }>
  ): Promise<Array<{
    category: string;
    difficulty: string;
    success: boolean;
  }>> {
    // TODO: 实际执行任务
    // 这里只是模拟
    return tasks.map(task => ({
      category: task.category,
      difficulty: task.difficulty,
      success: Math.random() > 0.3, // 模拟 70% 成功率
    }));
  }

  /**
   * 生成 SkillsBench 报告
   */
  private generateSkillsBenchReport(
    byCategory: Record<string, number>,
    byDifficulty: Record<string, number>,
    overall: number
  ): string {
    let report = `
SkillsBench 跨任务评测报告
========================

整体准确率：${(overall * 100).toFixed(1)}%

按类别：
`.trim();
    
    for (const [cat, acc] of Object.entries(byCategory)) {
      report += `\n- ${cat}: ${(acc * 100).toFixed(1)}%`;
    }
    
    report += '\n\n按难度：';
    for (const [diff, acc] of Object.entries(byDifficulty)) {
      report += `\n- ${diff}: ${(acc * 100).toFixed(1)}%`;
    }
    
    return report;
  }
}
