#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Todo List - 智能待办事项管理
支持 GTD 方法、优先级排序、智能提醒
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
TASKS_FILE = os.path.join(DATA_DIR, 'tasks.json')


def ensure_data_dir():
    """确保数据目录存在"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_tasks() -> List[Dict]:
    """加载任务列表"""
    ensure_data_dir()
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_tasks(tasks: List[Dict]):
    """保存任务列表"""
    ensure_data_dir()
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(title: str, priority: str = 'medium', category: str = 'other', 
             due_date: Optional[str] = None) -> Dict:
    """添加新任务"""
    tasks = load_tasks()
    
    # 生成 ID
    task_id = max([t.get('id', 0) for t in tasks], default=0) + 1
    
    # 解析截止日期
    if due_date:
        try:
            due = datetime.fromisoformat(due_date)
        except:
            due = datetime.now() + timedelta(days=1)
    else:
        due = None
    
    task = {
        'id': task_id,
        'title': title,
        'priority': priority,
        'category': category,
        'due_date': due.isoformat() if due else None,
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    
    tasks.append(task)
    save_tasks(tasks)
    
    return task


def list_tasks(filter_type: str = 'all', category: Optional[str] = None) -> List[Dict]:
    """查看任务列表
    
    filter_type: all/today/week/completed/pending
    category: work/study/life/other
    """
    tasks = load_tasks()
    now = datetime.now()
    
    filtered = []
    
    for task in tasks:
        # 按状态过滤
        if filter_type == 'completed' and not task.get('completed'):
            continue
        if filter_type == 'pending' and task.get('completed'):
            continue
        
        if filter_type == 'today':
            due = task.get('due_date')
            if due:
                due_date = datetime.fromisoformat(due).date()
                if due_date != now.date():
                    continue
            else:
                continue
        
        if filter_type == 'week':
            due = task.get('due_date')
            if due:
                due_date = datetime.fromisoformat(due).date()
                week_end = now.date() + timedelta(days=7)
                if due_date < now.date() or due_date > week_end:
                    continue
        
        # 按分类过滤
        if category and task.get('category') != category:
            continue
        
        filtered.append(task)
    
    # 按优先级排序
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    filtered.sort(key=lambda t: (
        t.get('completed', False),
        priority_order.get(t.get('priority', 'medium'), 1)
    ))
    
    return filtered


def complete_task(task_id: int) -> Optional[Dict]:
    """完成任务"""
    tasks = load_tasks()
    
    for task in tasks:
        if task.get('id') == task_id:
            task['completed'] = True
            task['completed_at'] = datetime.now().isoformat()
            save_tasks(tasks)
            return task
    
    return None


def delete_task(task_id: int) -> bool:
    """删除任务"""
    tasks = load_tasks()
    original_len = len(tasks)
    
    tasks = [t for t in tasks if t.get('id') != task_id]
    
    if len(tasks) < original_len:
        save_tasks(tasks)
        return True
    
    return False


def get_stats() -> Dict:
    """获取统计信息"""
    tasks = load_tasks()
    now = datetime.now()
    
    total = len(tasks)
    completed = sum(1 for t in tasks if t.get('completed'))
    pending = total - completed
    
    # 今日任务
    today = sum(1 for t in tasks if t.get('due_date') and 
                datetime.fromisoformat(t['due_date']).date() == now.date())
    
    # 本周任务
    week_end = now.date() + timedelta(days=7)
    this_week = sum(1 for t in tasks if t.get('due_date') and 
                   now.date() <= datetime.fromisoformat(t['due_date']).date() <= week_end)
    
    # 逾期任务
    overdue = sum(1 for t in tasks if t.get('due_date') and 
                  datetime.fromisoformat(t['due_date']).date() < now.date() and 
                  not t.get('completed'))
    
    # 按优先级统计
    high = sum(1 for t in tasks if t.get('priority') == 'high' and not t.get('completed'))
    medium = sum(1 for t in tasks if t.get('priority') == 'medium' and not t.get('completed'))
    low = sum(1 for t in tasks if t.get('priority') == 'low' and not t.get('completed'))
    
    # 按分类统计
    categories = {}
    for task in tasks:
        cat = task.get('category', 'other')
        if cat not in categories:
            categories[cat] = {'total': 0, 'completed': 0}
        categories[cat]['total'] += 1
        if task.get('completed'):
            categories[cat]['completed'] += 1
    
    return {
        'total': total,
        'completed': completed,
        'pending': pending,
        'today': today,
        'this_week': this_week,
        'overdue': overdue,
        'by_priority': {
            'high': high,
            'medium': medium,
            'low': low
        },
        'by_category': categories,
        'completion_rate': f"{completed/total*100:.1f}%" if total > 0 else "0%"
    }


def format_task(task: Dict) -> str:
    """格式化任务显示"""
    priority_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
    category_icons = {'work': '💼', 'study': '📚', 'life': '🏠', 'other': '📦'}
    
    icon = '✅' if task.get('completed') else '⬜'
    priority = priority_icons.get(task.get('priority', 'medium'), '🟡')
    category = category_icons.get(task.get('category', 'other'), '📦')
    
    due = ''
    if task.get('due_date'):
        due_date = datetime.fromisoformat(task['due_date'])
        due = f" 📅 {due_date.strftime('%m-%d %H:%M')}"
    
    return f"{icon} {priority} {category} #{task['id']} {task['title']}{due}"


def run(command: str = '', args: List[str] = None) -> str:
    """主入口函数"""
    args = args or []
    
    if command == 'add' or command == '添加':
        title = ' '.join(args) if args else '新任务'
        task = add_task(title)
        return f"✅ 已添加任务 #{task['id']}: {task['title']}"
    
    elif command == 'list' or command == '查看':
        filter_type = args[0] if args else 'all'
        tasks = list_tasks(filter_type)
        
        if not tasks:
            return "📭 暂无任务"
        
        lines = [f"📋 待办事项 ({len(tasks)} 个):"]
        for task in tasks:
            lines.append(format_task(task))
        
        return '\n'.join(lines)
    
    elif command == 'complete' or command == '完成':
        if not args:
            return "❌ 请提供任务 ID"
        
        try:
            task_id = int(args[0])
            task = complete_task(task_id)
            if task:
                return f"✅ 已完成任务 #{task_id}: {task['title']}"
            else:
                return f"❌ 未找到任务 #{task_id}"
        except ValueError:
            return "❌ 任务 ID 必须是数字"
    
    elif command == 'delete' or command == '删除':
        if not args:
            return "❌ 请提供任务 ID"
        
        try:
            task_id = int(args[0])
            if delete_task(task_id):
                return f"✅ 已删除任务 #{task_id}"
            else:
                return f"❌ 未找到任务 #{task_id}"
        except ValueError:
            return "❌ 任务 ID 必须是数字"
    
    elif command == 'stats' or command == '统计':
        stats = get_stats()
        
        lines = [
            "📊 待办事项统计:",
            f"├─ 总任务数：{stats['total']}",
            f"├─ 已完成：{stats['completed']}",
            f"├─ 待完成：{stats['pending']}",
            f"├─ 完成率：{stats['completion_rate']}",
            f"├─ 今日任务：{stats['today']}",
            f"├─ 本周任务：{stats['this_week']}",
            f"└─ 逾期任务：{stats['overdue']} 🔴",
            "",
            "按优先级:",
            f"├─ 高优先级：{stats['by_priority']['high']} 🔴",
            f"├─ 中优先级：{stats['by_priority']['medium']} 🟡",
            f"└─ 低优先级：{stats['by_priority']['low']} 🟢"
        ]
        
        return '\n'.join(lines)
    
    elif command == 'help' or command == '帮助':
        return """
📝 Todo List - 待办事项管理

可用命令:
  add/添加 [任务内容]          - 添加新任务
  list/查看 [today/week/all]   - 查看任务列表
  complete/完成 [任务 ID]       - 完成任务
  delete/删除 [任务 ID]         - 删除任务
  stats/统计                   - 查看统计信息
  help/帮助                    - 显示帮助

示例:
  添加任务：明天下午 3 点开会，优先级高
  查看今天：list today
  完成任务：complete 1
  查看统计：stats
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
