/**
 * Memory Retriever v4.1 - 增强版记忆检索
 * 
 * 基于 Generative Agents + Mem0 + MemoryBank 最佳实践
 * 
 * 新增功能：
 * - 重要性评分（近因 + 重要性 + 相关性）
 * - 情感维度（情感类型 + 情感强度）
 * - 动态 Top-K 优化
 * - 混合检索（语义 + 关键词 + 时间）
 * 
 * @author 小鬼 👻 + Jake
 * @version 4.1.0
 */

import * as fs from 'fs';
import * as path from 'path';

/**
 * 情感类型
 */
export type EmotionType = 
  | 'positive'    // 正面
  | 'negative'    // 负面
  | 'neutral'     // 中性
  | 'joy'         // 喜悦
  | 'sadness'     // 悲伤
  | 'anger'       // 愤怒
  | 'surprise'    // 惊讶
  | 'fear'        // 恐惧
  | 'disgust';    // 厌恶

/**
 * 记忆项（增强版）
 */
export interface MemoryItem {
  id: string;
  content: string;
  type: '情景' | '语义' | '程序' | '人设';
  timestamp: number;
  metadata?: {
    topic?: string;
    project?: string;
    emotion?: EmotionType;
    emotionIntensity?: number;  // 1-5
    importance?: number;        // 1-5
    tags?: string[];
  };
  // 检索评分
  recencyScore?: number;        // 近因评分
  importanceScore?: number;     // 重要性评分
  relevanceScore?: number;      // 相关性评分
  combinedScore?: number;       // 综合评分
}

/**
 * 检索选项（增强版）
 */
export interface RetrieveOptions {
  // 基础选项
  type?: 'procedural' | 'temporal' | 'relational' | 'persona' | 'factual';
  limit?: number;               // 返回数量限制
  
  // 评分权重（参考 Generative Agents）
  recencyWeight?: number;       // 近因权重（默认 0.3）
  importanceWeight?: number;    // 重要性权重（默认 0.5）
  relevanceWeight?: number;     // 相关性权重（默认 0.2）
  
  // 情感过滤（参考 MemoryBank）
  emotion?: EmotionType;
  minEmotionIntensity?: number; // 最小情感强度
  
  // Top-K 优化（参考 Mem0）
  dynamicK?: boolean;           // 动态 K 值（默认 false）
  minK?: number;                // 最小 K 值（默认 3）
  maxK?: number;                // 最大 K 值（默认 10）
  
  // 时间范围
  startTime?: number;
  endTime?: number;
  
  // 混合检索
  hybridSearch?: boolean;       // 启用混合检索（默认 false）
  keywordBoost?: number;        // 关键词提升倍数（默认 1.5）
}

/**
 * 检索结果（增强版）
 */
export interface RetrieveResult {
  memories: MemoryItem[];
  total: number;
  query?: string;
  searchType?: string;
  scores?: {
    avgRecency: number;
    avgImportance: number;
    avgRelevance: number;
  };
  emotions?: {
    positive: number;
    negative: number;
    neutral: number;
  };
}

/**
 * 增强版记忆检索器
 */
export class MemoryRetrieverV41 {
  private memoryDir: string;
  private indexCache: Map<string, MemoryItem[]> = new Map();

  constructor(memoryDir: string = 'memory') {
    this.memoryDir = memoryDir;
  }

