/**
 * Memory-Master 技能自进化模块
 * 
 * 基于 AutoSkill / SkillRL 论文
 * - 从错误中学习
 * - 技能蒸馏
 * - 经验驱动的终身学习
 */

import * as fs from 'fs';
import * as path from 'path';

/**
 * 技能条目
 */
export interface Skill {
  id: string;
  name: string;
  description: string;
  pattern: string;         // 触发模式
  action: string;          // 执行动作
  successCount: number;    // 成功次数
  failureCount: number;    // 失败次数
  lastUsed?: number;       // 最后使用时间
  createdAt: number;       // 创建时间
  updatedAt: number;       // 更新时间
}

/**
 * 经验记录
 */
export interface Experience {
  id: string;
  skillId?: string;        // 关联技能
  context: string;         // 上下文
  action: string;          // 执行的动作
  result: 'success' | 'failure';
  feedback?: string;       // 反馈
  timestamp: number;
  lessons?: string[];      // 学到的教训
}

/**
 * 技能进化配置
 */
export interface SkillEvolutionConfig {
  minSuccesses: number;    // 最小成功次数（用于蒸馏）
  minFailures: number;     // 最小失败次数（触发学习）
  retentionDays: number;   // 经验保留天数
}

/**
 * 默认配置
 */
const DEFAULT_CONFIG: SkillEvolutionConfig = {
  minSuccesses: 3,         // 3 次成功触发蒸馏
  minFailures: 2,          // 2 次失败触发学习
  retentionDays: 30,       // 保留 30 天经验
};

/**
 * 技能进化器
 */
export class SkillEvolver {
  private config: SkillEvolutionConfig;
  private skillsFile: string;
  private experiencesFile: string;

  constructor(memoryDir: string = 'memory', config?: Partial<SkillEvolutionConfig>) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.skillsFile = path.join(memoryDir, 'skills.json');
    this.experiencesFile = path.join(memoryDir, 'experiences.json');
    
