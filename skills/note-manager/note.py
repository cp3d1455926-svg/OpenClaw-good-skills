#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Note Manager - 笔记管理
快速记录、标签分类、搜索查询
"""

import json
import os
from datetime import datetime
from typing import List, Dict

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
NOTES_FILE = os.path.join(DATA_DIR, 'notes.json')


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_notes() -> List[Dict]:
    ensure_data_dir()
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_notes(notes: List[Dict]):
    ensure_data_dir()
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


def create_note(content: str, tags: List[str] = None, title: str = None) -> Dict:
    """创建笔记"""
    notes = load_notes()
    
    note_id = max([n.get('id', 0) for n in notes], default=0) + 1
    
    note = {
        'id': note_id,
        'title': title or f"笔记 #{note_id}",
        'content': content,
        'tags': tags or [],
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    notes.append(note)
    save_notes(notes)
    
    return note


def get_note(note_id: int) -> Dict:
    """获取单条笔记"""
    notes = load_notes()
    
    for note in notes:
        if note.get('id') == note_id:
            return note
    
    return None


def update_note(note_id: int, content: str = None, tags: List[str] = None, title: str = None) -> Dict:
    """更新笔记"""
    notes = load_notes()
    
    for note in notes:
        if note.get('id') == note_id:
            if content:
                note['content'] = content
            if tags:
                note['tags'] = tags
            if title:
                note['title'] = title
            note['updated_at'] = datetime.now().isoformat()
            
            save_notes(notes)
            return note
    
    return None


def delete_note(note_id: int) -> bool:
    """删除笔记"""
    notes = load_notes()
    original_len = len(notes)
    
    notes = [n for n in notes if n.get('id') != note_id]
    
    if len(notes) < original_len:
        save_notes(notes)
        return True
    
    return False


def search_notes(query: str = None, tag: str = None) -> List[Dict]:
    """搜索笔记"""
    notes = load_notes()
    results = []
    
    for note in notes:
        match = False
        
        if query:
            if (query.lower() in note.get('title', '').lower() or 
                query.lower() in note.get('content', '').lower()):
                match = True
        
        if tag:
            if tag in note.get('tags', []):
                match = True
        
        if (query and tag):
            if (query.lower() in note.get('title', '').lower() or 
                query.lower() in note.get('content', '').lower()) and tag in note.get('tags', []):
                match = True
        
        if not query and not tag:
            match = True
        
        if match:
            results.append(note)
    
    # 按更新时间排序
    results.sort(key=lambda n: n.get('updated_at', ''), reverse=True)
    
    return results


def get_all_tags() -> List[str]:
    """获取所有标签"""
    notes = load_notes()
    tags = set()
    
    for note in notes:
        for tag in note.get('tags', []):
            tags.add(tag)
    
    return sorted(list(tags))


def run(command: str = '', args: List[str] = None) -> str:
    """主入口"""
    args = args or []
    
    if command == 'new' or command == '新建':
        content = ' '.join(args) if args else ''
        
        # 解析标签 #tag
        tags = []
        words = content.split()
        content_words = []
        
        for word in words:
            if word.startswith('#'):
                tags.append(word[1:])
            else:
                content_words.append(word)
        
        content = ' '.join(content_words)
        note = create_note(content, tags)
        
        tags_str = ' '.join(f"#{t}" for t in tags) if tags else ''
        return f"✅ 已创建笔记 #{note['id']}\n标题：{note['title']}\n标签：{tags_str}"
    
    elif command == 'list' or command == '查看':
        notes = search_notes()
        
        if not notes:
            return "📭 暂无笔记"
        
        lines = [f"📝 笔记列表 ({len(notes)} 条):"]
        
        for note in notes[:20]:  # 显示最近 20 条
            tags = ' '.join(f"#{t}" for t in note.get('tags', []))
            preview = note.get('content', '')[:30] + '...' if len(note.get('content', '')) > 30 else note.get('content', '')
            updated = datetime.fromisoformat(note['updated_at']).strftime('%m-%d %H:%M')
            
            lines.append(f"├─ #{note['id']} {note['title']}")
            lines.append(f"│  {preview}")
            lines.append(f"│  {tags} | {updated}")
        
        if len(notes) > 20:
            lines.append(f"└─ ... 还有{len(notes) - 20}条")
        
        return '\n'.join(lines)
    
    elif command == 'show' or command == '显示':
        if not args:
            return "❌ 请提供笔记 ID"
        
        try:
            note_id = int(args[0])
            note = get_note(note_id)
            
            if note:
                tags = ' '.join(f"#{t}" for t in note.get('tags', []))
                created = datetime.fromisoformat(note['created_at']).strftime('%Y-%m-%d %H:%M')
                updated = datetime.fromisoformat(note['updated_at']).strftime('%Y-%m-%d %H:%M')
                
                return f"""
