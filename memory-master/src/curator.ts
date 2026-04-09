/**
 * Memory Curator - 记忆整理员
 * 
 * 基于 LLM Wiki 理念 + OS 级 4 层架构
 * 主动整理原始记忆 → 结构化知识
 * 
 * 功能：
 * 1. 定期从 raw/ 读取每日记忆
 * 2. 提炼核心洞察、决策、待办
 * 3. 写入 wiki/ 结构化知识
 * 4. 更新 MEMORY.md 长期记忆
 * 5. 建立记忆关联图谱
 * 6. 清理过期记忆
 */

import * as fs from 'fs';
import * as path from 'path';

// 简单的 ChatCompletion 封装（避免循环依赖）
interface ChatCompletionOptions {
  temperature?: number;
  maxTokens?: number;
}

class SimpleChat {
  async complete(prompt: string, options: ChatCompletionOptions = {}): Promise<string> {
    // 这里使用 OpenClaw 的 sessions_send 或者直接调用 API
    // 简化版本：返回空响应，实际使用需要集成 OpenClaw
    console.log('[SimpleChat] Prompt:', prompt.slice(0, 100) + '...');
    return '{}'; // 占位符，实际需要调用 AI API
  }
}

// ============================================================================
// 类型定义
// ============================================================================

export interface CuratorConfig {
  workspaceRoot: string;
  memoryDir: string;
  rawDir: string;
  wikiDir: string;
  memoryFile: string;
  autoCompact: boolean;
  compactThreshold: number; // 文件数量阈值
  retentionDays: number; // 保留天数
}

export interface MemoryItem {
  date: string;
  content: string;
  type: 'task' | 'decision' | 'insight' | 'context' | 'preference';
  importance: number; // 1-5
  tags: string[];
  relatedTo?: string[]; // 关联的记忆 ID
}

export interface CuratedKnowledge {
  projects: ProjectInfo[];
  people: PersonInfo[];
  decisions: DecisionInfo[];
  tasks: TaskInfo[];
  insights: InsightInfo[];
  preferences: PreferenceInfo[];
}

export interface ProjectInfo {
  name: string;
  status: 'active' | 'paused' | 'completed';
  description: string;
  lastUpdated: string;
  relatedFiles?: string[];
}

export interface PersonInfo {
  name: string;
  role?: string;
  context: string;
  lastMentioned: string;
}

export interface DecisionInfo {
  id: string;
  date: string;
  context: string;
  decision: string;
  reasoning: string;
  alternatives?: string[];
}

export interface TaskInfo {
  id: string;
  title: string;
  status: 'pending' | 'in-progress' | 'completed' | 'cancelled';
  priority: 'high' | 'medium' | 'low';
  dueDate?: string;
  context: string;
}

export interface InsightInfo {
  id: string;
  date: string;
  category: string;
  insight: string;
  source?: string;
}

export interface PreferenceInfo {
  category: string;
  preference: string;
  context: string;
}

export interface CurationResult {
  processedFiles: number;
  extractedMemories: MemoryItem[];
  updatedKnowledge: CuratedKnowledge;
  updatedMemoryMd: boolean;
  cleanedFiles: number;
  duration: number;
}

// ============================================================================
// 记忆整理员类
// ============================================================================

export class MemoryCurator {
  private config: CuratorConfig;
  private chat: SimpleChat;

  constructor(config: Partial<CuratorConfig>) {
    this.config = {
      workspaceRoot: config.workspaceRoot || process.cwd(),
      memoryDir: config.memoryDir || 'memory',
      rawDir: config.rawDir || 'memory/raw',
      wikiDir: config.wikiDir || 'memory/wiki',
      memoryFile: config.memoryFile || 'MEMORY.md',
      autoCompact: config.autoCompact ?? true,
      compactThreshold: config.compactThreshold ?? 30,
      retentionDays: config.retentionDays ?? 90,
    };

    this.chat = new SimpleChat();
  }

