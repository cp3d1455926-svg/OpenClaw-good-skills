#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Time Tracker - 时间记录
番茄工作法、时间块记录、效率分析
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
SESSIONS_FILE = os.path.join(DATA_DIR, 'sessions.json')


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_sessions() -> List[Dict]:
    ensure_data_dir()
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_sessions(sessions: List[Dict]):
    ensure_data_dir()
    with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)


def start_session(task: str, session_type: str = 'work') -> Dict:
    """开始时间记录"""
    sessions = load_sessions()
    
    # 结束当前未结束的 session
    for s in sessions:
        if not s.get('end_time'):
            s['end_time'] = datetime.now().isoformat()
    
    session = {
        'id': len(sessions) + 1,
        'task': task,
        'type': session_type,  # work/break/long_break
        'start_time': datetime.now().isoformat(),
        'end_time': None
    }
    
    sessions.append(session)
    save_sessions(sessions)
    
    return session


def end_session() -> Optional[Dict]:
    """结束当前时间记录"""
    sessions = load_sessions()
    
    for session in reversed(sessions):
        if not session.get('end_time'):
            session['end_time'] = datetime.now().isoformat()
            
            # 计算时长
            start = datetime.fromisoformat(session['start_time'])
            end = datetime.fromisoformat(session['end_time'])
            duration = (end - start).total_seconds() / 60  # 分钟
            
            session['duration_minutes'] = round(duration, 1)
            
            save_sessions(sessions)
            return session
    
    return None


def get_active_session() -> Optional[Dict]:
    """获取当前进行中的 session"""
    sessions = load_sessions()
    
    for session in reversed(sessions):
        if not session.get('end_time'):
            return session
    
    return None


def pomodoro() -> str:
    """番茄工作法"""
    session = start_session('番茄工作', 'work')
    
    return f"""
🍅 番茄钟开始！

任务：{session['task']}
开始时间：{datetime.fromisoformat(session['start_time']).strftime('%H:%M:%S')}

建议：
- 专注工作 25 分钟
- 然后休息 5 分钟
- 每 4 个番茄钟后休息 15-30 分钟

结束命令：end/结束
    """.strip()


def get_today_stats() -> Dict:
    """获取今日统计"""
    sessions = load_sessions()
    today = datetime.now().date()
    
    today_sessions = []
    for s in sessions:
        start = datetime.fromisoformat(s['start_time'])
        if start.date() == today and s.get('end_time'):
            today_sessions.append(s)
    
    total_minutes = sum(s.get('duration_minutes', 0) for s in today_sessions)
    
    by_type = {}
    for s in today_sessions:
        t = s.get('type', 'work')
        if t not in by_type:
            by_type[t] = 0
        by_type[t] += s.get('duration_minutes', 0)
    
    return {
        'total_minutes': round(total_minutes, 1),
        'total_hours': round(total_minutes / 60, 2),
        'sessions_count': len(today_sessions),
        'by_type': by_type
    }


def run(command: str = '', args: List[str] = None) -> str:
    """主入口"""
    args = args or []
    
    if command == 'start' or command == '开始':
        task = ' '.join(args) if args else '未命名任务'
        session = start_session(task)
        start_time = datetime.fromisoformat(session['start_time']).strftime('%H:%M:%S')
        return f"⏱️ 开始记录：{task}\n时间：{start_time}\n\n结束命令：end/结束"
    
    elif command == 'end' or command == '结束':
        session = end_session()
        
        if session:
            duration = session.get('duration_minutes', 0)
            return f"✅ 结束记录：{session['task']}\n时长：{duration} 分钟"
        else:
            return "⚠️ 没有进行中的记录"
    
    elif command == 'status' or command == '状态':
        session = get_active_session()
        
        if session:
            start = datetime.fromisoformat(session['start_time'])
            elapsed = (datetime.now() - start).total_seconds() / 60
            return f"⏱️ 进行中：{session['task']}\n已用：{elapsed:.1f} 分钟\n类型：{session['type']}"
        else:
            return "⏸️ 暂无进行中的记录"
    
    elif command == 'pomodoro' or command == '番茄':
        return pomodoro()
    
    elif command == 'stats' or command == '统计':
        stats = get_today_stats()
        
        lines = [
            "📊 今日时间统计:",
            f"├─ 总时长：{stats['total_hours']} 小时 ({stats['total_minutes']} 分钟)",
            f"├─ 记录次数：{stats['sessions_count']}",
        ]
        
        type_names = {'work': '工作', 'break': '休息', 'long_break': '长休息'}
        for t, minutes in stats['by_type'].items():
            name = type_names.get(t, t)
            hours = minutes / 60
            lines.append(f"├─ {name}: {hours:.2f} 小时")
        
        return '\n'.join(lines)
    
    elif command == 'today' or command == '今日':
        stats = get_today_stats()
        sessions = load_sessions()
        today = datetime.now().date()
        
        today_sessions = [
            s for s in sessions 
            if datetime.fromisoformat(s['start_time']).date() == today and s.get('end_time')
        ]
        
        if not today_sessions:
            return "📭 今日暂无时间记录"
        
        lines = [f"📅 今日记录 ({len(today_sessions)} 次):"]
        
        for s in today_sessions[-10:]:  # 显示最近 10 条
            start = datetime.fromisoformat(s['start_time']).strftime('%H:%M')
            duration = s.get('duration_minutes', 0)
            lines.append(f"├─ {start} {s['task']} ({duration}分钟)")
        
        if len(today_sessions) > 10:
            lines.append(f"└─ ... 还有{len(today_sessions) - 10}条")
        
        return '\n'.join(lines)
    
    elif command == 'help' or command == '帮助':
        return """
⏱️ Time Tracker - 时间记录

可用命令:
  start/开始 [任务名]           - 开始记录
  end/结束                     - 结束记录
  status/状态                  - 查看当前状态
  pomodoro/番茄                - 启动番茄钟
  stats/统计                   - 今日统计
  today/今日                   - 今日记录详情
  help/帮助                    - 显示帮助

示例:
  开始任务：start 写代码
  番茄工作：pomodoro
  结束记录：end
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
