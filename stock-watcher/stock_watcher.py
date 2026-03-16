#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📈 Stock Watcher - 股票观察助手
功能：股价查询、自选股管理、价格提醒
"""

import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent
WATCHLIST_FILE = DATA_DIR / "watchlist.json"

# 示例股票数据
STOCKS = {
    "600519": {"name": "贵州茅台", "price": 1680.00, "change": 0.90},
    "00700": {"name": "腾讯控股", "price": 350.00, "change": 1.20},
    "AAPL": {"name": "苹果", "price": 175.00, "change": -0.50},
    "TSLA": {"name": "特斯拉", "price": 250.00, "change": 2.30},
}


def load_watchlist():
    """加载自选股"""
    if WATCHLIST_FILE.exists():
        with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"watchlist": []}


def save_watchlist(data):
    """保存自选股"""
    with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_stock_price(symbol):
    """获取股价"""
    return STOCKS.get(symbol)


def add_to_watchlist(symbol):
    """添加到自选"""
    data = load_watchlist()
    
    if symbol not in [s["symbol"] for s in data["watchlist"]]:
        stock = get_stock_price(symbol)
        if stock:
            data["watchlist"].append({
                "symbol": symbol,
                "name": stock["name"],
                "added_date": datetime.now().strftime("%Y-%m-%d")
            })
            save_watchlist(data)
            return True
    return False


def format_stock(symbol, stock):
    """格式化股票信息"""
    change_icon = "🔴" if stock["change"] >= 0 else "🟢"
    return f"{symbol} {stock['name']} ¥{stock['price']} {change_icon} {stock['change']:+.2f}%"


def main(query):
    """主函数"""
    query = query.lower()
    
    # 查询股价
    for symbol, stock in STOCKS.items():
        if symbol in query or stock["name"] in query:
            return format_stock(symbol, stock)
    
    # 添加自选
    if "添加" in query or "自选" in query:
        for symbol in STOCKS.keys():
            if symbol in query:
                if add_to_watchlist(symbol):
                    return f"✅ 已添加 {symbol} 到自选股"
    
    # 查看自选
    if "自选" in query and "列表" in query:
        data = load_watchlist()
        if not data["watchlist"]:
            return "📈 暂无自选股"
        
        response = "📈 **自选股列表**：\n\n"
        for s in data["watchlist"]:
            stock = get_stock_price(s["symbol"])
            if stock:
                response += format_stock(s["symbol"], stock) + "\n"
        return response
    
    # 默认回复
    return """📈 股票观察助手

**功能**：
1. 股价查询 - "查询贵州茅台股价"
2. 自选股管理 - "添加茅台到自选"
3. 查看自选 - "我的自选股列表"

**支持**：A 股、港股、美股

告诉我你想查哪只股票？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(main("查询贵州茅台"))
