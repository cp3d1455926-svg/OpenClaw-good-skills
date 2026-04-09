/**
 * Memory-Master 记忆检索模块
 * 
 * 支持 5 种查询类型（基于 Karpathy 方法论）
 * - procedural: 流程查询
 * - temporal: 时间查询
 * - relational: 关系查询
 * - persona: 偏好查询
 * - factual: 事实查询
 */

import * as fs from 'fs';
import * as path from 'path';
import * as glob from 'glob';

/**
 * 查询类型
 */
export type QueryType = 'procedural' | 'temporal' | 'relational' | 'persona' | 'factual';

/**
 * 检索选项
 */
export interface RetrieveOptions {
  type?: QueryType;
  limit?: number;         // 返回数量（默认 5）
  timeRange?: {
    start?: string;       // 开始日期
    end?: string;         // 结束日期
  };
  includeRaw?: boolean;   // 包含原始记录
}

/**
 * 记忆条目
 */
export interface Memory {
  id: string;
  type: string;
  content: string;
  timestamp: number;
  metadata?: {
    source?: string;
    topic?: string;
    project?: string;
  };
  path?: string;
}

/**
 * 检索结果
 */
export interface RetrieveResult {
  success: boolean;
  queryType: QueryType;
  memories: Memory[];
  timeMs: number;
}

/**
 * 记忆检索器
 */
export class MemoryRetriever {
  private memoryDir: string;
  private memoryFile: string;

  constructor(memoryDir: string = 'memory') {
    this.memoryDir = memoryDir;
    this.memoryFile = path.join(memoryDir, 'MEMORY.md');
  }

  /**
   * 检索记忆
   */
  async retrieve(query: string, options: RetrieveOptions = {}): Promise<RetrieveResult> {
    const startTime = Date.now();
    
    const {
      type = this.classifyQuery(query),
      limit = 5,
      timeRange,
      includeRaw = false,
    } = options;

    // 1. 根据查询类型选择检索策略
    let memories: Memory[] = [];
    
    switch (type) {
      case 'procedural':
        memories = await this.searchProcedural(query, limit);
        break;
      case 'temporal':
        memories = await this.searchTemporal(query, limit, timeRange);
        break;
      case 'relational':
        memories = await this.searchRelational(query, limit);
        break;
      case 'persona':
        memories = await this.searchPersona(query, limit);
        break;
      case 'factual':
        memories = await this.searchFactual(query, limit);
        break;
    }

    // 2. 限制返回数量
    memories = memories.slice(0, limit);

    // 3. 返回结果
    return {
      success: true,
      queryType: type,
      memories,
      timeMs: Date.now() - startTime,
    };
  }

  /**
   * 自动分类查询类型
   */
  private classifyQuery(query: string): QueryType {
    const q = query.toLowerCase();
    
    // 流程查询关键词
    if (q.includes('如何') || q.includes('怎么做') || q.includes('步骤') || q.includes('流程')) {
      return 'procedural';
    }
    
    // 时间查询关键词
    if (q.includes('什么时候') || q.includes('昨天') || q.includes('今天') || 
        q.includes('明天') || q.includes('上周') || q.includes('下周')) {
      return 'temporal';
    }
    
    // 偏好查询关键词
    if (q.includes('喜欢') || q.includes('偏好') || q.includes('习惯') || 
        q.includes('我 ') && (q.includes('什么') || q.includes('怎么样'))) {
      return 'persona';
    }
    
    // 关系查询关键词
    if (q.includes('关系') || q.includes('关联') || q.includes('和 ') && q.includes('什么')) {
      return 'relational';
    }
    
    // 默认：事实查询
    return 'factual';
  }

  /**
   * 流程查询
   */
  private async searchProcedural(query: string, limit: number): Promise<Memory[]> {
    // 从 MEMORY.md 的程序记忆章节检索
    if (!fs.existsSync(this.memoryFile)) {
      return [];
    }

    const content = fs.readFileSync(this.memoryFile, 'utf-8');
    const sectionStart = content.indexOf('## 程序记忆');
    
    if (sectionStart === -1) {
      return [];
    }

    const sectionEnd = content.indexOf('\n## ', sectionStart + 1);
    const section = content.substring(sectionStart, sectionEnd === -1 ? undefined : sectionEnd);

    // 简单关键词匹配（TODO: 实现向量检索）
    const memories = this.extractMemoriesFromSection(section, '程序');
    return this.rankByRelevance(memories, query).slice(0, limit);
  }

  /**
   * 时间查询
   */
  private async searchTemporal(query: string, limit: number, timeRange?: { start?: string; end?: string }): Promise<Memory[]> {
    const memories: Memory[] = [];
    
    // 解析时间关键词
    const { start, end } = this.parseTimeRange(query, timeRange);
    
    // 检索指定日期范围内的文件
    const files = glob.sync(path.join(this.memoryDir, '*.md'));
    
    for (const file of files) {
      const fileName = path.basename(file);
      const dateMatch = fileName.match(/(\d{4}-\d{2}-\d{2})\.md/);
      
      if (!dateMatch) continue;
      
      const fileDate = dateMatch[1];
      
      // 检查是否在时间范围内
      if (start && fileDate < start) continue;
      if (end && fileDate > end) continue;
      
      // 读取文件内容
      const content = fs.readFileSync(file, 'utf-8');
      const extracted = this.extractMemoriesFromFile(file, content);
      memories.push(...extracted);
    }

    // 按时间倒序排列
    memories.sort((a, b) => b.timestamp - a.timestamp);
    
    return memories.slice(0, limit);
  }