    // 初始化文件
    this.initFiles();
  }

  /**
   * 初始化文件
   */
  private initFiles(): void {
    if (!fs.existsSync(this.skillsFile)) {
      fs.writeFileSync(this.skillsFile, JSON.stringify([], null, 2), 'utf-8');
    }
    
    if (!fs.existsSync(this.experiencesFile)) {
      fs.writeFileSync(this.experiencesFile, JSON.stringify([], null, 2), 'utf-8');
    }
  }

  /**
   * 记录经验
   */
  async recordExperience(
    context: string,
    action: string,
    result: 'success' | 'failure',
    feedback?: string,
    skillId?: string
  ): Promise<Experience> {
    const experiences = this.loadExperiences();
    
    const experience: Experience = {
      id: this.generateId(),
      skillId,
      context,
      action,
      result,
      feedback,
      timestamp: Date.now(),
    };
    
    // 从失败中学习
    if (result === 'failure') {
      experience.lessons = await this.learnFromFailure(experience);
      
      // 更新关联技能的失败计数
      if (skillId) {
        this.updateSkillStats(skillId, { failure: true });
      }
    } else {
      // 更新关联技能的成功计数
      if (skillId) {
        this.updateSkillStats(skillId, { success: true });
      }
    }
    
    experiences.push(experience);
    this.saveExperiences(experiences);
    
    return experience;
  }

  /**
   * 从失败中学习
   */
  private async learnFromFailure(experience: Experience): Promise<string[]> {
    const lessons: string[] = [];
    
    // 简单实现：提取关键错误信息
    // TODO: 使用 LLM 分析失败原因
    if (experience.feedback) {
      const errorPatterns = [
        { pattern: /超时|timeout/i, lesson: '增加超时时间或重试机制' },
        { pattern: /权限|permission/i, lesson: '检查权限配置' },
        { pattern: /格式|format/i, lesson: '验证输入格式' },
        { pattern: /不存在|not found/i, lesson: '添加存在性检查' },
      ];
      
      for (const { pattern, lesson } of errorPatterns) {
        if (pattern.test(experience.feedback)) {
          lessons.push(lesson);
        }
      }
    }
    
    // 如果没有检测到具体错误，添加通用教训
    if (lessons.length === 0) {
      lessons.push('记录详细错误日志以便后续分析');
    }
    
    return lessons;
  }

  /**
   * 技能蒸馏（从成功经验中提取）
   */
  async distillSkills(): Promise<Skill[]> {
    const experiences = this.loadExperiences();
    const skills = this.loadSkills();
    
    // 按动作分组成功经验
    const successByAction = new Map<string, Experience[]>();
    
    for (const exp of experiences) {
      if (exp.result === 'success') {
        const actionKey = exp.action;
        if (!successByAction.has(actionKey)) {
          successByAction.set(actionKey, []);
        }
        successByAction.get(actionKey)!.push(exp);
      }
    }
    
    const newSkills: Skill[] = [];
    
    // 为频繁成功的动作创建技能
    for (const [action, exps] of successByAction.entries()) {
      if (exps.length >= this.config.minSuccesses) {
        // 检查是否已存在相同技能的技能
        const existingSkill = skills.find(s => s.action === action);
        
        if (!existingSkill) {
          // 创建新技能
          const skill: Skill = {
            id: this.generateId(),
            name: `Skill-${action.substring(0, 20)}`,
            description: `从 ${exps.length} 次成功经验中蒸馏`,
            pattern: this.extractPattern(exps),
            action,
            successCount: exps.length,
            failureCount: 0,
            createdAt: Date.now(),
            updatedAt: Date.now(),
          };
          
          newSkills.push(skill);
        } else {
          // 更新现有技能
          existingSkill.successCount += exps.length;
          existingSkill.updatedAt = Date.now();
        }
      }
    }
    
    // 保存新技能
    if (newSkills.length > 0) {
      skills.push(...newSkills);
      this.saveSkills(skills);
    }
    
    return newSkills;
  }

  /**
   * 提取触发模式
   */
  private extractPattern(experiences: Experience[]): string {
    // 简单实现：提取共同上下文
    // TODO: 使用 LLM 提取通用模式
    const contexts = experiences.map(e => e.context);
    const commonWords = this.findCommonWords(contexts);
    return commonWords.join(' ') || '*';
  }

  /**
   * 查找共同词汇
   */
  private findCommonWords(texts: string[]): string[] {
    const wordCount = new Map<string, number>();
    
    for (const text of texts) {
      const words = text.split(/\s+/);
      const uniqueWords = new Set(words);
      
      for (const word of uniqueWords) {
        if (word.length > 2) { // 忽略短词
          wordCount.set(word, (wordCount.get(word) || 0) + 1);
        }
      }
    }
    
    // 返回出现频率高的词
    const threshold = Math.ceil(texts.length * 0.5);
    return Array.from(wordCount.entries())
      .filter(([_, count]) => count >= threshold)
      .map(([word]) => word);
  }

  /**
   * 更新技能统计
   */
  private updateSkillStats(
    skillId: string,
    stats: { success?: boolean; failure?: boolean }
  ): void {
    const skills = this.loadSkills();
    const skill = skills.find(s => s.id === skillId);
    
    if (skill) {
      if (stats.success) {
        skill.successCount++;
      }
      if (stats.failure) {
        skill.failureCount++;
      }
      skill.updatedAt = Date.now();
      
      this.saveSkills(skills);
    }
  }

  /**
   * 获取技能建议
   */
  getSkillSuggestions(context: string): Skill[] {
    const skills = this.loadSkills();
    
    // 简单匹配：检查上下文是否包含技能模式
    return skills.filter(skill => {
      if (skill.pattern === '*') return true;
      return context.toLowerCase().includes(skill.pattern.toLowerCase());
    }).sort((a, b) => {
      // 按成功率排序
      const aRate = a.successCount / (a.successCount + a.failureCount || 1);
      const bRate = b.successCount / (b.successCount + b.failureCount || 1);
      return bRate - aRate;
    });
  }

  /**
   * 清理旧经验
   */
  cleanupOldExperiences(): void {
    const experiences = this.loadExperiences();
    const cutoff = Date.now() - this.config.retentionDays * 24 * 60 * 60 * 1000;
    
    const filtered = experiences.filter(exp => exp.timestamp > cutoff);
    
    if (filtered.length !== experiences.length) {
      this.saveExperiences(filtered);
    }
  }

  /**
   * 加载技能
   */
  private loadSkills(): Skill[] {
    const content = fs.readFileSync(this.skillsFile, 'utf-8');
    return JSON.parse(content);
  }

  /**
   * 保存技能
   */
  private saveSkills(skills: Skill[]): void {
    fs.writeFileSync(this.skillsFile, JSON.stringify(skills, null, 2), 'utf-8');
  }

  /**
   * 加载经验
   */
  private loadExperiences(): Experience[] {
    const content = fs.readFileSync(this.experiencesFile, 'utf-8');
    return JSON.parse(content);
  }

  /**
   * 保存经验
   */
  private saveExperiences(experiences: Experience[]): void {
    fs.writeFileSync(this.experiencesFile, JSON.stringify(experiences, null, 2), 'utf-8');
  }

  /**
   * 生成 ID
   */
  private generateId(): string {
    return `skill-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`;
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    totalSkills: number;
    totalExperiences: number;
    successRate: number;
  } {
    const skills = this.loadSkills();
    const experiences = this.loadExperiences();
    
    const successes = experiences.filter(e => e.result === 'success').length;
    const failures = experiences.filter(e => e.result === 'failure').length;
    const total = successes + failures;
    
    return {
      totalSkills: skills.length,
      totalExperiences: experiences.length,
      successRate: total > 0 ? successes / total : 0,
    };
  }
}

// 导出
export default SkillEvolver;
