#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Habit Tracker v2.0 - 习惯养成助手
功能：习惯打卡、统计分析、成就系统、习惯库、提醒督促
代码量：~14KB
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

DATA_DIR = Path(__file__).parent
HABITS_FILE = DATA_DIR / "habits.json"
ACHIEVEMENTS_FILE = DATA_DIR / "achievements.json"

# ============================================================================
# 📚 习惯库（20+ 习惯模板）
# ============================================================================
HABIT_LIBRARY = {
    # 健康类
    "每天运动": {
        "category": "健康",
        "default_time": "07:00",
        "frequency": "daily",
        "description": "每天至少运动 30 分钟",
        "tips": ["晨跑", "瑜伽", "健身房", "居家 HIIT"],
        "milestones": [7, 21, 30, 60, 90, 100]
    },
    "早睡早起": {
        "category": "健康",
        "default_time": "23:00",
        "frequency": "daily",
        "description": "23 点前睡觉，7 点前起床",
        "tips": ["睡前不玩手机", "泡脚", "调暗灯光"],
        "milestones": [7, 21, 30, 60, 90, 100]
    },
    "健康饮食": {
        "category": "健康",
        "default_time": "12:00",
        "frequency": "daily",
        "description": "三餐规律，少油少盐",
        "tips": ["自己做饭", "多吃蔬菜", "少喝奶茶"],
        "milestones": [7, 21, 30, 60, 90, 100]
    },
    "喝水打卡": {
        "category": "健康",
        "default_time": "09:00",
        "frequency": "daily",
        "description": "每天喝 8 杯水 (2000ml)",
        "tips": ["买大水杯", "设提醒", "饭前一杯水"],
        "milestones": [7, 14, 30, 60, 90, 100]
    },
    "冥想静心": {
        "category": "健康",
        "default_time": "21:00",
        "frequency": "daily",
        "description": "每天冥想 10-20 分钟",
        "tips": ["用冥想 APP", "安静环境", "专注呼吸"],
        "milestones": [7, 21, 30, 60, 90, 100]
    },
    
    # 学习类
    "每天读书": {
        "category": "学习",
        "default_time": "21:00",
        "frequency": "daily",
        "description": "每天读书至少 30 分钟",
        "tips": ["纸质书更好", "做笔记", "固定时间"],
        "milestones": [7, 21, 30, 60, 90, 100, 365]
    },
    "学英语": {
        "category": "学习",
        "default_time": "08:00",
        "frequency": "daily",
        "description": "每天学习英语 30 分钟",
        "tips": ["背单词 APP", "听英语播客", "看美剧"],
        "milestones": [7, 21, 30, 60, 90, 100, 365]
    },
    "学编程": {
        "category": "学习",
        "default_time": "20:00",
        "frequency": "daily",
        "description": "每天编程练习 1 小时",
        "tips": ["LeetCode", "做项目", "看技术文档"],
        "milestones": [7, 21, 30, 60, 90, 100, 365]
    },
    "写日记": {
        "category": "学习",
        "default_time": "22:00",
        "frequency": "daily",
        "description": "每天写日记复盘",
        "tips": ["记录三件好事", "反思改进", "感恩日记"],
        "milestones": [7, 21, 30, 60, 90, 100, 365]
    },
    "学乐器": {
        "category": "学习",
        "default_time": "19:00",
        "frequency": "daily",
        "description": "每天练习乐器 30 分钟",
        "tips": ["固定练习时间", "录下来听", "找老师"],
        "milestones": [7, 21, 30, 60, 90, 100, 365]
    },
    
    # 工作类
    "今日事今日毕": {
        "category": "工作",
        "default_time": "18:00",
        "frequency": "daily",
        "description": "当天任务当天完成",
        "tips": ["列 To-Do 清单", "优先级排序", "番茄工作法"],
        "milestones": [7, 21, 30, 60, 90, 100]
    },
    "时间管理": {
        "category": "工作",
        "default_time": "09:00",
        "frequency": "daily",
        "description": "使用时间块管理时间",
        "tips": ["日历规划", "番茄钟", "避免多任务"],
        "milestones": [7, 21, 30, 60, 90, 100]
    },
    "深度工作": {
        "category": "工作",
        "default_time": "10:00",
        "frequency": "daily",
        "description": "每天 2 小时深度工作",
        "tips": ["关闭通知", "固定时间", "单任务"],
        "milestones": [7, 21, 30, 60, 90, 100]
    },
    "周复盘": {
        "category": "工作",
        "default_time": "20:00",
        "frequency": "weekly",
        "description": "每周日复盘本周工作",
        "tips": ["回顾目标", "分析得失", "规划下周"],
        "milestones": [4, 12, 24, 52]
    },
    
    # 生活类
    "整理房间": {
        "category": "生活",
        "default_time": "20:00",
        "frequency": "daily",
        "description": "每天整理房间 15 分钟",
        "tips": ["断舍离", "物归原位", "定期大扫除"],
        "milestones": [7, 21, 30, 60, 90, 100]
    },
    "记账": {
        "category": "生活",
        "default_time": "22:00",
        "frequency": "daily",
        "description": "每天记录收支",
        "tips": ["用记账 APP", "保留小票", "定期复盘"],
        "milestones": [7, 21, 30, 60, 90, 100, 365]
    },
    "陪家人": {
        "category": "生活",
        "default_time": "19:00",
        "frequency": "daily",
        "description": "每天陪家人聊天 30 分钟",
        "tips": ["放下手机", "用心倾听", "一起吃饭"],
        "milestones": [7, 21, 30, 60, 90, 100]
    },
    "晒太阳": {
        "category": "生活",
        "default_time": "10:00",
        "frequency": "daily",
        "description": "每天晒太阳 15 分钟",
        "tips": ["上午 10 点前", "户外活动", "注意防晒"],
        "milestones": [7, 21, 30, 60, 90, 100]
    },
    "微笑打卡": {
        "category": "生活",
        "default_time": "08:00",
        "frequency": "daily",
        "description": "每天保持好心情",
        "tips": ["对镜子微笑", "想开心事", "积极暗示"],
        "milestones": [7, 21, 30, 60, 90, 100]
    },
    
    # 社交类
    "社交拓展": {
        "category": "社交",
        "default_time": "15:00",
        "frequency": "weekly",
        "description": "每周认识一个新朋友",
        "tips": ["参加活动", "主动交流", "保持联系"],
        "milestones": [4, 12, 24, 52]
    },
    "感恩打卡": {
        "category": "社交",
        "default_time": "21:00",
        "frequency": "daily",
        "description": "每天记录 3 件感恩的事",
        "tips": ["写感恩日记", "感谢他人", "珍惜当下"],
        "milestones": [7, 21, 30, 60, 90, 100]
    }
}

