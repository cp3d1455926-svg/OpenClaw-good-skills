#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💰 Expense Tracker v2.0 - 记账助手
功能：记账、分类统计、预算管理、消费分析、储蓄目标、账单提醒
代码量：~14KB
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

DATA_DIR = Path(__file__).parent
TRANSACTIONS_FILE = DATA_DIR / "transactions.json"
BUDGET_FILE = DATA_DIR / "budget.json"
SAVINGS_FILE = DATA_DIR / "savings.json"

# ============================================================================
# 📊 消费分类体系（20+ 子分类）
# ============================================================================
CATEGORIES = {
    "餐饮": {
        "icon": "🍜",
        "subcategories": ["早餐", "午餐", "晚餐", "外卖", "咖啡奶茶", "零食", "聚餐"],
        "monthly_avg": 1500
    },
    "交通": {
        "icon": "🚗",
        "subcategories": ["地铁公交", "打车", "加油", "停车", "保养", "保险"],
        "monthly_avg": 500
    },
    "购物": {
        "icon": "🛍️",
        "subcategories": ["衣服", "鞋子", "数码", "日用品", "化妆品", "家居"],
        "monthly_avg": 1000
    },
    "娱乐": {
        "icon": "🎬",
        "subcategories": ["电影", "游戏", "聚会", "KTV", "运动", "演出"],
        "monthly_avg": 500
    },
    "居住": {
        "icon": "🏠",
        "subcategories": ["房租", "水电", "物业", "网费", "维修", "清洁"],
        "monthly_avg": 3000
    },
    "医疗": {
        "icon": "🏥",
        "subcategories": ["看病", "买药", "体检", "保健品", "健身"],
        "monthly_avg": 300
    },
    "学习": {
        "icon": "📚",
        "subcategories": ["书籍", "课程", "培训", "考试", "订阅"],
        "monthly_avg": 500
    },
    "人情": {
        "icon": "🧧",
        "subcategories": ["红包", "礼物", "请客", "捐款"],
        "monthly_avg": 500
    },
    "通讯": {
        "icon": "📱",
        "subcategories": ["话费", "流量", "宽带"],
        "monthly_avg": 200
    },
    "其他": {
        "icon": "📦",
        "subcategories": ["杂项"],
        "monthly_avg": 500
    }
}

# ============================================================================
# 💡 消费提示库
# ============================================================================
SPENDING_TIPS = {
    "餐饮": [
        "自己做饭比外卖省 50%",
        "办张公司附近餐厅会员卡",
        "少喝奶茶，一个月省 300 元"
    ],
    "购物": [
        "等 3 天再买，可能就不想买了",
        "比价后再下单",
        "二手平台淘好物"
    ],
    "娱乐": [
        "找免费活动替代",
        "办年卡更划算",
        "和朋友 AA 聚餐"
    ],
    "交通": [
        "地铁比打车便宜 80%",
        "共享单车月卡很划算",
        "拼车省油费"
    ]
}

# ============================================================================
# 🎯 储蓄目标模板
# ============================================================================
SAVINGS_GOALS = {
    "应急基金": {
        "desc": "6 个月生活费",
        "default_amount": 30000,
        "priority": "high"
    },
    "旅行基金": {
        "desc": "年度旅行",
        "default_amount": 10000,
        "priority": "medium"
    },
    "购房首付": {
        "desc": "买房首付",
        "default_amount": 500000,
        "priority": "high"
    },
    "购车计划": {
        "desc": "买车",
        "default_amount": 100000,
        "priority": "medium"
    },
    "教育基金": {
        "desc": "进修学习",
        "default_amount": 50000,
        "priority": "medium"
    },
    "创业基金": {
        "desc": "创业启动金",
        "default_amount": 200000,
        "priority": "low"
    }
}

# ============================================================================
# 📈 分析报表
# ============================================================================
def load_data():
    """加载数据"""
    if TRANSACTIONS_FILE.exists():
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            transactions = json.load(f)
    else:
        transactions = {"transactions": []}
    
    if BUDGET_FILE.exists():
        with open(BUDGET_FILE, "r", encoding="utf-8") as f:
            budget = json.load(f)
    else:
        budget = {
            "monthly_limit": 5000,
            "category_limits": {cat: info["monthly_avg"] for cat, info in CATEGORIES.items()}
        }
    
    if SAVINGS_FILE.exists():
        with open(SAVINGS_FILE, "r", encoding="utf-8") as f:
            savings = json.load(f)
    else:
        savings = {"goals": []}
    
    return transactions, budget, savings


