#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📅 Calendar Manager - 日历管理助手
功能：日程管理、提醒、查看
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).parent
EVENTS_FILE = DATA_DIR / "events.json"


def load_events():
    """加载日程"""
    if EVENTS_FILE.exists():
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"events": []}


def save_events(data):
    """保存日程"""
    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_event(title, start, end=None, reminder=True):
    """添加日程"""
    data = load_events()
    
    event = {
        "title": title,
        "start": start,
        "end": end or start,
        "reminder": reminder,
        "created": datetime.now().isoformat()
    }
    
    data["events"].append(event)
    save_events(data)
    
    return event


def get_today_events():
    """获取今日日程"""
    data = load_events()
    today = datetime.now().strftime("%Y-%m-%d")
    
    return [e for e in data["events"] if e["start"].startswith(today)]


def format_events(events, title="日程"):
    """格式化日程"""
    if not events:
        return f"📅 {title}：暂无安排"
    
    response = f"📅 **{title}**：\n\n"
    for e in events:
        start_time = e["start"].split("T")[1] if "T" in e["start"] else e["start"]
        response += f"⏰ {start_time} {e['title']}\n"
    
    return response


def main(query):
    """主函数"""
    query = query.lower()
    
    # 添加日程
    if "添加" in query or "安排" in query or "点" in query:
        import re
        time_match = re.search(r'(\d+) 点', query)
        if time_match:
            hour = int(time_match.group(1))
            today = datetime.now().strftime("%Y-%m-%d")
            start = f"{today}T{hour:02d}:00:00"
            
            # 提取标题
            title = query.replace(f"{hour}点", "").replace("添加", "").replace("安排", "").strip()
            if not title:
                title = "未命名日程"
            
            add_event(title, start)
            return f"✅ 日程已添加：{title}（{hour}:00）"
    
    # 查看今日日程
    if "今天" in query or "今日" in query:
        events = get_today_events()
        return format_events(events, "今日日程")
    
    # 查看日程列表
    if "日程" in query and "列表" in query:
        data = load_events()
        return format_events(data["events"][:10], "最近日程")
    
    # 默认回复
    return """📅 日历管理助手

**功能**：
1. 添加日程 - "今天下午 3 点开会"
2. 查看日程 - "今天有什么安排"
3. 日程列表 - "我的日程列表"

告诉我你要添加什么日程？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(main("今天有什么安排"))
