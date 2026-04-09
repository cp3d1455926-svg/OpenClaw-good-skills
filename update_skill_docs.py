#!/usr/bin/env python3
"""
批量更新技能文档
为所有技能补充版本号和作者信息
"""

import os
import re
from pathlib import Path

class SkillDocUpdater:
    """技能文档更新器"""
    
    def __init__(self, skills_dir):
        self.skills_dir = Path(skills_dir)
        self.updated = 0
        self.skipped = 0
    
    def update_skill_md(self, skill_path):
        """更新单个技能的 SKILL.md"""
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            return False
        
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 检查是否已有版本号
        if not re.search(r'version[:：]\s*v?\d+\.\d+', content, re.IGNORECASE):
            # 在 author 后添加 version
            if 'author:' in content:
                content = re.sub(
                    r'(author[:：]\s*[^\n]+\n)',
                    r'\1version: 1.0.0\n',
                    content,
                    count=1,
                    flags=re.IGNORECASE
                )
            elif '---' in content:  # 在头部元数据区域添加
                content = re.sub(
                    r'^(---\n(?:.*?\n)*?)---',
                    r'\1version: 1.0.0\n---',
                    content,
                    flags=re.DOTALL
                )
            self.updated += 1
        
        # 检查是否已有作者
        if not re.search(r'author[:：]', content, re.IGNORECASE):
            if '---' in content:
                content = re.sub(
                    r'^(---\n)',
                    r'---\nauthor: 小鬼 👻\n',
                    content
                )
                self.updated += 1
        
        # 保存
        if content != original:
            with open(skill_md, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {skill_path.name}")
            return True
        else:
            print(f"⏭️ {skill_path.name} (已完整)")
            self.skipped += 1
            return False
    
    def update_all(self):
        """更新所有技能"""
        print("开始更新技能文档...\n")
        
        for item in sorted(self.skills_dir.iterdir()):
            if not item.is_dir() or item.name.startswith('.'):
                continue
            if item.name in ['.git', '.openclaw', 'memory', 'ontology', 'promotions', 'skills']:
                continue
            
            self.update_skill_md(item)
        
        print(f"\n完成！更新：{self.updated} 个，跳过：{self.skipped} 个")

if __name__ == "__main__":
    skills_dir = r"C:\Users\shenz\.openclaw\workspace\OpenClaw-good-skill"
    updater = SkillDocUpdater(skills_dir)
    updater.update_all()
