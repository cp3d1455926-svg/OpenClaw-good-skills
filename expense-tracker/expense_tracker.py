#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💰 Expense Tracker - 记账助手
功能：记账、统计、预算管理
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).parent
TRANSACTIONS_FILE = DATA_DIR / "transactions.json"

# 消费分类
CATEGORIES = {
    "餐饮": ["吃饭", "外卖", "咖啡", "奶茶"],
    "交通": ["地铁", "公交", "打车", "加油"],
    "购物": ["衣服", "日用品", "数码"],
    "娱乐": ["电影", "游戏", "聚会"],
    "居住": ["房租", "水电", "物业"],
    "医疗": ["看病", "买药"],
    "学习": ["书籍", "课程"],
    "其他": []
}


def load_data():
    """加载数据"""
    if TRANSACTIONS_FILE.exists():
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "transactions": [],
        "budget": {"monthly": 5000, "categories": {}}
    }


def save_data(data):
    """保存数据"""
    with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_transaction(amount, category, note="", date=None, trans_type="expense"):
    """添加账单"""
    data = load_data()
    
    transaction = {
        "type": trans_type,
        "amount": amount,
        "category": category,
        "note": note,
        "date": date or datetime.now().strftime("%Y-%m-%d")
    }
    
    data["transactions"].append(transaction)
    save_data(data)
    
    return transaction


def get_stats(period="month"):
    """获取统计"""
    data = load_data()
    transactions = data["transactions"]
    
    now = datetime.now()
    
    if period == "month":
        start = now.replace(day=1)
    elif period == "week":
        start = now - timedelta(days=now.weekday())
    else:
        start = now - timedelta(days=30)
    
    # 筛选
    filtered = [t for t in transactions if datetime.strptime(t["date"], "%Y-%m-%d") >= start]
    
    # 统计
    total_expense = sum(t["amount"] for t in filtered if t["type"] == "expense")
    total_income = sum(t["amount"] for t in filtered if t["type"] == "income")
    
    # 分类统计
    by_category = {}
    for t in filtered:
        if t["type"] == "expense":
            cat = t["category"]
            by_category[cat] = by_category.get(cat, 0) + t["amount"]
    
    return {
        "expense": total_expense,
        "income": total_income,
        "by_category": by_category,
        "budget": data["budget"]["monthly"]
    }


def format_stats(stats):
    """格式化统计"""
    response = f"📊 **消费统计**\n\n"
    response += f"💰 总支出：¥{stats['expense']}\n"
    response += f"📈 收入：¥{stats['income']}\n"
    response += f"✅ 预算：¥{stats['budget']}\n"
    response += f"💵 剩余：¥{stats['budget'] - stats['expense']}\n\n"
    
    if stats["by_category"]:
        response += "📋 **分类统计**：\n"
        for cat, amount in sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True):
            percent = amount / stats["expense"] * 100 if stats["expense"] > 0 else 0
            response += f"- {cat}：¥{amount} ({percent:.0f}%)\n"
    
    return response


def main(query):
    """主函数"""
    query = query.lower()
    
    # 记账
    if "花了" in query or "支出" in query:
        import re
        amount_match = re.search(r'(\d+) 元', query)
        if amount_match:
            amount = int(amount_match.group(1))
            # 自动分类
            category = "其他"
            for cat, keywords in CATEGORIES.items():
                for kw in keywords:
                    if kw in query:
                        category = cat
                        break
            
            add_transaction(amount, category)
            return f"✅ 已记录支出 ¥{amount}（{category}）"
    
    # 统计
    if "统计" in query or "花了多少钱" in query or "预算" in query:
        stats = get_stats()
        return format_stats(stats)
    
    # 设置预算
    if "预算" in query and "设置" in query:
        import re
        amount_match = re.search(r'(\d+)', query)
        if amount_match:
            data = load_data()
            data["budget"]["monthly"] = int(amount_match.group(1))
            save_data(data)
            return f"✅ 预算已设置为 ¥{data['budget']['monthly']}"
    
    # 默认回复
    return """💰 记账助手

**功能**：
1. 记账 - "今天花了 50 元吃饭"
2. 统计 - "这个月花了多少钱"
3. 预算 - "设置每月预算 5000 元"

**分类**：餐饮、交通、购物、娱乐、居住、医疗、学习、其他

告诉我你想记什么账？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(main("这个月花了多少钱"))