  /**
   * 关系查询
   */
  private async searchRelational(query: string, limit: number): Promise<Memory[]> {
    // TODO: 实现知识图谱检索
    // 目前返回所有相关记忆
    return this.searchFactual(query, limit);
  }

  /**
   * 偏好查询
   */
  private async searchPersona(query: string, limit: number): Promise<Memory[]> {
    if (!fs.existsSync(this.memoryFile)) {
      return [];
    }

    const content = fs.readFileSync(this.memoryFile, 'utf-8');
    const sectionStart = content.indexOf('## 人设记忆');
    
    if (sectionStart === -1) {
      return [];
    }

    const sectionEnd = content.indexOf('\n## ', sectionStart + 1);
    const section = content.substring(sectionStart, sectionEnd === -1 ? undefined : sectionEnd);

    const memories = this.extractMemoriesFromSection(section, '人设');
    return this.rankByRelevance(memories, query).slice(0, limit);
  }

  /**
   * 事实查询
   */
  private async searchFactual(query: string, limit: number): Promise<Memory[]> {
    const memories: Memory[] = [];
    
    // 搜索所有记忆文件
    const files = glob.sync(path.join(this.memoryDir, '*.md'));
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      const extracted = this.extractMemoriesFromFile(file, content);
      
      // 简单关键词匹配
      const matched = extracted.filter(m => 
        m.content.toLowerCase().includes(query.toLowerCase())
      );
      
      memories.push(...matched);
    }

    // 按相关性排序
    return this.rankByRelevance(memories, query).slice(0, limit);
  }

  /**
   * 从章节提取记忆
   */
  private extractMemoriesFromSection(section: string, type: string): Memory[] {
    const memories: Memory[] = [];
    const lines = section.split('\n');
    
    let currentMemory: Partial<Memory> = {};
    
    for (const line of lines) {
      if (line.startsWith('### ')) {
        // 新记忆开始
        if (currentMemory.id) {
          memories.push(currentMemory as Memory);
        }
        currentMemory = {
          type,
          timestamp: this.parseTimestamp(line.replace('### ', '')),
        };
      } else if (line.startsWith('**ID**:')) {
        currentMemory.id = line.replace('**ID**:', '').trim();
      } else if (line.trim() && !line.startsWith('**ID**')) {
        currentMemory.content = (currentMemory.content || '') + line + '\n';
      }
    }
    
    // 添加最后一个记忆
    if (currentMemory.id) {
      memories.push(currentMemory as Memory);
    }
    
    return memories;
  }

  /**
   * 从文件提取记忆
   */
  private extractMemoriesFromFile(filePath: string, content: string): Memory[] {
    const memories: Memory[] = [];
    const lines = content.split('\n');
    
    let currentMemory: Partial<Memory> = {};
    
    for (const line of lines) {
      if (line.startsWith('## ')) {
        // 新记忆开始
        if (currentMemory.id) {
          currentMemory.path = filePath;
          memories.push(currentMemory as Memory);
        }
        currentMemory = {
          type: '情景',
          timestamp: this.parseTimestamp(line.replace('## ', '')),
        };
      } else if (line.startsWith('**ID**:')) {
        currentMemory.id = line.replace('**ID**:', '').trim();
      } else if (line.trim() && !line.startsWith('**ID**')) {
        currentMemory.content = (currentMemory.content || '') + line + '\n';
      }
    }
    
    // 添加最后一个记忆
    if (currentMemory.id) {
      currentMemory.path = filePath;
      memories.push(currentMemory as Memory);
    }
    
    return memories;
  }

  /**
   * 按相关性排序
   */
  private rankByRelevance(memories: Memory[], query: string): Memory[] {
    // 简单实现：按关键词匹配度排序
    // TODO: 实现向量检索
    return memories.sort((a, b) => {
      const aScore = this.calculateRelevance(a.content, query);
      const bScore = this.calculateRelevance(b.content, query);
      return bScore - aScore;
    });
  }

  /**
   * 计算相关性分数
   */
  private calculateRelevance(content: string, query: string): number {
    const q = query.toLowerCase();
    const c = content.toLowerCase();
    
    let score = 0;
    
    // 完全匹配
    if (c.includes(q)) {
      score += 10;
    }
    
    // 关键词匹配
    const keywords = q.split(/\s+/);
    for (const keyword of keywords) {
      if (c.includes(keyword)) {
        score += 1;
      }
    }
    
    return score;
  }

  /**
   * 解析时间范围
   */
  private parseTimeRange(query: string, timeRange?: { start?: string; end?: string }): { start: string; end: string } {
    const today = new Date();
    const start = timeRange?.start || this.getDateString(today);
    const end = timeRange?.end || this.getDateString(today);
    
    // 解析时间关键词
    if (query.includes('昨天')) {
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);
      return {
        start: this.getDateString(yesterday),
        end: this.getDateString(yesterday),
      };
    }
    
    if (query.includes('今天')) {
      return {
        start: this.getDateString(today),
        end: this.getDateString(today),
      };
    }
    
    return { start, end };
  }

  /**
   * 解析时间戳
   */
  private parseTimestamp(timeStr: string): number {
    const match = timeStr.match(/(\d{4}-\d{2}-\d{2})/);
    if (match) {
      return new Date(match[1]).getTime();
    }
    return Date.now();
  }

  /**
   * 获取日期字符串
   */
  private getDateString(date: Date): string {
    return date.toISOString().split('T')[0];
  }
}

// 导出
export default MemoryRetriever;
