#!/usr/bin/env python3
"""分析技能代码情况"""

from pathlib import Path

base_path = Path(r"C:\Users\shenz\.openclaw\workspace\OpenClaw-good-skill")

skills_with_code = []
skills_without_code = []

for item in base_path.iterdir():
    if not item.is_dir() or item.name.startswith('.') or item.name in ['.git', '.openclaw', 'memory', 'ontology', 'promotions', 'skills']:
        continue
    
    skill_md = item / 'SKILL.md'
    if not skill_md.exists():
        continue
    
    # 查找代码文件
    py_files = list(item.glob('*.py'))
    js_files = list(item.glob('*.js'))
    sh_files = list(item.glob('*.sh'))
    
    if py_files or js_files or sh_files:
        skills_with_code.append({
            'name': item.name,
            'files': [f.name for f in (py_files + js_files + sh_files)],
            'size': sum(f.stat().st_size for f in (py_files + js_files + sh_files))
        })
    else:
        skills_without_code.append(item.name)

print('=== 有代码的技能 ===')
for skill in sorted(skills_with_code, key=lambda x: x['size'], reverse=True):
    print(f"{skill['name']}: {len(skill['files'])}个文件, {skill['size']//1024}KB")

print(f"\n总计: {len(skills_with_code)}个技能有代码")

print('\n=== 只有文档的技能（前30个）===')
for skill in sorted(skills_without_code)[:30]:
    print(f"- {skill}")

print(f"\n总计: {len(skills_without_code)}个技能只有文档")

# 保存列表
with open('skills_with_code.txt', 'w') as f:
    for skill in skills_with_code:
        f.write(f"{skill['name']}\n")

with open('skills_without_code.txt', 'w') as f:
    for skill in skills_without_code:
        f.write(f"{skill}\n")

print("\n已保存到 skills_with_code.txt 和 skills_without_code.txt")