# ============================================================================
# 🏆 成就系统
# ============================================================================
ACHIEVEMENTS = {
    # 新手成就
    "初出茅庐": {"desc": "首次打卡", "condition": lambda s: s >= 1, "icon": "🌱"},
    "崭露头角": {"desc": "连续打卡 3 天", "condition": lambda s: s >= 3, "icon": "🌿"},
    "持之以恒": {"desc": "连续打卡 7 天", "condition": lambda s: s >= 7, "icon": "🌳"},
    "习惯养成": {"desc": "连续打卡 21 天", "condition": lambda s: s >= 21, "icon": "🏆"},
    "百日战神": {"desc": "连续打卡 100 天", "condition": lambda s: s >= 100, "icon": "👑"},
    
    # 数量成就
    "打卡新手": {"desc": "累计打卡 10 次", "condition": lambda t: t >= 10, "icon": "⭐"},
    "打卡达人": {"desc": "累计打卡 50 次", "condition": lambda t: t >= 50, "icon": "🌟"},
    "打卡王者": {"desc": "累计打卡 200 次", "condition": lambda t: t >= 200, "icon": "💫"},
    
    # 多习惯成就
    "多面手": {"desc": "同时坚持 3 个习惯", "condition": lambda c: c >= 3, "icon": "🎭"},
    "全能王": {"desc": "同时坚持 5 个习惯", "condition": lambda c: c >= 5, "icon": "🎪"},
}