  /**
   * 检索记忆（增强版）
   */
  async retrieve(
    query: string,
    options: RetrieveOptions = {}
  ): Promise<RetrieveResult> {
    const {
      type = 'factual',
      limit = 5,
      recencyWeight = 0.3,
      importanceWeight = 0.5,
      relevanceWeight = 0.2,
      emotion,
      minEmotionIntensity,
      dynamicK = false,
      minK = 3,
      maxK = 10,
      startTime,
      endTime,
      hybridSearch = false,
      keywordBoost = 1.5,
    } = options;

    // 1. 加载记忆
    const memories = await this.loadMemories();

    // 2. 过滤（时间/情感/类型）
    let filtered = this.filterMemories(memories, {
      type,
      startTime,
      endTime,
      emotion,
      minEmotionIntensity,
    });

    // 3. 计算评分
    const scored = this.calculateScores(filtered, query, {
      recencyWeight,
      importanceWeight,
      relevanceWeight,
      hybridSearch,
      keywordBoost,
    });

    // 4. 排序
    scored.sort((a, b) => (b.combinedScore || 0) - (a.combinedScore || 0));

    // 5. 动态 Top-K（参考 Mem0）
    const finalLimit = dynamicK 
      ? this.calculateDynamicK(scored, minK, maxK)
      : limit;

    const topMemories = scored.slice(0, finalLimit);

    // 6. 统计信息
    const stats = this.calculateStats(topMemories);

    return {
      memories: topMemories,
      total: filtered.length,
      query,
      searchType: type,
      scores: stats.scores,
      emotions: stats.emotions,
    };
  }

  /**
   * 加载记忆
   */
  private async loadMemories(): Promise<MemoryItem[]> {
    // 检查缓存
    if (this.indexCache.has('all')) {
      return this.indexCache.get('all')!;
    }

    const memories: MemoryItem[] = [];
    const memoryDir = path.join(process.cwd(), this.memoryDir);

    // 加载 MEMORY.md
    const memoryFile = path.join(memoryDir, 'MEMORY.md');
    if (fs.existsSync(memoryFile)) {
      const content = fs.readFileSync(memoryFile, 'utf-8');
      const parsed = this.parseMemoryMd(content);
      memories.push(...parsed);
    }

    // 加载 daily memory
    const dailyDir = path.join(memoryDir, 'daily');
    if (fs.existsSync(dailyDir)) {
      const files = fs.readdirSync(dailyDir).filter(f => f.endsWith('.md'));
      for (const file of files) {
        const filePath = path.join(dailyDir, file);
        const content = fs.readFileSync(filePath, 'utf-8');
        const parsed = this.parseDailyMemory(content, file);
        memories.push(...parsed);
      }
    }

    // 加载 wiki memory（v4.1 新增）
    const wikiDir = path.join(memoryDir, 'wiki');
    if (fs.existsSync(wikiDir)) {
      const files = fs.readdirSync(wikiDir).filter(f => f.endsWith('.md'));
      for (const file of files) {
        const filePath = path.join(wikiDir, file);
        const content = fs.readFileSync(filePath, 'utf-8');
        const parsed = this.parseWikiMemory(content, file);
        memories.push(...parsed);
      }
    }

    // 缓存
    this.indexCache.set('all', memories);

    return memories;
  }

  /**
   * 过滤记忆
   */
  private filterMemories(
    memories: MemoryItem[],
    filters: {
      type?: string;
      startTime?: number;
      endTime?: number;
      emotion?: EmotionType;
      minEmotionIntensity?: number;
    }
  ): MemoryItem[] {
    return memories.filter(memory => {
      // 时间过滤
      if (filters.startTime && memory.timestamp < filters.startTime) {
        return false;
      }
      if (filters.endTime && memory.timestamp > filters.endTime) {
        return false;
      }

      // 情感过滤（v4.1 新增）
      if (filters.emotion && memory.metadata?.emotion !== filters.emotion) {
        return false;
      }
      if (filters.minEmotionIntensity && 
          (memory.metadata?.emotionIntensity || 0) < filters.minEmotionIntensity) {
        return false;
      }

      return true;
    });
  }

