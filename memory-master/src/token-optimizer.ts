/**
 * Memory-Master Token 优化模块
 * 
 * 基于 Mem0/MemOS 最佳实践
 * - 智能 Token 预算分配
 * - 记忆优先级排序
 * - 动态压缩触发
 * 
 * 目标：节省 60-70% Token（参考 Mem0/MemOS）
 */

import * as fs from 'fs';
import * as path from 'path';

/**
 * 记忆优先级
 */
export enum MemoryPriority {
  CRITICAL = 1,    // 关键信息（永久保留）
  HIGH = 2,        // 重要信息（保留 30 天）
  MEDIUM = 3,      // 一般信息（保留 7 天）
  LOW = 4,         // 临时信息（保留 1 天）
}

/**
 * Token 预算配置
 */
export interface TokenBudgetConfig {
  maxTokens: number;        // 最大 Token 数
  criticalReserve: number;  // 关键信息预留比例（0-1）
  compressionThreshold: number; // 压缩触发阈值（0-1）
}

/**
 * 默认配置
 */
const DEFAULT_CONFIG: TokenBudgetConfig = {
  maxTokens: 4000,          // 默认 4000 Token
  criticalReserve: 0.3,     // 30% 预留给关键信息
  compressionThreshold: 0.8, // 80% 触发压缩
};

/**
 * 记忆条目（带优先级）
 */
export interface PrioritizedMemory {
  id: string;
  content: string;
  priority: MemoryPriority;
  tokens: number;
  timestamp: number;
  lastAccessed?: number;  // 最后访问时间
  accessCount: number;    // 访问次数
}

/**
 * Token 优化器
 */
export class TokenOptimizer {
  private config: TokenBudgetConfig;
  private memoryDir: string;

