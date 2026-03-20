#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Habit Tracker - 习惯追踪器
每日打卡、统计分析、习惯养成
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
HABITS_FILE = os.path.join(DATA_DIR, 'habits.json')
LOGS_FILE = os.path.join(DATA_DIR, 'logs.json')


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_habits() -> List[Dict]:
    ensure_data_dir()
    if os.path.exists(HABITS_FILE):
        try:
            with open(HABITS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_habits(habits: List[Dict]):
    ensure_data_dir()
    with open(HABITS_FILE, 'w', encoding='utf-8') as f:
        json.dump(habits, f, indent=2, ensure_ascii=False)


def load_logs() -> List[Dict]:
    ensure_data_dir()
    if os.path.exists(LOGS_FILE):
        try:
            with open(LOGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_logs(logs: List[Dict]):
    ensure_data_dir()
    with open(LOGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


def add_habit(name: str, frequency: str = 'daily', goal: int = 30) -> Dict:
    """添加新习惯"""
    habits = load_habits()
    
    habit_id = max([h.get('id', 0) for h in habits], default=0) + 1
    
    habit = {
        'id': habit_id,
        'name': name,
        'frequency': frequency,  # daily/weekly
        'goal': goal,  # 目标天数
        'created_at': datetime.now().isoformat(),
        'active': True
    }
    
    habits.append(habit)
    save_habits(habits)
    
    return habit


def check_in(habit_id: int, date: Optional[str] = None) -> Dict:
    """打卡"""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    logs = load_logs()
    
    # 检查是否已打卡
    for log in logs:
        if log.get('habit_id') == habit_id and log.get('date') == date:
            return {'success': False, 'message': '今日已打卡'}
    
    log = {
        'habit_id': habit_id,
        'date': date,
        'checked_at': datetime.now().isoformat()
    }
    
    logs.append(log)
    save_logs(logs)
    
    return {'success': True, 'message': '打卡成功！'}


def get_streak(habit_id: int) -> int:
    """获取连续打卡天数"""
    logs = load_logs()
    habit_logs = [l for l in logs if l.get('habit_id') == habit_id]
    
    if not habit_logs:
        return 0
    
    # 按日期排序
    dates = sorted([l['date'] for l in habit_logs], reverse=True)
    
    streak = 1
    today = datetime.now().date()
    
    for i in range(1, len(dates)):
        prev_date = datetime.strptime(dates[i-1], '%Y-%m-%d').date()
        curr_date = datetime.strptime(dates[i], '%Y-%m-%d').date()
        
        if (prev_date - curr_date).days == 1:
            streak += 1
        else:
            break
    
    # 检查今天是否打卡
    if dates[0] != today.strftime('%Y-%m-%d'):
        # 如果昨天没打卡，连续中断
        yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')
        if dates[0] != yesterday:
            return 0
    
    return streak


def get_completion_rate(habit_id: int, days: int = 30) -> float:
    """获取完成率"""
    logs = load_logs()
    habit_logs = [l for l in logs if l.get('habit_id') == habit_id]
    
    if not habit_logs:
        return 0.0
    
    # 统计最近 N 天的打卡
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    checked_days = set()
    for log in habit_logs:
        log_date = datetime.strptime(log['date'], '%Y-%m-%d').date()
        if start_date <= log_date <= end_date:
            checked_days.add(log_date)
    
    return len(checked_days) / days * 100


def list_habits() -> List[Dict]:
    """列出所有习惯"""
    habits = load_habits()
    
    result = []
    for habit in habits:
        if not habit.get('active'):
            continue
        
        streak = get_streak(habit['id'])
        rate = get_completion_rate(habit['id'])
        
        result.append({
            **habit,
            'streak': streak,
            'completion_rate': f"{rate:.1f}%"
        })
    
    return result


def get_today_checkins() -> List[Dict]:
    """获取今日打卡情况"""
    habits = load_habits()
    logs = load_logs()
    today = datetime.now().strftime('%Y-%m-%d')
    
    result = []
    for habit in habits:
        if not habit.get('active'):
            continue
        
        checked = any(
            l.get('habit_id') == habit['id'] and l.get('date') == today
            for l in logs
        )
        
        result.append({
            'id': habit['id'],
            'name': habit['name'],
            'checked': checked,
            'streak': get_streak(habit['id'])
        })
    
    return result


def run(command: str = '', args: List[str] = None) -> str:
    """主入口"""
    args = args or []
    
    if command == 'add' or command == '添加':
        name = ' '.join(args) if args else '新习惯'
        habit = add_habit(name)
        return f"✅ 已添加习惯 #{habit['id']}: {habit['name']}"
    
    elif command == 'checkin' or command == '打卡':
        if not args:
            # 显示今日待打卡
            checkins = get_today_checkins()
            unchecked = [c for c in checkins if not c['checked']]
            
            if not unchecked:
                return "🎉 今日所有习惯已打卡！"
            
            lines = ["📅 今日待打卡:"]
            for c in unchecked:
                lines.append(f"⬜ #{c['id']} {c['name']} (连续{c['streak']}天)")
            
            return '\n'.join(lines)
        
        try:
            habit_id = int(args[0])
            result = check_in(habit_id)
            if result['success']:
                streak = get_streak(habit_id)
                return f"✅ 打卡成功！🔥 连续{streak}天"
            else:
                return f"⚠️ {result['message']}"
        except ValueError:
            return "❌ 习惯 ID 必须是数字"
    
    elif command == 'list' or command == '查看':
        habits = list_habits()
        
        if not habits:
            return "📭 暂无习惯"
        
        lines = [f"🎯 习惯列表 ({len(habits)} 个):"]
        for h in habits:
            icon = '🔥' if h['streak'] > 7 else '⭐'
            lines.append(f"{icon} #{h['id']} {h['name']}")
            lines.append(f"   连续：{h['streak']}天 | 完成率：{h['completion_rate']}")
        
        return '\n'.join(lines)
    
    elif command == 'stats' or command == '统计':
        habits = list_habits()
        
        if not habits:
            return "📭 暂无习惯"
        
        total_streak = sum(h['streak'] for h in habits)
        avg_rate = sum(float(h['completion_rate'].replace('%', '')) for h in habits) / len(habits)
        
        lines = [
            "📊 习惯追踪统计:",
            f"├─ 习惯总数：{len(habits)}",
            f"├─ 总连续天数：{total_streak} 🔥",
            f"├─ 平均完成率：{avg_rate:.1f}%",
            "",
            "习惯详情:"
        ]
        
        for h in sorted(habits, key=lambda x: x['streak'], reverse=True):
            lines.append(f"├─ {h['name']}: {h['streak']}天连续 | {h['completion_rate']}完成")
        
        return '\n'.join(lines)
    
    elif command == 'today' or command == '今日':
        checkins = get_today_checkins()
        
        checked = [c for c in checkins if c['checked']]
        unchecked = [c for c in checkins if not c['checked']]
        
        lines = [f"📅 今日打卡 ({len(checked)}/{len(checkins)}):"]
        
        if checked:
            lines.append("✅ 已完成:")
            for c in checked:
                lines.append(f"   {c['name']} (连续{c['streak']}天)")
        
        if unchecked:
            lines.append("⬜ 待完成:")
            for c in unchecked:
                lines.append(f"   {c['name']} (连续{c['streak']}天)")
        
        return '\n'.join(lines)
    
    elif command == 'help' or command == '帮助':
        return """
🎯 Habit Tracker - 习惯追踪器

可用命令:
  add/添加 [习惯名称]           - 添加新习惯
  checkin/打卡 [习惯 ID]         - 打卡
  list/查看                     - 查看所有习惯
  today/今日                    - 查看今日打卡
  stats/统计                    - 查看统计
  help/帮助                     - 显示帮助

示例:
  添加习惯：add 早起跑步
  打卡：checkin 1
  查看今日：today
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
