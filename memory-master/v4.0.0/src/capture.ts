/**
 * Memory-Master 记忆捕捉模块
 * 
 * 基于 Karpathy 五环节之"原始数据输入"和"数据摄取与编译"
 * 基于 Anthropic Skill 设计原则
 */

import * as fs from 'fs';
import * as path from 'path';
import { FilterResult, filterSensitiveData } from './filter';

/**
 * 记忆类型
 */
export type MemoryType = '情景' | '语义' | '程序' | '人设';

/**
 * 记忆元数据
 */
export interface MemoryMetadata {
  source?: string;      // 来源（会话 ID）
  timestamp?: number;   // 时间戳
  topic?: string;       // 主题
  project?: string;     // 项目
  tags?: string[];      // 标签
}

/**
 * 捕捉选项
 */
export interface CaptureOptions {
  type?: MemoryType;
  metadata?: MemoryMetadata;
  skipFilter?: boolean;   // 跳过敏感数据过滤
}

/**
 * 捕捉结果
 */
export interface CaptureResult {
  success: boolean;
  id: string;             // 记忆 ID
  type: MemoryType;
  content: string;        // 原始内容
  filtered?: FilterResult; // 过滤结果
  path: string;           // 存储路径
  timestamp: number;
}

/**
 * 记忆捕捉器
 */
export class MemoryCapture {
  private memoryDir: string;
  private memoryFile: string;

  constructor(memoryDir: string = 'memory') {
    this.memoryDir = memoryDir;
    this.memoryFile = path.join(memoryDir, 'MEMORY.md');
    
    // 确保目录存在
    if (!fs.existsSync(memoryDir)) {
      fs.mkdirSync(memoryDir, { recursive: true });
    }
    
    // 确保 MEMORY.md 存在
    if (!fs.existsSync(this.memoryFile)) {
      this.initMemoryFile();
    }
  }

  /**
   * 初始化 MEMORY.md
   */
  private initMemoryFile(): void {
    const content = `# MEMORY.md - 长期记忆

这是 Memory-Master 的长期记忆文件，用于存储语义记忆、程序记忆和人设记忆。

---

## 语义记忆

_提炼的知识、概念_

---

## 程序记忆

_操作技能、流程_

---

## 人设记忆

_用户偏好、习惯_

---

*最后更新：${new Date().toISOString()}*
`;
    fs.writeFileSync(this.memoryFile, content, 'utf-8');
  }

  /**
   * 捕捉记忆
   */
  async capture(content: string, options: CaptureOptions = {}): Promise<CaptureResult> {
    const {
      type = '情景',
      metadata = {},
      skipFilter = false,
    } = options;

    // 1. 敏感数据过滤
    let filtered: FilterResult | undefined;
    let filteredContent = content;
    
    if (!skipFilter) {
      filtered = await filterSensitiveData(content);
      if (filtered.hasSensitive) {
        filteredContent = filtered.filtered;
      }
    }

    // 2. 生成记忆 ID
    const timestamp = metadata.timestamp || Date.now();
    const id = this.generateId(type, timestamp);

    // 3. 存储记忆
    const storePath = this.getStorePath(type, timestamp);
    this.storeMemory(storePath, id, type, filteredContent, metadata);

    // 4. 返回结果
    return {
      success: true,
      id,
      type,
      content: filteredContent,
      filtered,
      path: storePath,
      timestamp,
    };
  }

  /**
   * 生成记忆 ID
   */
  private generateId(type: MemoryType, timestamp: number): string {
    const date = new Date(timestamp);
    const dateStr = date.toISOString().split('T')[0].replace(/-/g, '');
    const random = Math.random().toString(36).substring(2, 6);
    return `mem-${dateStr}-${random}`;
  }

  /**
   * 获取存储路径
   */
  private getStorePath(type: MemoryType, timestamp: number): string {
    if (type === '情景') {
      // 情景记忆按日期存储
      const date = new Date(timestamp);
      const dateStr = date.toISOString().split('T')[0];
      return path.join(this.memoryDir, `${dateStr}.md`);
    } else {
      // 其他类型存储到 MEMORY.md
      return this.memoryFile;
    }
  }

  /**
   * 存储记忆
   */
  private storeMemory(
    filePath: string,
    id: string,
    type: MemoryType,
    content: string,
    metadata: MemoryMetadata
  ): void {
    const date = new Date(metadata.timestamp || Date.now());
    const timeStr = date.toISOString().replace('T', ' ').substring(0, 19);

    if (type === '情景') {
      // 情景记忆：按日期存储
      this.storeEpisodicMemory(filePath, id, content, metadata, timeStr);
    } else {
      // 其他类型：存储到 MEMORY.md
      this.storeSemanticMemory(filePath, id, type, content, metadata, timeStr);
    }
  }

  /**
   * 存储情景记忆
   */
  private storeEpisodicMemory(
    filePath: string,
    id: string,
    content: string,
    metadata: MemoryMetadata,
    timeStr: string
  ): void {
    let fileContent = '';
    
    if (fs.existsSync(filePath)) {
      fileContent = fs.readFileSync(filePath, 'utf-8');
    } else {
      // 创建新文件
      const date = filePath.split('/').pop()?.replace('.md', '') || '';
      fileContent = `# ${date} 日记\n\n`;
    }

    // 添加新记忆
    const newMemory = `\n## ${timeStr}\n\n**ID**: ${id}\n${this.formatMetadata(metadata)}\n${content}\n`;
    
    fileContent += newMemory;
    fs.writeFileSync(filePath, fileContent, 'utf-8');
  }

  /**
   * 存储语义/程序/人设记忆
   */
  private storeSemanticMemory(
    filePath: string,
    id: string,
    type: MemoryType,
    content: string,
    metadata: MemoryMetadata,
    timeStr: string
  ): void {
    let fileContent = fs.readFileSync(filePath, 'utf-8');
    
    // 找到对应的章节
    const sectionMap: Record<MemoryType, string> = {
      '情景': '## 情景记忆',
      '语义': '## 语义记忆',
      '程序': '## 程序记忆',
      '人设': '## 人设记忆',
    };
    
    const section = sectionMap[type];
    const sectionIndex = fileContent.indexOf(section);
    
    if (sectionIndex === -1) {
      console.warn(`Section "${section}" not found in MEMORY.md`);
      return;
    }

    // 找到下一节的开始位置
    const nextSectionIndex = fileContent.indexOf('\n## ', sectionIndex + 1);
    const insertPos = nextSectionIndex === -1 ? fileContent.length : nextSectionIndex;

    // 插入新记忆
    const newMemory = `\n### ${timeStr}\n\n**ID**: ${id}\n${this.formatMetadata(metadata)}${content}\n`;
    
    fileContent = fileContent.slice(0, insertPos) + newMemory + fileContent.slice(insertPos);
    fs.writeFileSync(filePath, fileContent, 'utf-8');
  }

  /**
   * 格式化元数据
   */
  private formatMetadata(metadata: MemoryMetadata): string {
    const parts: string[] = [];
    
    if (metadata.source) parts.push(`来源：${metadata.source}`);
    if (metadata.topic) parts.push(`主题：${metadata.topic}`);
    if (metadata.project) parts.push(`项目：${metadata.project}`);
    if (metadata.tags && metadata.tags.length > 0) parts.push(`标签：${metadata.tags.join(', ')}`);
    
    return parts.length > 0 ? parts.join(' | ') + '\n' : '';
  }
}

// 导出
export default MemoryCapture;