  // ============================================================================
  // 主入口：执行整理
  // ============================================================================

  /**
   * 执行完整整理流程
   */
  async curate(): Promise<CurationResult> {
    const startTime = Date.now();

    console.log('🔍 [Curator] 开始整理记忆...');

    // 1. 确保目录存在
    this.ensureDirectories();

    // 2. 读取 raw/ 下的所有每日记忆
    const rawMemories = this.readRawMemories();
    console.log(`📄 [Curator] 读取到 ${rawMemories.length} 个原始记忆文件`);

    // 3. 提炼结构化知识
    const knowledge = await this.extractKnowledge(rawMemories);
    console.log(`🧠 [Curator] 提炼出 ${this.countKnowledgeItems(knowledge)} 条知识`);

    // 4. 写入 wiki/ 结构化存储
    this.writeWiki(knowledge);
    console.log('📝 [Curator] 写入 wiki 完成');

    // 5. 更新 MEMORY.md
    const updatedMemoryMd = await this.updateMemoryMd(knowledge);
    console.log(`💾 [Curator] MEMORY.md 更新：${updatedMemoryMd ? '成功' : '跳过'}`);

    // 6. 清理过期文件
    const cleanedCount = this.cleanOldMemories();
    console.log(`🧹 [Curator] 清理 ${cleanedCount} 个过期文件`);

    const duration = Date.now() - startTime;

    return {
      processedFiles: rawMemories.length,
      extractedMemories: this.flattenKnowledge(knowledge),
      updatedKnowledge: knowledge,
      updatedMemoryMd,
      cleanedFiles: cleanedCount,
      duration,
    };
  }

  // ============================================================================
  // 目录管理
  // ============================================================================