  /**
   * 计算评分（参考 Generative Agents）
   */
  private calculateScores(
    memories: MemoryItem[],
    query: string,
    options: {
      recencyWeight: number;
      importanceWeight: number;
      relevanceWeight: number;
      hybridSearch: boolean;
      keywordBoost: number;
    }
  ): MemoryItem[] {
    const now = Date.now();
    const oneDay = 24 * 60 * 60 * 1000;
    const oneWeek = 7 * oneDay;
    const oneMonth = 30 * oneDay;

    return memories.map(memory => {
      // 1. 近因评分（Recency）- 指数衰减
      const age = now - memory.timestamp;
      let recencyScore: number;
      
      if (age < oneDay) {
        recencyScore = 1.0;
      } else if (age < oneWeek) {
        recencyScore = 0.8;
      } else if (age < oneMonth) {
        recencyScore = 0.5;
      } else {
        recencyScore = 0.3;
      }

      // 2. 重要性评分（Importance）
      const importanceScore = memory.metadata?.importance || 3;

      // 3. 相关性评分（Relevance）- 简单关键词匹配
      let relevanceScore = 0;
      const queryWords = query.toLowerCase().split(/\s+/);
      const content = memory.content.toLowerCase();
      
      for (const word of queryWords) {
        if (word.length > 2 && content.includes(word)) {
          relevanceScore += 1;
        }
      }
      relevanceScore = Math.min(relevanceScore / queryWords.length, 1.0);

      // 混合检索增强（v4.1 新增）
      if (options.hybridSearch && relevanceScore > 0) {
        relevanceScore *= options.keywordBoost;
      }

      // 4. 综合评分
      const combinedScore = 
        recencyScore * options.recencyWeight +
        (importanceScore / 5) * options.importanceWeight +
        relevanceScore * options.relevanceWeight;

      return {
        ...memory,
        recencyScore,
        importanceScore,
        relevanceScore,
        combinedScore,
      };
    });
  }

  /**
   * 动态 Top-K（参考 Mem0）
   */
  private calculateDynamicK(
    memories: MemoryItem[],
    minK: number,
    maxK: number
  ): number {
    if (memories.length === 0) {
      return minK;
    }

    // 计算评分分布
    const scores = memories.map(m => m.combinedScore || 0);
    const maxScore = Math.max(...scores);
    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;

    // 动态调整 K 值
    // 如果最高分远高于平均分，说明有明确答案，返回较少结果
    // 如果分数分布均匀，说明需要更多上下文，返回较多结果
    const ratio = maxScore / (avgScore || 0.1);
    
    if (ratio > 2) {
      // 明确答案
      return Math.max(minK, Math.floor(maxK * 0.3));
    } else if (ratio > 1.5) {
      // 中等明确
      return Math.max(minK, Math.floor(maxK * 0.5));
    } else {
      // 需要更多上下文
      return maxK;
    }
  }

  /**
   * 计算统计信息
   */
  private calculateStats(memories: MemoryItem[]) {
    const scores = {
      avgRecency: 0,
      avgImportance: 0,
      avgRelevance: 0,
    };

    const emotions = {
      positive: 0,
      negative: 0,
      neutral: 0,
    };

    if (memories.length === 0) {
      return { scores, emotions };
    }

    // 计算平均评分
    scores.avgRecency = memories.reduce((sum, m) => sum + (m.recencyScore || 0), 0) / memories.length;
    scores.avgImportance = memories.reduce((sum, m) => sum + (m.importanceScore || 0), 0) / memories.length;
    scores.avgRelevance = memories.reduce((sum, m) => sum + (m.relevanceScore || 0), 0) / memories.length;

    // 统计情感分布（v4.1 新增）
    for (const memory of memories) {
      const emotion = memory.metadata?.emotion;
      if (emotion) {
        if (['positive', 'joy', 'surprise'].includes(emotion)) {
          emotions.positive++;
        } else if (['negative', 'sadness', 'anger', 'fear', 'disgust'].includes(emotion)) {
          emotions.negative++;
        } else {
          emotions.neutral++;
        }
      }
    }

    return { scores, emotions };
  }