  constructor(memoryDir: string = 'memory', config?: Partial<TokenBudgetConfig>) {
    this.memoryDir = memoryDir;
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  /**
   * 估算 Token 数
   */
  estimateTokens(text: string): number {
    // 中文：约 1.5 字符/Token
    // 英文：约 4 字符/Token
    const chinese = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
    const english = (text.match(/[a-zA-Z0-9]/g) || []).length;
    const other = text.length - chinese - english;
    
    return Math.floor(chinese / 1.5 + english / 4 + other / 2);
  }

  /**
   * 计算记忆优先级
   */
  calculatePriority(content: string, metadata?: { type?: string; tags?: string[] }): MemoryPriority {
    // 关键词检测
    const criticalKeywords = ['必须', '一定', '永远', '密码', '关键', '重要'];
    const highKeywords = ['记住', '偏好', '习惯', '项目', '决定'];
    const mediumKeywords = ['今天', '明天', '计划', '安排'];
    
    const lowerContent = content.toLowerCase();
    
    // 检查关键词
    if (criticalKeywords.some(kw => content.includes(kw))) {
      return MemoryPriority.CRITICAL;
    }
    
    if (highKeywords.some(kw => content.includes(kw))) {
      return MemoryPriority.HIGH;
    }
    
    if (mediumKeywords.some(kw => content.includes(kw))) {
      return MemoryPriority.MEDIUM;
    }
    
    // 默认低优先级
    return MemoryPriority.LOW;
  }

  /**
   * 智能 Token 分配
   */
  allocateTokens(memories: PrioritizedMemory[]): { allocated: PrioritizedMemory[]; saved: number } {
    // 按优先级排序
    const sorted = [...memories].sort((a, b) => a.priority - b.priority);
    
    // 计算各优先级预算
    const criticalBudget = Math.floor(this.config.maxTokens * this.config.criticalReserve);
    const remainingBudget = this.config.maxTokens - criticalBudget;
    
    const allocated: PrioritizedMemory[] = [];
    let usedTokens = 0;
    let savedTokens = 0;
    
    for (const memory of sorted) {
      // 关键信息优先保留
      if (memory.priority === MemoryPriority.CRITICAL) {
        if (usedTokens + memory.tokens <= criticalBudget) {
          allocated.push(memory);
          usedTokens += memory.tokens;
        } else {
          // 超出预算，压缩或丢弃
          savedTokens += memory.tokens;
        }
      } else {
        // 非关键信息按优先级分配
        const remainingForThis = remainingBudget * (1 - (memory.priority - 2) * 0.2);
        
        if (usedTokens + memory.tokens <= this.config.maxTokens * this.config.compressionThreshold) {
          allocated.push(memory);
          usedTokens += memory.tokens;
        } else {
          savedTokens += memory.tokens;
        }
      }
    }
    
    return {
      allocated,
      saved: savedTokens,
    };
  }

  /**
   * 动态压缩触发
   */
  shouldCompress(currentTokens: number): boolean {
    return currentTokens > this.config.maxTokens * this.config.compressionThreshold;
  }

  /**
   * 获取压缩建议
   */
  getCompressionSuggestions(memories: PrioritizedMemory[]): CompressionSuggestion[] {
    const suggestions: CompressionSuggestion[] = [];
    
    // 按优先级和时间排序
    const sorted = [...memories].sort((a, b) => {
      // 先按优先级
      if (a.priority !== b.priority) {
        return a.priority - b.priority;
      }
      // 再按最后访问时间
      return (b.lastAccessed || 0) - (a.lastAccessed || 0);
    });
    
    // 生成压缩建议
    for (const memory of sorted) {
      if (memory.priority === MemoryPriority.LOW) {
        suggestions.push({
          id: memory.id,
          action: 'compress',
          reason: '低优先级记忆',
          savedTokens: Math.floor(memory.tokens * 0.6), // 预计节省 60%
        });
      } else if (memory.priority === MemoryPriority.MEDIUM && 
                 (!memory.lastAccessed || Date.now() - memory.lastAccessed > 7 * 24 * 60 * 60 * 1000)) {
        suggestions.push({
          id: memory.id,
          action: 'compress',
          reason: '7 天未访问的中等优先级记忆',
          savedTokens: Math.floor(memory.tokens * 0.5), // 预计节省 50%
        });
      }
    }
    
    return suggestions;
  }

  /**
   * 更新访问统计
   */
  updateAccessStats(memoryId: string): void {
    const statsFile = path.join(this.memoryDir, '.access-stats.json');
    let stats: Record<string, { count: number; lastAccess: number }> = {};
    
    if (fs.existsSync(statsFile)) {
      stats = JSON.parse(fs.readFileSync(statsFile, 'utf-8'));
    }
    
    stats[memoryId] = {
      count: (stats[memoryId]?.count || 0) + 1,
      lastAccess: Date.now(),
    };
    
    fs.writeFileSync(statsFile, JSON.stringify(stats, null, 2), 'utf-8');
  }

  /**
   * 获取访问统计
   */
  getAccessStats(memoryId: string): { count: number; lastAccess: number } | null {
    const statsFile = path.join(this.memoryDir, '.access-stats.json');
    
    if (!fs.existsSync(statsFile)) {
      return null;
    }
    
    const stats = JSON.parse(fs.readFileSync(statsFile, 'utf-8'));
    return stats[memoryId] || null;
  }

  /**
   * 清理旧统计
   */
  cleanupOldStats(days: number = 30): void {
    const statsFile = path.join(this.memoryDir, '.access-stats.json');
    
    if (!fs.existsSync(statsFile)) {
      return;
    }
    
    const stats = JSON.parse(fs.readFileSync(statsFile, 'utf-8'));
    const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
    
    for (const [id, stat] of Object.entries(stats)) {
      const statObj = stat as { lastAccess: number };
      if (statObj.lastAccess < cutoff) {
        delete (stats as any)[id];
      }
    }
    
    fs.writeFileSync(statsFile, JSON.stringify(stats, null, 2), 'utf-8');
  }
}

/**
 * 压缩建议
 */
export interface CompressionSuggestion {
  id: string;
  action: 'compress' | 'delete' | 'archive';
  reason: string;
  savedTokens: number;
}

/**
 * Token 优化报告
 */
export interface TokenOptimizationReport {
  totalTokens: number;
  allocatedTokens: number;
  savedTokens: number;
  savingsRate: number;
  suggestions: CompressionSuggestion[];
}

/**
 * 生成优化报告
 */
export async function generateOptimizationReport(
  memories: PrioritizedMemory[],
  optimizer: TokenOptimizer
): Promise<TokenOptimizationReport> {
  const totalTokens = memories.reduce((sum, m) => sum + m.tokens, 0);
  const { allocated, saved } = optimizer.allocateTokens(memories);
  const allocatedTokens = allocated.reduce((sum, m) => sum + m.tokens, 0);
  const suggestions = optimizer.getCompressionSuggestions(memories);
  
  return {
    totalTokens,
    allocatedTokens,
    savedTokens: saved,
    savingsRate: totalTokens > 0 ? saved / totalTokens : 0,
    suggestions,
  };
}

// 导出
export default TokenOptimizer;