# ============================================================================
# 📊 统计报表
# ============================================================================
def load_data():
    """加载数据"""
    if HABITS_FILE.exists():
        with open(HABITS_FILE, "r", encoding="utf-8") as f:
            habits_data = json.load(f)
    else:
        habits_data = {"habits": []}
    
    if ACHIEVEMENTS_FILE.exists():
        with open(ACHIEVEMENTS_FILE, "r", encoding="utf-8") as f:
            achievements_data = json.load(f)
    else:
        achievements_data = {"unlocked": []}
    
    return habits_data, achievements_data


def save_habits(data):
    """保存习惯数据"""
    with open(HABITS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_achievements(data):
    """保存成就数据"""
    with open(ACHIEVEMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_habit(name, reminder_time=None, frequency="daily"):
    """创建习惯"""
    habits_data, achievements_data = load_data()
    
    # 从库中获取模板信息
    template = HABIT_LIBRARY.get(name, {})
    
    habit = {
        "name": name,
        "category": template.get("category", "其他"),
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "reminder_time": reminder_time or template.get("default_time", "21:00"),
        "frequency": frequency or template.get("frequency", "daily"),
        "streak": 0,
        "total_checkins": 0,
        "checkins": [],
        "missed_days": [],
        "description": template.get("description", ""),
        "tips": template.get("tips", []),
        "milestones": template.get("milestones", [7, 21, 30, 60, 90, 100])
    }
    
    habits_data["habits"].append(habit)
    save_habits(habits_data)
    
    return habit


def checkin(habit_name):
    """打卡"""
    habits_data, achievements_data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    for habit in habits_data["habits"]:
        if habit_name in habit["name"]:
            # 检查是否已打卡
            if today in habit["checkins"]:
                return {"error": "今天已经打卡过了~", "streak": habit["streak"]}
            
            # 检查是否连续
            if habit["checkins"] and habit["checkins"][-1] == yesterday:
                habit["streak"] += 1
            elif habit["checkins"] and habit["checkins"][-1] != yesterday:
                # 中断后重新开始
                habit["streak"] = 1
                habit["missed_days"].append(yesterday)
            else:
                habit["streak"] = 1
            
            habit["checkins"].append(today)
            habit["total_checkins"] += 1
            
            save_habits(habits_data)
            
            # 检查成就
            new_achievements = check_achievements(habit["streak"], habit["total_checkins"])
            
            return {
                "success": True,
                "name": habit["name"],
                "streak": habit["streak"],
                "total": habit["total_checkins"],
                "category": habit["category"],
                "new_achievements": new_achievements
            }
    
    return {"error": "未找到该习惯，先创建一个吧~"}


def check_achievements(streak, total):
    """检查成就解锁"""
    habits_data, achievements_data = load_data()
    new_achievements = []
    
    # 连续成就
    for name, ach in ACHIEVEMENTS.items():
        if name not in achievements_data["unlocked"]:
            if "连续" in ach["desc"] or "打卡" not in ach["desc"]:
                if ach["condition"](streak):
                    achievements_data["unlocked"].append(name)
                    new_achievements.append({
                        "name": name,
                        "desc": ach["desc"],
                        "icon": ach["icon"]
                    })
            elif ach["condition"](total):
                achievements_data["unlocked"].append(name)
                new_achievements.append({
                    "name": name,
                    "desc": ach["desc"],
                    "icon": ach["icon"]
                })
    
    if new_achievements:
        save_achievements(achievements_data)
    
    return new_achievements


def get_stats(period="all"):
    """获取详细统计"""
    habits_data, achievements_data = load_data()
    now = datetime.now()
    
    # 计算时间范围
    if period == "week":
        start = now - timedelta(days=now.weekday())
    elif period == "month":
        start = now.replace(day=1)
    elif period == "year":
        start = now.replace(month=1, day=1)
    else:
        start = datetime.now() - timedelta(days=365)
    
    start_str = start.strftime("%Y-%m-%d")
    
    stats = {
        "summary": {
            "total_habits": len(habits_data["habits"]),
            "active_habits": 0,
            "total_checkins": 0,
            "total_streak": 0,
            "period_checkins": 0
        },
        "habits": [],
        "by_category": defaultdict(lambda: {"count": 0, "checkins": 0}),
        "achievements": len(achievements_data["unlocked"]),
        "weekly_trend": []
    }
    
    for habit in habits_data["habits"]:
        # 过滤周期内打卡
        period_checkins = [d for d in habit["checkins"] if d >= start_str]
        
        habit_stat = {
            "name": habit["name"],
            "category": habit["category"],
            "streak": habit["streak"],
            "total": habit["total_checkins"],
            "period": len(period_checkins),
            "completion_rate": round(len(period_checkins) / ((now - start).days + 1) * 100, 1) if period != "all" else 100,
            "created": habit["created_date"]
        }
        
        stats["habits"].append(habit_stat)
        stats["summary"]["total_checkins"] += habit["total_checkins"]
        stats["summary"]["period_checkins"] += len(period_checkins)
        stats["summary"]["total_streak"] += habit["streak"]
        
        if habit["streak"] > 0:
            stats["summary"]["active_habits"] += 1
        
        # 按分类统计
        cat = habit["category"]
        stats["by_category"][cat]["count"] += 1
        stats["by_category"][cat]["checkins"] += len(period_checkins)
    
    # 周趋势（最近 7 天）
    for i in range(6, -1, -1):
        date = (now - timedelta(days=i)).strftime("%Y-%m-%d")
        count = sum(1 for h in habits_data["habits"] if date in h["checkins"])
        stats["weekly_trend"].append({"date": date, "count": count})
    
    return stats


def generate_report(period="month"):
    """生成统计报告"""
    stats = get_stats(period)
    
    response = f"📊 **习惯统计报告** ({'本周' if period=='week' else '本月' if period=='month' else '本年'})\n\n"
    
    # 总览
    response += "📈 **总览**\n"
    response += f"- 习惯总数：{stats['summary']['total_habits']} 个\n"
    response += f"- 活跃习惯：{stats['summary']['active_habits']} 个\n"
    response += f"- 总打卡次数：{stats['summary']['total_checkins']} 次\n"
    response += f"- 周期打卡：{stats['summary']['period_checkins']} 次\n"
    response += f"- 解锁成就：{stats['achievements']} 个\n\n"
    
    # 按分类
    response += "📂 **按分类**\n"
    for cat, data in sorted(stats["by_category"].items(), key=lambda x: x[1]["checkins"], reverse=True):
        response += f"- {cat}: {data['count']}个习惯，{data['checkins']}次打卡\n"
    response += "\n"
    
    # 习惯详情
    response += "📋 **习惯详情**\n"
    for h in sorted(stats["habits"], key=lambda x: x["streak"], reverse=True):
        bar_len = int(h["completion_rate"] / 10)
        bar = "█" * bar_len + "░" * (10 - bar_len)
        response += f"\n**{h['name']}** ({h['category']})\n"
        response += f"  🔥 连续：{h['streak']}天 | 📊 总计：{h['total']}次\n"
        response += f"  📈 完成率：[{bar}] {h['completion_rate']}%\n"
    
    return response


def get_habit_list():
    """获取习惯库列表"""
    response = "📚 **习惯库**\n\n"
    
    categories = defaultdict(list)
    for name, info in HABIT_LIBRARY.items():
        categories[info["category"]].append((name, info))
    
    for cat, habits in sorted(categories.items()):
        response += f"**{cat}**\n"
        for name, info in habits:
            response += f"- {name}: {info['description']}\n"
        response += "\n"
    
    return response


def get_achievements_list():
    """获取成就列表"""
    habits_data, achievements_data = load_data()
    
    response = "🏆 **成就系统**\n\n"
    response += f"已解锁：{len(achievements_data['unlocked'])}/{len(ACHIEVEMENTS)}\n\n"
    
    for name, ach in ACHIEVEMENTS.items():
        icon = ach["icon"]
        status = "✅" if name in achievements_data["unlocked"] else "🔒"
        response += f"{status} {icon} **{name}**: {ach['desc']}\n"
    
    return response


def checkin_all():
    """一键打卡所有习惯"""
    habits_data, _ = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    
    results = []
    for habit in habits_data["habits"]:
        if today not in habit["checkins"]:
            habit["checkins"].append(today)
            habit["total_checkins"] += 1
            habit["streak"] += 1
            results.append(habit["name"])
    
    save_habits(habits_data)
    return results


# ============================================================================
# 🎯 主函数
# ============================================================================
def main(query):
    """主函数"""
    query_lower = query.lower()
    
    # 创建习惯
    if "创建" in query_lower or "开始" in query_lower or "养成" in query_lower:
        for habit_name in HABIT_LIBRARY.keys():
            if habit_name in query_lower:
                habit = create_habit(habit_name)
                return f"""✅ 习惯已创建！

📚 **{habit['name']}**
📂 分类：{habit['category']}
📝 说明：{habit['description']}
⏰ 提醒：{habit['reminder_time']}
💡 建议：{', '.join(habit['tips'][:3])}

回复"打卡{habit_name}"开始打卡！👻"""
        
        # 未知习惯，显示库
        return "📚  habit 库中没有这个习惯~\n\n" + get_habit_list()
    
    # 打卡
    if "打卡" in query_lower:
        if "全部" in query_lower or "所有" in query_lower:
            results = checkin_all()
            if results:
                return f"✅ 一键打卡完成！\n\n已打卡：{', '.join(results)}\n共 {len(results)} 个习惯"
            else:
                return "✅ 所有习惯今天都已打卡！"
        
        for habit_name in HABIT_LIBRARY.keys():
            if habit_name in query_lower:
                result = checkin(habit_name)
                if result.get("error"):
                    return f"❌ {result['error']}"
                
                response = f"""✅ 打卡成功！

📚 **{result['name']}** ({result['category']})
🔥 连续打卡：{result['streak']}天
📊 总打卡：{result['total']}次
"""
                if result.get("new_achievements"):
                    response += "\n🏆 **解锁成就**:\n"
                    for ach in result["new_achievements"]:
                        response += f"  {ach['icon']} {ach['name']}: {ach['desc']}\n"
                
                response += "\n💪 加油！坚持就是胜利！"
                return response
        
        return "❌ 未找到该习惯，先创建一个吧~"
    
    # 统计
    if "统计" in query_lower or "报告" in query_lower or "查看" in query_lower:
        period = "month"
        if "周" in query_lower: period = "week"
        elif "年" in query_lower: period = "year"
        elif "全部" in query_lower: period = "all"
        
        return generate_report(period)
    
    # 成就
    if "成就" in query_lower or "徽章" in query_lower:
        return get_achievements_list()
    
    # 习惯库
    if "习惯库" in query_lower or "有哪些习惯" in query_lower:
        return get_habit_list()
    
    # 删除习惯
    if "删除" in query_lower or "取消" in query_lower:
        habits_data, _ = load_data()
        for habit_name in HABIT_LIBRARY.keys():
            if habit_name in query_lower:
                habits_data["habits"] = [h for h in habits_data["habits"] if habit_name not in h["name"]]
                save_habits(habits_data)
                return f"✅ 已删除习惯：{habit_name}"
        return "❌ 未找到该习惯"
    
    # 默认回复
    return """🎯 习惯养成助手 v2.0

**功能**：
1. 创建习惯 - "我想养成每天读书的习惯"
2. 每日打卡 - "打卡读书"、"打卡全部"
3. 查看统计 - "查看习惯统计"、"本周报告"
4. 成就系统 - "查看我的成就"
5. 习惯库 - "有哪些习惯"

**习惯分类**：
- 健康：运动、早睡早起、健康饮食、喝水、冥想
- 学习：读书、学英语、编程、写日记、乐器
- 工作：今日事今日毕、时间管理、深度工作、周复盘
- 生活：整理房间、记账、陪家人、晒太阳、微笑
- 社交：社交拓展、感恩打卡

**成就系统**：从🌱初出茅庐到👑百日战神，共 10 个成就等你解锁！

告诉我你想养成什么习惯？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(main("查看习惯统计"))