  private ensureDirectories(): void {
    const dirs = [
      path.join(this.config.workspaceRoot, this.config.rawDir),
      path.join(this.config.workspaceRoot, this.config.wikiDir),
    ];

    for (const dir of dirs) {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log(`📁 [Curator] 创建目录：${dir}`);
      }
    }
  }

  // ============================================================================
  // 读取原始记忆
  // ============================================================================

  private readRawMemories(): Array<{ file: string; content: string; date: string }> {
    const rawDir = path.join(this.config.workspaceRoot, this.config.rawDir);
    const memories: Array<{ file: string; content: string; date: string }> = [];

    if (!fs.existsSync(rawDir)) {
      return memories;
    }

    const files = fs.readdirSync(rawDir)
      .filter(f => f.endsWith('.md'))
      .sort(); // 按日期排序

    for (const file of files) {
      const filePath = path.join(rawDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      const date = file.replace('.md', '');

      memories.push({ file, content, date });
    }

    return memories;
  }

  // ============================================================================
  // 知识提炼（核心 AI 能力）
  // ============================================================================

  private async extractKnowledge(
    memories: Array<{ file: string; content: string; date: string }>
  ): Promise<CuratedKnowledge> {
    if (memories.length === 0) {
      return this.emptyKnowledge();
    }

    // 合并所有记忆内容
    const combinedContent = memories
      .map(m => `## ${m.date}\n\n${m.content}`)
      .join('\n\n---\n\n');

    // 使用 AI 提炼知识
    const prompt = this.buildExtractionPrompt(combinedContent);
    const response = await this.chat.complete(prompt, {
      temperature: 0.3,
      maxTokens: 4000,
    });

    // 解析 JSON 响应
    try {
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]) as CuratedKnowledge;
      }
    } catch (e) {
      console.warn('⚠️ [Curator] JSON 解析失败，使用空知识');
    }

    return this.emptyKnowledge();
  }

  private buildExtractionPrompt(content: string): string {
    return `你是一个专业的记忆整理员。请从以下原始对话记忆中提取结构化知识。

## 原始记忆内容

${content.slice(0, 15000)} ${content.length > 15000 ? '...(截断)' : ''}

## 提取要求

请提取以下 6 类知识：

1. **Projects（项目）**：用户正在进行的项目、任务、目标
2. **People（人物）**：提到的人名、角色、关系
3. **Decisions（决策）**：用户做出的重要决定、选择
4. **Tasks（待办）**：待办事项、计划、承诺
5. **Insights（洞察）**：学到的东西、经验教训、新理解
6. **Preferences（偏好）**：用户的喜好、习惯、风格

## 输出格式

必须输出严格的 JSON 格式：

\`\`\`json
{
  "projects": [
    {
      "name": "项目名称",
      "status": "active|paused|completed",
      "description": "项目描述",
      "lastUpdated": "YYYY-MM-DD",
      "relatedFiles": ["文件路径（可选）"]
    }
  ],
  "people": [
    {
      "name": "人名",
      "role": "角色（可选）",
      "context": "相关上下文",
      "lastMentioned": "YYYY-MM-DD"
    }
  ],
  "decisions": [
    {
      "id": "dec_001",
      "date": "YYYY-MM-DD",
      "context": "决策背景",
      "decision": "决策内容",
      "reasoning": "决策理由",
      "alternatives": ["其他选项（可选）"]
    }
  ],
  "tasks": [
    {
      "id": "task_001",
      "title": "任务标题",
      "status": "pending|in-progress|completed|cancelled",
      "priority": "high|medium|low",
      "dueDate": "YYYY-MM-DD（可选）",
      "context": "任务上下文"
    }
  ],
  "insights": [
    {
      "id": "ins_001",
      "date": "YYYY-MM-DD",
      "category": "分类",
      "insight": "洞察内容",
      "source": "来源（可选）"
    }
  ],
  "preferences": [
    {
      "category": "分类",
      "preference": "偏好内容",
      "context": "上下文"
    }
  ]
}
\`\`\`

## 注意事项

- 只提取真正重要的信息，不要提取琐碎内容
- 保持简洁，每条知识 1-2 句话
- 日期格式：YYYY-MM-DD
- 如果某类没有内容，返回空数组 []

现在请提取知识：`;
  }

  private emptyKnowledge(): CuratedKnowledge {
    return {
      projects: [],
      people: [],
      decisions: [],
      tasks: [],
      insights: [],
      preferences: [],
    };
  }

  private countKnowledgeItems(knowledge: CuratedKnowledge): number {
    return (
      knowledge.projects.length +
      knowledge.people.length +
      knowledge.decisions.length +
      knowledge.tasks.length +
      knowledge.insights.length +
      knowledge.preferences.length
    );
  }

  private flattenKnowledge(knowledge: CuratedKnowledge): MemoryItem[] {
    const items: MemoryItem[] = [];
    const today = new Date().toISOString().split('T')[0];

    for (const project of knowledge.projects) {
      items.push({
        date: project.lastUpdated,
        type: 'context',
        content: `项目：${project.name} - ${project.description}`,
        importance: project.status === 'active' ? 4 : 3,
        tags: ['project', project.status],
      });
    }

    for (const person of knowledge.people) {
      items.push({
        date: person.lastMentioned,
        type: 'context',
        content: `人物：${person.name}${person.role ? ` (${person.role})` : ''} - ${person.context}`,
        importance: 3,
        tags: ['person', person.name],
      });
    }

    for (const decision of knowledge.decisions) {
      items.push({
        date: decision.date,
        type: 'decision',
        content: `决策：${decision.decision}`,
        importance: 5,
        tags: ['decision'],
      });
    }

    for (const task of knowledge.tasks) {
      items.push({
        date: today,
        type: 'task',
        content: `任务：${task.title}`,
        importance: task.priority === 'high' ? 5 : task.priority === 'medium' ? 3 : 2,
        tags: ['task', task.status, task.priority],
      });
    }

    for (const insight of knowledge.insights) {
      items.push({
        date: insight.date,
        type: 'insight',
        content: `洞察：${insight.insight}`,
        importance: 4,
        tags: ['insight', insight.category],
      });
    }

    for (const pref of knowledge.preferences) {
      items.push({
        date: today,
        type: 'preference',
        content: `偏好：${pref.category} - ${pref.preference}`,
        importance: 3,
        tags: ['preference', pref.category],
      });
    }

    return items;
  }

  // ============================================================================
  // 写入 Wiki
  // ============================================================================

  private writeWiki(knowledge: CuratedKnowledge): void {
    const wikiDir = path.join(this.config.workspaceRoot, this.config.wikiDir);

    // 写入项目索引
    if (knowledge.projects.length > 0) {
      const projectsMd = this.formatProjectsWiki(knowledge.projects);
      fs.writeFileSync(path.join(wikiDir, 'projects.md'), projectsMd);
    }

    // 写入人物索引
    if (knowledge.people.length > 0) {
      const peopleMd = this.formatPeopleWiki(knowledge.people);
      fs.writeFileSync(path.join(wikiDir, 'people.md'), peopleMd);
    }

    // 写入决策日志
    if (knowledge.decisions.length > 0) {
      const decisionsMd = this.formatDecisionsWiki(knowledge.decisions);
      fs.writeFileSync(path.join(wikiDir, 'decisions.md'), decisionsMd);
    }

    // 写入任务看板
    const tasksMd = this.formatTasksWiki(knowledge.tasks);
    fs.writeFileSync(path.join(wikiDir, 'tasks.md'), tasksMd);

    // 写入洞察集合
    if (knowledge.insights.length > 0) {
      const insightsMd = this.formatInsightsWiki(knowledge.insights);
      fs.writeFileSync(path.join(wikiDir, 'insights.md'), insightsMd);
    }

    // 写入偏好设置
    if (knowledge.preferences.length > 0) {
      const preferencesMd = this.formatPreferencesWiki(knowledge.preferences);
      fs.writeFileSync(path.join(wikiDir, 'preferences.md'), preferencesMd);
    }
  }

  private formatProjectsWiki(projects: ProjectInfo[]): string {
    const today = new Date().toISOString().split('T')[0];
    let md = `# 项目索引\n\n*最后更新：${today}*\n\n`;

    const active = projects.filter(p => p.status === 'active');
    const paused = projects.filter(p => p.status === 'paused');
    const completed = projects.filter(p => p.status === 'completed');

    if (active.length > 0) {
      md += `## 🟢 进行中\n\n`;
      for (const p of active) {
        md += `### ${p.name}\n\n${p.description}\n\n`;
      }
    }

    if (paused.length > 0) {
      md += `## 🟡 已暂停\n\n`;
      for (const p of paused) {
        md += `### ${p.name}\n\n${p.description}\n\n`;
      }
    }

    if (completed.length > 0) {
      md += `## ✅ 已完成\n\n`;
      for (const p of completed) {
        md += `### ${p.name}\n\n${p.description}\n\n`;
      }
    }

    return md;
  }

  private formatPeopleWiki(people: PersonInfo[]): string {
    const today = new Date().toISOString().split('T')[0];
    let md = `# 人物索引\n\n*最后更新：${today}*\n\n`;

    for (const person of people) {
      md += `## ${person.name}`;
      if (person.role) md += ` (${person.role})`;
      md += `\n\n${person.context}\n\n`;
    }

    return md;
  }

  private formatDecisionsWiki(decisions: DecisionInfo[]): string {
    const today = new Date().toISOString().split('T')[0];
    let md = `# 决策日志\n\n*最后更新：${today}*\n\n`;

    for (const d of decisions) {
      md += `## ${d.date}: ${d.decision}\n\n`;
      md += `**背景**: ${d.context}\n\n`;
      md += `**理由**: ${d.reasoning}\n\n`;
      if (d.alternatives && d.alternatives.length > 0) {
        md += `**其他选项**: ${d.alternatives.join(', ')}\n\n`;
      }
      md += `---\n\n`;
    }

    return md;
  }

  private formatTasksWiki(tasks: TaskInfo[]): string {
    const today = new Date().toISOString().split('T')[0];
    let md = `# 任务看板\n\n*最后更新：${today}*\n\n`;

    const byStatus: Record<string, TaskInfo[]> = {};
    for (const task of tasks) {
      if (!byStatus[task.status]) byStatus[task.status] = [];
      byStatus[task.status].push(task);
    }

    const statusLabels: Record<string, string> = {
      'pending': '📋 待处理',
      'in-progress': '🔄 进行中',
      'completed': '✅ 已完成',
      'cancelled': '❌ 已取消',
    };

    for (const [status, label] of Object.entries(statusLabels)) {
      const statusTasks = byStatus[status] || [];
      if (statusTasks.length > 0) {
        md += `## ${label}\n\n`;
        for (const task of statusTasks) {
          const priorityIcon = task.priority === 'high' ? '🔴' : task.priority === 'medium' ? '🟡' : '🟢';
          md += `- ${priorityIcon} **${task.title}**`;
          if (task.dueDate) md += ` (截止：${task.dueDate})`;
          md += `\n  - ${task.context}\n`;
        }
        md += `\n`;
      }
    }

    return md;
  }

  private formatInsightsWiki(insights: InsightInfo[]): string {
    const today = new Date().toISOString().split('T')[0];
    let md = `# 洞察集合\n\n*最后更新：${today}*\n\n`;

    const byCategory: Record<string, InsightInfo[]> = {};
    for (const insight of insights) {
      if (!byCategory[insight.category]) byCategory[insight.category] = [];
      byCategory[insight.category].push(insight);
    }

    for (const [category, categoryInsights] of Object.entries(byCategory)) {
      md += `## ${category}\n\n`;
      for (const insight of categoryInsights) {
        md += `- ${insight.date}: ${insight.insight}\n`;
      }
      md += `\n`;
    }

    return md;
  }

  private formatPreferencesWiki(preferences: PreferenceInfo[]): string {
    const today = new Date().toISOString().split('T')[0];
    let md = `# 偏好设置\n\n*最后更新：${today}*\n\n`;

    const byCategory: Record<string, PreferenceInfo[]> = {};
    for (const pref of preferences) {
      if (!byCategory[pref.category]) byCategory[pref.category] = [];
      byCategory[pref.category].push(pref);
    }

    for (const [category, categoryPrefs] of Object.entries(byCategory)) {
      md += `## ${category}\n\n`;
      for (const pref of categoryPrefs) {
        md += `- ${pref.preference}\n`;
        if (pref.context) md += `  - ${pref.context}\n`;
      }
      md += `\n`;
    }

    return md;
  }

  // ============================================================================
  // 更新 MEMORY.md
  // ============================================================================

  private async updateMemoryMd(knowledge: CuratedKnowledge): Promise<boolean> {
    const memoryFilePath = path.join(this.config.workspaceRoot, this.config.memoryFile);

    if (!fs.existsSync(memoryFilePath)) {
      console.log('⚠️ [Curator] MEMORY.md 不存在，跳过更新');
      return false;
    }

    const existingContent = fs.readFileSync(memoryFilePath, 'utf-8');
    const today = new Date().toISOString().split('T')[0];

    // 构建更新内容
    const updateSection = this.buildMemoryUpdateSection(knowledge, today);

    // 查找"## 当前记忆"部分并更新
    const currentMemoryRegex = /(## 当前记忆\n\n)([\s\S]*?)(\n\n###|\n\n---|\n\*最后更新|$)/;
    const match = existingContent.match(currentMemoryRegex);

    let newContent: string;
    if (match) {
      // 替换现有内容
      newContent = existingContent.replace(
        currentMemoryRegex,
        `$1${updateSection}$3`
      );
    } else {
      // 在"## 当前记忆"后插入
      const insertMarker = '## 当前记忆';
      const insertIndex = existingContent.indexOf(insertMarker);
      if (insertIndex !== -1) {
        newContent = existingContent.slice(0, insertIndex + insertMarker.length) +
          '\n\n' + updateSection +
          existingContent.slice(insertIndex + insertMarker.length);
      } else {
        // 追加到末尾
        newContent = existingContent + '\n\n## 当前记忆\n\n' + updateSection;
      }
    }

    // 更新最后更新时间
    newContent = newContent.replace(
      /\*最后更新：[\d-]+\*/,
      `*最后更新：${today}*`
    );

    fs.writeFileSync(memoryFilePath, newContent, 'utf-8');
    return true;
  }

  private buildMemoryUpdateSection(knowledge: CuratedKnowledge, today: string): string {
    let section = `*最后更新：${today}*\n\n`;

    // 项目进展
    const activeProjects = knowledge.projects.filter(p => p.status === 'active');
    if (activeProjects.length > 0) {
      section += `### 项目进展\n\n`;
      for (const p of activeProjects) {
        section += `#### ${p.name}\n- 状态：进行中\n- 描述：${p.description}\n\n`;
      }
    }

    // 重要决策
    if (knowledge.decisions.length > 0) {
      section += `### 重要决策\n\n`;
      for (const d of knowledge.decisions.slice(0, 5)) {
        section += `- **${d.date}**: ${d.decision}\n`;
      }
      section += `\n`;
    }

    // 待办事项
    const pendingTasks = knowledge.tasks.filter(t => t.status === 'pending' || t.status === 'in-progress');
    if (pendingTasks.length > 0) {
      section += `### 待办事项\n\n`;
      for (const t of pendingTasks.slice(0, 10)) {
        const icon = t.status === 'in-progress' ? '🔄' : '📋';
        section += `${icon} ${t.title}`;
        if (t.priority === 'high') section += ' 🔴';
        section += `\n`;
      }
      section += `\n`;
    }

    // 新洞察
    if (knowledge.insights.length > 0) {
      section += `### 新洞察\n\n`;
      for (const i of knowledge.insights.slice(0, 5)) {
        section += `- ${i.insight}\n`;
      }
      section += `\n`;
    }

    return section;
  }

  // ============================================================================
  // 清理过期记忆
  // ============================================================================

  private cleanOldMemories(): number {
    const rawDir = path.join(this.config.workspaceRoot, this.config.rawDir);
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - this.config.retentionDays);

    if (!fs.existsSync(rawDir)) {
      return 0;
    }

    let cleaned = 0;
    const files = fs.readdirSync(rawDir).filter(f => f.endsWith('.md'));

    for (const file of files) {
      const dateStr = file.replace('.md', '');
      const fileDate = new Date(dateStr);

      if (fileDate < cutoffDate) {
        const filePath = path.join(rawDir, file);
        fs.unlinkSync(filePath);
        cleaned++;
        console.log(`🗑️ [Curator] 删除过期文件：${file}`);
      }
    }

    return cleaned;
  }
}

// ============================================================================
// CLI 入口
// ============================================================================

if (require.main === module) {
  const workspaceRoot = process.argv[2] || process.cwd();

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

  curator.curate()
    .then(result => {
      console.log('\n✅ 整理完成！');
      console.log(`   处理文件：${result.processedFiles}`);
      console.log(`   提取记忆：${result.extractedMemories.length}`);
      console.log(`   更新 MEMORY.md: ${result.updatedMemoryMd ? '是' : '否'}`);
      console.log(`   清理文件：${result.cleanedFiles}`);
      console.log(`   耗时：${(result.duration / 1000).toFixed(2)}秒`);
    })
    .catch(err => {
      console.error('❌ 整理失败:', err);
      process.exit(1);
    });
}
