#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍳 Recipe Finder - 菜谱助手
功能：食材推荐菜谱、菜谱详情、营养分析
"""

import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent
FAVORITES_FILE = DATA_DIR / "favorites.json"

# 示例菜谱数据库
RECIPES = {
    "家常菜": [
        {
            "name": "番茄炒蛋",
            "difficulty": 1,
            "time": 10,
            "ingredients": ["番茄", "鸡蛋", "葱花"],
            "steps": [
                "番茄切块，鸡蛋打散",
                "热锅凉油，炒鸡蛋盛出",
                "炒番茄出汁",
                "加入鸡蛋翻炒",
                "加盐、糖调味",
                "撒葱花出锅"
            ],
            "tips": "鸡蛋加少许水更嫩",
            "calories": 200
        },
        {
            "name": "宫保鸡丁",
            "difficulty": 3,
            "time": 20,
            "ingredients": ["鸡胸肉", "花生", "干辣椒", "葱姜蒜"],
            "steps": [
                "鸡肉切丁，腌制",
                "花生炸香",
                "炒香干辣椒",
                "下鸡丁翻炒",
                "加调料",
                "出锅前加花生"
            ],
            "tips": "鸡肉用淀粉腌制更嫩",
            "calories": 350
        },
        {
            "name": "红烧肉",
            "difficulty": 4,
            "time": 60,
            "ingredients": ["五花肉", "冰糖", "料酒", "生抽", "八角"],
            "steps": [
                "五花肉切块焯水",
                "炒糖色",
                "下肉块翻炒",
                "加调料和水",
                "小火炖 40 分钟",
                "大火收汁"
            ],
            "tips": "炒糖色不要炒糊",
            "calories": 500
        },
        {
            "name": "土豆烧牛肉",
            "difficulty": 3,
            "time": 40,
            "ingredients": ["牛肉", "土豆", "胡萝卜", "葱姜"],
            "steps": [
                "牛肉切块焯水",
                "土豆胡萝卜切块",
                "炒香牛肉",
                "加水炖 20 分钟",
                "加土豆胡萝卜",
                "再炖 15 分钟"
            ],
            "tips": "牛肉选牛腩更好吃",
            "calories": 400
        }
    ],
    "汤类": [
        {
            "name": "番茄蛋花汤",
            "difficulty": 1,
            "time": 10,
            "ingredients": ["番茄", "鸡蛋", "葱花"],
            "steps": [
                "番茄切块",
                "水烧开下番茄",
                "淋入蛋液",
                "加盐调味",
                "撒葱花"
            ],
            "tips": "蛋液要慢慢淋",
            "calories": 100
        }
    ],
    "素食": [
        {
            "name": "麻婆豆腐",
            "difficulty": 2,
            "time": 15,
            "ingredients": ["豆腐", "豆瓣酱", "花椒", "葱姜蒜"],
            "steps": [
                "豆腐切块焯水",
                "炒香豆瓣酱",
                "下豆腐",
                "加水煮",
                "勾芡",
                "撒花椒粉"
            ],
            "tips": "豆腐焯水去腥",
            "calories": 250
        }
    ]
}

# 食材匹配
INGREDIENT_MAP = {
    "番茄": ["番茄炒蛋", "番茄蛋花汤"],
    "鸡蛋": ["番茄炒蛋", "番茄蛋花汤"],
    "土豆": ["土豆烧牛肉"],
    "牛肉": ["土豆烧牛肉"],
    "豆腐": ["麻婆豆腐"],
    "鸡肉": ["宫保鸡丁"],
    "猪肉": ["红烧肉"]
}


def load_favorites():
    """加载收藏"""
    if FAVORITES_FILE.exists():
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"favorites": []}


def save_favorites(data):
    """保存收藏"""
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def recommend_by_ingredients(ingredients):
    """根据食材推荐"""
    results = []
    for ing in ingredients:
        if ing in INGREDIENT_MAP:
            results.extend(INGREDIENT_MAP[ing])
    
    # 去重
    return list(set(results))


def get_recipe_detail(name):
    """获取菜谱详情"""
    for category, recipes in RECIPES.items():
        for recipe in recipes:
            if recipe["name"] == name:
                return recipe
    return None


def format_recipe(recipe):
    """格式化菜谱"""
    difficulty = "⭐" * recipe["difficulty"]
    
    response = f"🍳 **{recipe['name']}**\n\n"
    response += f"难度：{difficulty}\n"
    response += f"时间：{recipe['time']}分钟\n"
    response += f"热量：{recipe['calories']}卡\n\n"
    
    response += "📝 **食材**：\n"
    response += "、".join(recipe["ingredients"]) + "\n\n"
    
    response += "👨‍🍳 **步骤**：\n"
    for i, step in enumerate(recipe["steps"], 1):
        response += f"{i}. {step}\n"
    
    response += f"\n💡 **技巧**：{recipe['tips']}\n"
    
    return response


def main(query):
    """主函数"""
    query = query.lower()
    
    # 推荐菜谱
    if "推荐" in query or "吃什么" in query:
        response = "🍳 **今日推荐菜谱**：\n\n"
        count = 0
        for category, recipes in RECIPES.items():
            for recipe in recipes[:2]:
                response += f"{count+1}. {recipe['name']} (难度：{'⭐'*recipe['difficulty']}, 时间：{recipe['time']}分钟)\n"
                count += 1
                if count >= 5:
                    break
            if count >= 5:
                break
        return response
    
    # 根据食材推荐
    if "我有" in query or "食材" in query:
        ingredients = []
        for ing in INGREDIENT_MAP.keys():
            if ing in query:
                ingredients.append(ing)
        
        if ingredients:
            results = recommend_by_ingredients(ingredients)
            response = f"🥔 用{','.join(ingredients)}可以做：\n\n"
            for name in results[:5]:
                recipe = get_recipe_detail(name)
                if recipe:
                    response += f"- {name} ({recipe['time']}分钟)\n"
            return response
    
    # 查询菜谱详情
    for category, recipes in RECIPES.items():
        for recipe in recipes:
            if recipe["name"] in query:
                return format_recipe(recipe)
    
    # 默认回复
    return """🍳 菜谱助手

**功能**：
1. 推荐菜谱 - "今天吃什么"
2. 食材推荐 - "我有土豆和牛肉"
3. 菜谱详情 - "怎么做番茄炒蛋"

**菜系**：家常菜、汤类、素食

告诉我你想吃什么？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(main("今天吃什么"))