📝 笔记 #{note['id']}

标题：{note['title']}
标签：{tags}
创建：{created}
更新：{updated}

内容:
{note['content']}
                """.strip()
            else:
                return f"❌ 未找到笔记 #{note_id}"
        except ValueError:
            return "❌ 笔记 ID 必须是数字"
    
    elif command == 'search' or command == '搜索':
        query = ' '.join(args) if args else ''
        
        # 检查是否有标签搜索
        tag = None
        if query.startswith('#'):
            tag = query[1:].split()[0]
            query = ''
        
        notes = search_notes(query, tag)
        
        if not notes:
            return f"📭 未找到匹配的笔记"
        
        lines = [f"🔍 搜索结果 ({len(notes)} 条):"]
        
        for note in notes[:10]:
            tags = ' '.join(f"#{t}" for t in note.get('tags', []))
            preview = note.get('content', '')[:40] + '...' if len(note.get('content', '')) > 40 else note.get('content', '')
            
            lines.append(f"├─ #{note['id']} {note['title']}")
            lines.append(f"│  {preview}")
            lines.append(f"│  {tags}")
        
        return '\n'.join(lines)
    
    elif command == 'delete' or command == '删除':
        if not args:
            return "❌ 请提供笔记 ID"
        
        try:
            note_id = int(args[0])
            if delete_note(note_id):
                return f"✅ 已删除笔记 #{note_id}"
            else:
                return f"❌ 未找到笔记 #{note_id}"
        except ValueError:
            return "❌ 笔记 ID 必须是数字"
    
    elif command == 'tags' or command == '标签':
        tags = get_all_tags()
        
        if not tags:
            return "🏷️ 暂无标签"
        
        return "🏷️ 所有标签:\n" + '\n'.join(f"├─ #{t}" for t in tags)
    
    elif command == 'stats' or command == '统计':
        notes = load_notes()
        tags = get_all_tags()
        
        return f"""
📊 笔记统计:
├─ 总笔记数：{len(notes)}
├─ 标签数量：{len(tags)}
└─ 最近标签：{', '.join(f'#{t}' for t in tags[:5]) if tags else '无'}
        """.strip()
    
    elif command == 'help' or command == '帮助':
        return """
📝 Note Manager - 笔记管理

可用命令:
  new/新建 [内容]              - 创建笔记 (用#tag 添加标签)
  list/查看                   - 查看所有笔记
  show/显示 [ID]               - 查看笔记详情
  search/搜索 [关键词]          - 搜索笔记
  delete/删除 [ID]             - 删除笔记
  tags/标签                   - 查看所有标签
  stats/统计                  - 查看统计
  help/帮助                   - 显示帮助

示例:
  新建笔记：new 今天学习了 Python #学习 #编程
  查看笔记：list
  搜索笔记：search Python
  按标签搜：search #学习
        """.strip()
    
    else:
        return "❌ 未知命令，输入 help 查看帮助"


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print(run('help'))
    else:
        command = sys.argv[1]
        args = sys.argv[2:]
        print(run(command, args))