def save_transactions(data):
    """保存交易数据"""
    with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_budget(data):
    """保存预算数据"""
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_savings(data):
    """保存储蓄数据"""
    with open(SAVINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_transaction(amount, category, note="", date=None, trans_type="expense", subcategory=None):
    """添加账单"""
    data, budget, savings = load_data()
    
    # 自动识别分类
    if category == "auto":
        category = auto_categorize(note)
    
    transaction = {
        "id": f"tx_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "type": trans_type,
        "amount": amount,
        "category": category,
        "subcategory": subcategory or "",
        "note": note,
        "date": date or datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M")
    }
    
    data["transactions"].append(transaction)
    save_transactions(data)
    
    # 检查预算
    warning = check_budget_warning(category, amount)
    
    return {"transaction": transaction, "warning": warning}


def auto_categorize(note):
    """自动分类"""
    note_lower = note.lower()
    
    for cat, info in CATEGORIES.items():
        keywords = info["subcategories"] + [cat]
        for kw in keywords:
            if kw in note_lower:
                return cat
    
    return "其他"


def check_budget_warning(category, amount):
    """预算预警"""
    data, budget, _ = load_data()
    now = datetime.now()
    month_start = now.replace(day=1).strftime("%Y-%m-%d")
    
    # 计算本月该分类已花费
    month_spending = sum(
        t["amount"] for t in data["transactions"]
        if t["type"] == "expense" and t["category"] == category and t["date"] >= month_start
    )
    
    # 加上本次消费
    total = month_spending + amount
    limit = budget["category_limits"].get(category, 1000)
    
    if total > limit:
        return {
            "warning": True,
            "message": f"⚠️ {category} 预算超支！已花¥{total}/限额¥{limit}",
            "spent": total,
            "limit": limit,
            "over": total - limit
        }
    
    if total > limit * 0.8:
        return {
            "warning": True,
            "message": f"⚠️ {category} 预算即将用完！已花¥{total}/限额¥{limit} (80%)",
            "spent": total,
            "limit": limit,
            "over": 0
        }
    
    return None


def get_stats(period="month"):
    """获取详细统计"""
    data, budget, savings = load_data()
    transactions = data["transactions"]
    now = datetime.now()
    
    # 计算时间范围
    if period == "month":
        start = now.replace(day=1)
    elif period == "week":
        start = now - timedelta(days=now.weekday())
    elif period == "year":
        start = now.replace(month=1, day=1)
    else:
        start = now - timedelta(days=30)
    
    start_str = start.strftime("%Y-%m-%d")
    
    # 筛选交易
    filtered = [t for t in transactions if t["date"] >= start_str]
    
    # 收支统计
    total_expense = sum(t["amount"] for t in filtered if t["type"] == "expense")
    total_income = sum(t["amount"] for t in filtered if t["type"] == "income")
    
    # 分类统计
    by_category = defaultdict(lambda: {"amount": 0, "count": 0, "items": []})
    for t in filtered:
        if t["type"] == "expense":
            cat = t["category"]
            by_category[cat]["amount"] += t["amount"]
            by_category[cat]["count"] += 1
            by_category[cat]["items"].append(t)
    
    # 每日趋势
    daily_stats = defaultdict(lambda: {"expense": 0, "income": 0})
    for t in filtered:
        if t["type"] == "expense":
            daily_stats[t["date"]]["expense"] += t["amount"]
        else:
            daily_stats[t["date"]]["income"] += t["amount"]
    
    # 预算执行率
    budget_usage = {}
    for cat, info in by_category.items():
        limit = budget["category_limits"].get(cat, 1000)
        budget_usage[cat] = {
            "spent": info["amount"],
            "limit": limit,
            "usage": round(info["amount"] / limit * 100, 1) if limit > 0 else 0
        }
    
    return {
        "period": period,
        "start_date": start_str,
        "end_date": now.strftime("%Y-%m-%d"),
        "expense": total_expense,
        "income": total_income,
        "balance": total_income - total_expense,
        "by_category": dict(by_category),
        "daily_trend": dict(daily_stats),
        "budget_usage": budget_usage,
        "monthly_limit": budget["monthly_limit"],
        "budget_remaining": budget["monthly_limit"] - total_expense,
        "savings_goals": savings.get("goals", [])
    }


def format_stats(stats):
    """格式化统计报表"""
    period_name = {"week": "本周", "month": "本月", "year": "本年"}.get(stats["period"], "近 30 天")
    
    response = f"📊 **消费统计** ({period_name})\n"
    response += f"📅 {stats['start_date']} ~ {stats['end_date']}\n\n"
    
    # 总览
    response += "💰 **总览**\n"
    response += f"- 总收入：¥{stats['income']}\n"
    response += f"- 总支出：¥{stats['expense']}\n"
    response += f"- 结余：¥{stats['balance']}\n"
    response += f"- 预算：¥{stats['monthly_limit']}\n"
    response += f"- 预算剩余：¥{stats['budget_remaining']}\n\n"
    
    # 分类统计
    if stats["by_category"]:
        response += "📋 **分类统计**\n"
        sorted_cats = sorted(stats["by_category"].items(), key=lambda x: x[1]["amount"], reverse=True)
        
        for cat, info in sorted_cats:
            icon = CATEGORIES.get(cat, {}).get("icon", "📦")
            amount = info["amount"]
            count = info["count"]
            percent = round(amount / stats["expense"] * 100, 1) if stats["expense"] > 0 else 0
            
            # 预算进度条
            budget_info = stats["budget_usage"].get(cat, {})
            usage = budget_info.get("usage", 0)
            bar_len = min(10, int(usage / 10))
            bar = "█" * bar_len + "░" * (10 - bar_len)
            over = "⚠️ 超支" if usage > 100 else ""
            
            response += f"\n{icon} **{cat}**: ¥{amount} ({percent}%) {over}\n"
            response += f"   预算：[{bar}] {usage}% | {count}笔\n"
    
    # 储蓄目标
    if stats["savings_goals"]:
        response += "\n🎯 **储蓄目标**\n"
        for goal in stats["savings_goals"]:
            progress = round(goal["current"] / goal["target"] * 100, 1)
            bar_len = min(10, int(progress / 10))
            bar = "█" * bar_len + "░" * (10 - bar_len)
            response += f"- {goal['name']}: ¥{goal['current']}/¥{goal['target']} [{bar}] {progress}%\n"
    
    return response


def format_analysis(stats):
    """生成消费分析"""
    response = "🔍 **消费分析**\n\n"
    
    # 找出最大支出分类
    if stats["by_category"]:
        top_cat = max(stats["by_category"].items(), key=lambda x: x[1]["amount"])
        response += f"💡 **最大支出**: {top_cat[0]} (¥{top_cat[1]['amount']})\n\n"
        
        # 给出建议
        if top_cat[0] in SPENDING_TIPS:
            response += f"💰 **省钱建议**:\n"
            for tip in SPENDING_TIPS[top_cat[0]][:3]:
                response += f"- {tip}\n"
    
    # 日均消费
    days = (datetime.strptime(stats["end_date"], "%Y-%m-%d") - 
            datetime.strptime(stats["start_date"], "%Y-%m-%d")).days + 1
    daily_avg = round(stats["expense"] / days, 1) if days > 0 else 0
    response += f"\n📈 **日均消费**: ¥{daily_avg}\n"
    
    # 预算预警
    over_budget = [cat for cat, info in stats["budget_usage"].items() if info["usage"] > 100]
    if over_budget:
        response += f"\n⚠️ **预算超支**: {', '.join(over_budget)}\n"
    
    return response


def create_savings_goal(name, target_amount, current=0):
    """创建储蓄目标"""
    _, _, savings = load_data()
    
    goal = {
        "name": name,
        "target": target_amount,
        "current": current,
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "monthly_target": round((target_amount - current) / 12, 2)
    }
    
    savings["goals"].append(goal)
    save_savings(savings)
    
    return goal


def update_savings(goal_name, amount):
    """更新储蓄进度"""
    _, _, savings = load_data()
    
    for goal in savings["goals"]:
        if goal_name in goal["name"]:
            goal["current"] += amount
            return goal
    
    return None


def get_budget_report():
    """生成预算报告"""
    stats = get_stats("month")
    
    response = "💰 **预算执行报告**\n\n"
    response += f"月度总预算：¥{stats['monthly_limit']}\n"
    response += f"已使用：¥{stats['expense']}\n"
    response += f"剩余：¥{stats['budget_remaining']}\n"
    response += f"执行率：{round(stats['expense']/stats['monthly_limit']*100, 1)}%\n\n"
    
    # 分类预算
    response += "📋 **分类预算**\n"
    for cat, info in sorted(stats["budget_usage"].items(), key=lambda x: x[1]["usage"], reverse=True):
        icon = CATEGORIES.get(cat, {}).get("icon", "📦")
        status = "✅" if info["usage"] <= 80 else "⚠️" if info["usage"] <= 100 else "❌"
        response += f"{status} {icon} {cat}: ¥{info['spent']}/¥{info['limit']} ({info['usage']}%)\n"
    
    return response


def get_category_list():
    """获取分类列表"""
    response = "📊 **消费分类**\n\n"
    for cat, info in CATEGORIES.items():
        response += f"{info['icon']} **{cat}**: {', '.join(info['subcategories'][:5])}\n"
    return response


def get_savings_goals():
    """获取储蓄目标"""
    _, _, savings = load_data()
    
    if not savings["goals"]:
        return "🎯 暂无储蓄目标\n\n可用模板：应急基金、旅行基金、购房首付、购车计划、教育基金、创业基金"
    
    response = "🎯 **储蓄目标**\n\n"
    for goal in savings["goals"]:
        progress = round(goal["current"] / goal["target"] * 100, 1)
        response += f"- {goal['name']}: ¥{goal['current']}/¥{goal['target']} ({progress}%)\n"
        response += f"  每月需存：¥{goal['monthly_target']}\n"
    
    return response


# ============================================================================
# 🎯 主函数
# ============================================================================
def main(query):
    """主函数"""
    query_lower = query.lower()
    
    # 记账
    if "花了" in query_lower or "支出" in query_lower or "收入" in query_lower or "赚了" in query_lower:
        trans_type = "income" if any(k in query_lower for k in ["收入", "赚了", "工资", "奖金"]) else "expense"
        
        amount_match = re.search(r'(\d+) 元', query_lower)
        if amount_match:
            amount = int(amount_match.group(1))
            
            # 自动分类
            category = "auto"
            for cat in CATEGORIES.keys():
                if cat in query_lower:
                    category = cat
                    break
            
            result = add_transaction(amount, category, query_lower, trans_type=trans_type)
            
            icon = CATEGORIES.get(result["transaction"]["category"], {}).get("icon", "📦")
            type_text = "收入" if trans_type == "income" else "支出"
            
            response = f"✅ 已记录{type_text} {icon} ¥{amount}（{result['transaction']['category']}）"
            
            if result.get("warning"):
                response += f"\n\n{result['warning']['message']}"
            
            return response
    
    # 统计
    if "统计" in query_lower or "花了多少钱" in query_lower or "报表" in query_lower:
        period = "month"
        if "周" in query_lower: period = "week"
        elif "年" in query_lower: period = "year"
        
        stats = get_stats(period)
        response = format_stats(stats)
        
        if "分析" in query_lower:
            response += "\n" + format_analysis(stats)
        
        return response
    
    # 预算
    if "预算" in query_lower:
        if "设置" in query_lower:
            amount_match = re.search(r'(\d+)', query_lower)
            if amount_match:
                _, budget, _ = load_data()
                budget["monthly_limit"] = int(amount_match.group(1))
                save_budget(budget)
                return f"✅ 月度预算已设置为 ¥{budget['monthly_limit']}"
        
        return get_budget_report()
    
    # 储蓄目标
    if "储蓄" in query_lower or "存款" in query_lower or "攒钱" in query_lower:
        if "创建" in query_lower or "目标" in query_lower:
            for goal_name, info in SAVINGS_GOALS.items():
                if goal_name in query_lower:
                    goal = create_savings_goal(goal_name, info["default_amount"])
                    return f"✅ 储蓄目标已创建！\n\n🎯 {goal['name']}\n目标：¥{goal['target']}\n每月需存：¥{goal['monthly_target']}"
            
            return "🎯 可用储蓄目标模板：\n" + "\n".join(f"- {k}: {v['desc']} (¥{v['default_amount']})" for k, v in SAVINGS_GOALS.items())
        
        if "更新" in query_lower:
            amount_match = re.search(r'(\d+)', query_lower)
            if amount_match:
                for goal_name in SAVINGS_GOALS.keys():
                    if goal_name in query_lower:
                        goal = update_savings(goal_name, int(amount_match.group(1)))
                        if goal:
                            return f"✅ 已更新{goal['name']}：¥{goal['current']}/¥{goal['target']}"
        
        return get_savings_goals()
    
    # 分类列表
    if "分类" in query_lower or "有哪些" in query_lower:
        return get_category_list()
    
    # 分析
    if "分析" in query_lower:
        stats = get_stats("month")
        return format_analysis(stats)
    
    # 默认回复
    return """💰 记账助手 v2.0

**功能**：
1. 记账 - "今天花了 50 元吃饭"、"工资收入 10000 元"
2. 统计 - "这个月花了多少钱"、"本周统计"、"年度报表"
3. 预算 - "设置每月预算 5000 元"、"查看预算"
4. 储蓄 - "创建应急基金"、"更新储蓄目标"
5. 分析 - "消费分析"

**消费分类**：
🍜 餐饮 | 🚗 交通 | 🛍️ 购物 | 🎬 娱乐 | 🏠 居住
🏥 医疗 | 📚 学习 | 🧧 人情 | 📱 通讯 | 📦 其他

**储蓄目标**：应急基金、旅行基金、购房首付、购车计划、教育基金、创业基金

**特色功能**：
- 自动分类识别
- 预算超支预警
- 消费分析建议
- 储蓄进度追踪

告诉我你想记什么账？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(main("这个月花了多少钱"))