  /**
   * 解析 MEMORY.md
   */
  private parseMemoryMd(content: string): MemoryItem[] {
    const memories: MemoryItem[] = [];
    const sections = content.split(/^(## |### )/gm);

    let currentSection = '';
    let currentId = '';
    let currentContent = '';

    for (const section of sections) {
      if (section.startsWith('## ') || section.startsWith('### ')) {
        // 保存上一个记忆
        if (currentId && currentContent) {
          memories.push({
            id: currentId,
            content: currentContent.trim(),
            type: '语义',
            timestamp: Date.now(),
            metadata: {
              importance: 4,
            },
          });
        }

        currentSection = section.trim();
        currentId = this.extractId(section);
        currentContent = '';
      } else {
        currentContent += section;
      }
    }

    // 保存最后一个记忆
    if (currentId && currentContent) {
      memories.push({
        id: currentId,
        content: currentContent.trim(),
        type: '语义',
        timestamp: Date.now(),
        metadata: {
          importance: 4,
        },
      });
    }

    return memories;
  }

  /**
   * 解析每日记忆
   */
  private parseDailyMemory(content: string, filename: string): MemoryItem[] {
    const memories: MemoryItem[] = [];
    const date = filename.replace('.md', '');
    const timestamp = new Date(date).getTime();

    const lines = content.split('\n');
    let currentId = '';
    let currentContent = '';

    for (const line of lines) {
      if (line.startsWith('**ID**:')) {
        // 保存上一个记忆
        if (currentId && currentContent) {
          memories.push({
            id: currentId,
            content: currentContent.trim(),
            type: '情景',
            timestamp,
            metadata: {
              importance: 3,
            },
          });
        }

        currentId = line.replace('**ID**:', '').trim();
        currentContent = '';
      } else if (currentId) {
        currentContent += line + '\n';
      }
    }

    // 保存最后一个记忆
    if (currentId && currentContent) {
      memories.push({
        id: currentId,
        content: currentContent.trim(),
        type: '情景',
        timestamp,
        metadata: {
          importance: 3,
        },
      });
    }

    return memories;
  }

  /**
   * 解析 Wiki 记忆（v4.1 新增）
   */
  private parseWikiMemory(content: string, filename: string): MemoryItem[] {
    const memories: MemoryItem[] = [];
    const type = filename.replace('.md', '') as any;

    const sections = content.split(/^## /gm);

    for (const section of sections) {
      if (section.trim()) {
        const lines = section.split('\n');
        const title = lines[0].trim();
        const content = lines.slice(1).join('\n').trim();

        if (content) {
          memories.push({
            id: `wiki_${type}_${title}`,
            content: `${title}: ${content}`,
            type: '语义',
            timestamp: Date.now(),
            metadata: {
              importance: 4,
              tags: [type],
            },
          });
        }
      }
    }

    return memories;
  }

  /**
   * 提取 ID
   */
  private extractId(text: string): string {
    const match = text.match(/\*\*ID\*\*:\s*(\S+)/);
    return match ? match[1] : `mem_${Date.now()}`;
  }

  /**
   * 检测情感（v4.1 新增，简单实现）
   */
  detectEmotion(content: string): { emotion: EmotionType; intensity: number } {
    const positiveWords = ['好', '棒', '优秀', '成功', '开心', '高兴', '喜欢', '爱', '满意', '完美'];
    const negativeWords = ['坏', '差', '失败', '难过', '生气', '讨厌', '恨', '失望', '糟糕', '错误'];
    
    const contentLower = content.toLowerCase();
    let positiveCount = 0;
    let negativeCount = 0;

    for (const word of positiveWords) {
      if (contentLower.includes(word)) {
        positiveCount++;
      }
    }

    for (const word of negativeWords) {
      if (contentLower.includes(word)) {
        negativeCount++;
      }
    }

    const total = positiveCount + negativeCount;
    
    if (total === 0) {
      return { emotion: 'neutral', intensity: 1 };
    }

    const intensity = Math.min(5, Math.ceil(total / 3));

    if (positiveCount > negativeCount) {
      return { emotion: 'positive', intensity };
    } else if (negativeCount > positiveCount) {
      return { emotion: 'negative', intensity };
    } else {
      return { emotion: 'neutral', intensity };
    }
  }

  /**
   * 清除缓存
   */
  clearCache(): void {
    this.indexCache.clear();
  }
}
