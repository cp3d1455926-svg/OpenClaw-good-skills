/**
 * Memory-Master 记忆压缩模块
 * 
 * 基于 Claude Code 六层压缩设计
 * 简化为 3 阶段压缩：
 * - L1: 原始记录（保留 7 天）
 * - L2: 摘要提炼（保留 30 天）
 * - L3: 关键事实（永久保留）
 */

import * as fs from 'fs';
import * as path from 'path';
import * as glob from 'glob';

/**
 * 压缩级别
 */
export type CompactLevel = 'L1' | 'L2' | 'L3';

/**
 * 压缩选项
 */
export interface CompactOptions {
  force?: boolean;        // 强制压缩
  level?: CompactLevel;   // 压缩级别
  dryRun?: boolean;       // 仅预览
}

/**
 * 压缩结果
 */
export interface CompactResult {
  success: boolean;
  compressed: number;     // 压缩的记忆数
  savedTokens: number;    // 节省的 token 数
  compressionRate: number; // 压缩率（0-1）
  details?: CompactDetail[];
}

/**
 * 压缩详情
 */
export interface CompactDetail {
  id: string;
  from: string;
  to: string;
  savedTokens: number;
  level: CompactLevel;
}

/**
 * 记忆压缩器
 */
export class MemoryCompactor {
  private memoryDir: string;

  constructor(memoryDir: string = 'memory') {
    this.memoryDir = memoryDir;
  }

  /**
   * 执行压缩
   */
  async compact(options: CompactOptions = {}): Promise<CompactResult> {
    const {
      force = false,
      level = 'L2',
      dryRun = false,
    } = options;

    const details: CompactDetail[] = [];
    let totalCompressed = 0;
    let totalSavedTokens = 0;
    let totalOriginalTokens = 0;

    // 1. 获取所有记忆文件
    const files = glob.sync(path.join(this.memoryDir, '*.md'));
    
    // 2. 遍历文件
    for (const file of files) {
      const fileName = path.basename(file);
      
      // 跳过 MEMORY.md（长期记忆不自动压缩）
      if (fileName === 'MEMORY.md') {
        continue;
      }
      
      // 解析日期
      const dateMatch = fileName.match(/(\d{4}-\d{2}-\d{2})\.md/);
      if (!dateMatch) continue;
      
      const fileDate = dateMatch[1];
      const daysOld = this.getDaysOld(fileDate);
      
      // 3. 根据天数决定压缩级别
      let targetLevel: CompactLevel;
      
      if (daysOld <= 7) {
        targetLevel = 'L1'; // 7 天内保留原始
      } else if (daysOld <= 30) {
        targetLevel = 'L2'; // 30 天内摘要
      } else {
        targetLevel = 'L3'; // 30 天以上关键事实
      }
      
      // 如果指定了级别，使用指定级别
      if (level) {
        targetLevel = level;
      }
      
      // 4. 执行压缩
      const content = fs.readFileSync(file, 'utf-8');
      const compressed = await this.compressContent(content, targetLevel, file);
      
      if (compressed) {
        details.push(...compressed);
        
        for (const detail of compressed) {
          totalCompressed++;
          totalSavedTokens += detail.savedTokens;
          const compressionRate = targetLevel === 'L1' ? 0 : targetLevel === 'L2' ? 0.5 : 0.8;
          totalOriginalTokens += detail.savedTokens / (1 - compressionRate);
        }
        
        // 5. 写入文件（如果不是 dryRun）
        if (!dryRun) {
          const newContent = this.applyCompression(content, compressed);
          fs.writeFileSync(file, newContent, 'utf-8');
        }
      }
    }

    // 6. 返回结果
    return {
      success: true,
      compressed: totalCompressed,
      savedTokens: totalSavedTokens,
      compressionRate: totalOriginalTokens > 0 ? totalSavedTokens / totalOriginalTokens : 0,
      details: dryRun ? details : undefined,
    };
  }

  /**
   * 压缩内容
   */
  private async compressContent(
    content: string,
    level: CompactLevel,
    filePath: string
  ): Promise<CompactDetail[] | null> {
    const details: CompactDetail[] = [];
    
    // 提取记忆块
    const memories = this.extractMemories(content);
    
    for (const memory of memories) {
      const compressed = this.compressMemory(memory.content, level);
      
      if (compressed && compressed.to !== memory.content) {
        const savedTokens = this.estimateTokens(memory.content) - this.estimateTokens(compressed.to);
        
        details.push({
          id: memory.id,
          from: memory.content,
          to: compressed.to,
          savedTokens,
          level,
        });
      }
    }
    
    return details.length > 0 ? details : null;
  }

  /**
   * 压缩单条记忆
   */
  private compressMemory(
    content: string,
    level: CompactLevel
  ): { from: string; to: string } | null {
    const original = content;
    
    switch (level) {
      case 'L1':
        // L1: 保留原始，不做压缩
        return null;
      
      case 'L2':
        // L2: 摘要提炼
        const summary = this.generateSummary(original);
        return {
          from: original,
          to: summary,
        };
      
      case 'L3':
        // L3: 只保留关键事实
        const facts = this.extractKeyFacts(original);
        return {
          from: original,
          to: facts,
        };
      
      default:
        return null;
    }
  }

  /**
   * 生成摘要
   */
  private generateSummary(content: string): string {
    // 简单实现：提取前 3 个非空行
    // TODO: 使用 LLM 生成摘要
    const lines = content.split('\n').filter(line => line.trim());
    const summary = lines.slice(0, 3).join('\n');
    return summary + '\n\n[摘要 - 原始内容已压缩]';
  }

  /**
   * 提取关键事实
   */
  private extractKeyFacts(content: string): string {
    // 简单实现：提取包含关键词的行
    // TODO: 使用 LLM 提取关键事实
    const keywords = ['记住', '重要', '必须', '关键', '决定', '结论'];
    const lines = content.split('\n');
    
    const keyLines = lines.filter(line => 
      keywords.some(keyword => line.includes(keyword))
    );
    
    if (keyLines.length === 0) {
      // 如果没有关键词，保留第一行
      return lines[0] + '\n\n[关键事实 - 原始内容已压缩]';
    }
    
    return keyLines.join('\n') + '\n\n[关键事实 - 原始内容已压缩]';
  }

  /**
   * 应用压缩
   */
  private applyCompression(content: string, details: CompactDetail[]): string {
    let result = content;
    
    for (const detail of details) {
      result = result.replace(detail.from, detail.to);
    }
    
    return result;
  }

  /**
   * 提取记忆
   */
  private extractMemories(content: string): { id: string; content: string }[] {
    const memories: { id: string; content: string }[] = [];
    const lines = content.split('\n');
    
    let currentId = '';
    let currentContent = '';
    
    for (const line of lines) {
      if (line.startsWith('**ID**:')) {
        currentId = line.replace('**ID**:', '').trim();
      } else if (line.startsWith('## ') || line.startsWith('### ')) {
        if (currentId && currentContent) {
          memories.push({ id: currentId, content: currentContent });
        }
        currentContent = line + '\n';
      } else if (currentId) {
        currentContent += line + '\n';
      }
    }
    
    if (currentId && currentContent) {
      memories.push({ id: currentId, content: currentContent });
    }
    
    return memories;
  }

  /**
   * 估算 token 数
   */
  private estimateTokens(text: string): number {
    // 简单估算：中文字符数 / 2 + 英文字符数
    const chinese = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
    const english = (text.match(/[a-zA-Z0-9]/g) || []).length;
    return Math.floor(chinese / 2 + english / 4);
  }

  /**
   * 计算文件天数
   */
  private getDaysOld(dateStr: string): number {
    const fileDate = new Date(dateStr);
    const today = new Date();
    const diff = today.getTime() - fileDate.getTime();
    return Math.floor(diff / (1000 * 60 * 60 * 24));
  }
}

// 导出
export default MemoryCompactor;
