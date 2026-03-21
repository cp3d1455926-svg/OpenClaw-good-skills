#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✈️ Travel Planner v2.0 - 旅行规划助手
功能：行程规划、景点推荐、预算估算、打包清单、旅行模板
代码量：~15KB
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).parent
TRIPS_FILE = DATA_DIR / "trips.json"

# ============================================================================
# 🌍 目的地数据库（10+ 城市）
# ============================================================================
DESTINATIONS = {
    "北京": {
        "attractions": [
            {"name": "故宫", "time": "4 小时", "price": 60, "area": "东城", "type": "历史"},
            {"name": "天安门广场", "time": "2 小时", "price": 0, "area": "东城", "type": "地标"},
            {"name": "颐和园", "time": "4 小时", "price": 30, "area": "海淀", "type": "园林"},
            {"name": "八达岭长城", "time": "6 小时", "price": 40, "area": "延庆", "type": "历史"},
            {"name": "天坛", "time": "3 小时", "price": 15, "area": "东城", "type": "历史"},
            {"name": "圆明园", "time": "3 小时", "price": 25, "area": "海淀", "type": "历史"},
            {"name": "南锣鼓巷", "time": "2 小时", "price": 0, "area": "东城", "type": "文化"},
            {"name": "798 艺术区", "time": "3 小时", "price": 0, "area": "朝阳", "type": "艺术"},
        ],
        "food_cost": 150,
        "hotel_cost": 300,
        "best_season": "春秋 (9-11 月，3-5 月)",
        "tips": ["提前预约故宫门票", "长城建议选八达岭或慕田峪", "雾霾天备口罩"]
    },
    "上海": {
        "attractions": [
            {"name": "外滩", "time": "2 小时", "price": 0, "area": "黄浦", "type": "地标"},
            {"name": "东方明珠", "time": "3 小时", "price": 220, "area": "浦东", "type": "地标"},
            {"name": "迪士尼", "time": "8 小时", "price": 400, "area": "浦东", "type": "乐园"},
            {"name": "豫园", "time": "2 小时", "price": 40, "area": "黄浦", "type": "园林"},
            {"name": "田子坊", "time": "2 小时", "price": 0, "area": "黄浦", "type": "文化"},
            {"name": "陆家嘴", "time": "3 小时", "price": 0, "area": "浦东", "type": "地标"},
            {"name": "南京路", "time": "2 小时", "price": 0, "area": "黄浦", "type": "购物"},
        ],
        "food_cost": 200,
        "hotel_cost": 400,
        "best_season": "春秋 (3-5 月，9-11 月)",
        "tips": ["迪士尼工作日人少", "外滩夜景更美", "地铁方便"]
    },
    "杭州": {
        "attractions": [
            {"name": "西湖", "time": "4 小时", "price": 0, "area": "西湖", "type": "自然"},
            {"name": "灵隐寺", "time": "3 小时", "price": 75, "area": "西湖", "type": "宗教"},
            {"name": "千岛湖", "time": "6 小时", "price": 180, "area": "淳安", "type": "自然"},
            {"name": "宋城", "time": "4 小时", "price": 320, "area": "西湖", "type": "文化"},
            {"name": "西溪湿地", "time": "3 小时", "price": 80, "area": "西湖", "type": "自然"},
            {"name": "龙井村", "time": "2 小时", "price": 0, "area": "西湖", "type": "文化"},
        ],
        "food_cost": 120,
        "hotel_cost": 250,
        "best_season": "春秋 (3-5 月，9-11 月)",
        "tips": ["西湖建议骑行", "龙井茶可品尝", "避开节假日"]
    },
    "成都": {
        "attractions": [
            {"name": "大熊猫基地", "time": "4 小时", "price": 58, "area": "成华", "type": "动物"},
            {"name": "宽窄巷子", "time": "2 小时", "price": 0, "area": "青羊", "type": "文化"},
            {"name": "锦里", "time": "2 小时", "price": 0, "area": "武侯", "type": "文化"},
            {"name": "都江堰", "time": "5 小时", "price": 80, "area": "都江堰", "type": "历史"},
            {"name": "青城山", "time": "6 小时", "price": 80, "area": "都江堰", "type": "自然"},
            {"name": "春熙路", "time": "2 小时", "price": 0, "area": "锦江", "type": "购物"},
        ],
        "food_cost": 100,
        "hotel_cost": 200,
        "best_season": "春秋 (3-6 月，9-11 月)",
        "tips": ["熊猫基地早点去", "火锅必吃", "茶馆体验慢生活"]
    },
    "西安": {
        "attractions": [
            {"name": "兵马俑", "time": "4 小时", "price": 120, "area": "临潼", "type": "历史"},
            {"name": "大雁塔", "time": "2 小时", "price": 50, "area": "雁塔", "type": "历史"},
            {"name": "古城墙", "time": "2 小时", "price": 54, "area": "碑林", "type": "历史"},
            {"name": "华清宫", "time": "3 小时", "price": 120, "area": "临潼", "type": "历史"},
            {"name": "回民街", "time": "2 小时", "price": 0, "area": "莲湖", "type": "美食"},
            {"name": "陕西历史博物馆", "time": "3 小时", "price": 0, "area": "雁塔", "type": "文化"},
        ],
        "food_cost": 80,
        "hotel_cost": 180,
        "best_season": "春秋 (3-5 月，9-11 月)",
        "tips": ["兵马俑请讲解", "肉夹馍必吃", "城墙可骑行"]
    },
    "三亚": {
        "attractions": [
            {"name": "亚龙湾", "time": "4 小时", "price": 0, "area": "吉阳", "type": "海滩"},
            {"name": "天涯海角", "time": "3 小时", "price": 81, "area": "天涯", "type": "地标"},
            {"name": "南山寺", "time": "4 小时", "price": 129, "area": "崖州", "type": "宗教"},
            {"name": "蜈支洲岛", "time": "6 小时", "price": 144, "area": "海棠", "type": "海岛"},
            {"name": "热带天堂森林公园", "time": "4 小时", "price": 175, "area": "吉阳", "type": "自然"},
        ],
        "food_cost": 150,
        "hotel_cost": 500,
        "best_season": "冬季 (10 月 - 次年 3 月)",
        "tips": ["防晒必备", "旺季提前订酒店", "海鲜注意价格"]
    },
    "厦门": {
        "attractions": [
            {"name": "鼓浪屿", "time": "6 小时", "price": 35, "area": "思明", "type": "海岛"},
            {"name": "厦门大学", "time": "2 小时", "price": 0, "area": "思明", "type": "文化"},
            {"name": "南普陀寺", "time": "2 小时", "price": 0, "area": "思明", "type": "宗教"},
            {"name": "环岛路", "time": "3 小时", "price": 0, "area": "思明", "type": "自然"},
            {"name": "曾厝垵", "time": "2 小时", "price": 0, "area": "思明", "type": "文化"},
        ],
        "food_cost": 100,
        "hotel_cost": 250,
        "best_season": "春秋 (3-5 月，9-11 月)",
        "tips": ["鼓浪屿船票提前买", "厦大需预约", "沙茶面必吃"]
    },
    "丽江": {
        "attractions": [
            {"name": "丽江古城", "time": "4 小时", "price": 50, "area": "古城", "type": "文化"},
            {"name": "玉龙雪山", "time": "6 小时", "price": 130, "area": "玉龙", "type": "自然"},
            {"name": "束河古镇", "time": "3 小时", "price": 40, "area": "古城", "type": "文化"},
            {"name": "泸沽湖", "time": "8 小时", "price": 100, "area": "宁蒗", "type": "自然"},
            {"name": "蓝月谷", "time": "3 小时", "price": 0, "area": "玉龙", "type": "自然"},
        ],
        "food_cost": 80,
        "hotel_cost": 200,
        "best_season": "春秋 (3-5 月，9-11 月)",
        "tips": ["注意高原反应", "古城石板路难走", "防晒保湿"]
    },
    "桂林": {
        "attractions": [
            {"name": "漓江", "time": "4 小时", "price": 210, "area": "阳朔", "type": "自然"},
            {"name": "象鼻山", "time": "2 小时", "price": 75, "area": "象山", "type": "自然"},
            {"name": "龙脊梯田", "time": "6 小时", "price": 100, "area": "龙胜", "type": "自然"},
            {"name": "阳朔西街", "time": "2 小时", "price": 0, "area": "阳朔", "type": "文化"},
            {"name": "遇龙河", "time": "3 小时", "price": 160, "area": "阳朔", "type": "自然"},
        ],
        "food_cost": 70,
        "hotel_cost": 150,
        "best_season": "春秋 (4-10 月)",
        "tips": ["漓江漂流必体验", "米粉必吃", "雨季带伞"]
    },
    "张家界": {
        "attractions": [
            {"name": "国家森林公园", "time": "8 小时", "price": 225, "area": "武陵源", "type": "自然"},
            {"name": "天门山", "time": "6 小时", "price": 258, "area": "永定", "type": "自然"},
            {"name": "大峡谷玻璃桥", "time": "4 小时", "price": 219, "area": "慈利", "type": "自然"},
            {"name": "黄龙洞", "time": "3 小时", "price": 100, "area": "武陵源", "type": "自然"},
        ],
        "food_cost": 60,
        "hotel_cost": 150,
        "best_season": "春秋 (3-5 月，9-11 月)",
        "tips": ["穿舒适鞋子", "带雨衣", "索道排队久"]
    },
    "九寨沟": {
        "attractions": [
            {"name": "九寨沟景区", "time": "8 小时", "price": 190, "area": "九寨沟", "type": "自然"},
            {"name": "黄龙", "time": "6 小时", "price": 170, "area": "松潘", "type": "自然"},
            {"name": "五花海", "time": "2 小时", "price": 0, "area": "九寨沟", "type": "自然"},
            {"name": "诺日朗瀑布", "time": "1 小时", "price": 0, "area": "九寨沟", "type": "自然"},
        ],
        "food_cost": 80,
        "hotel_cost": 200,
        "best_season": "秋季 (9-10 月)",
        "tips": ["高原反应注意", "温差大带外套", "秋季最美"]
    },
    "拉萨": {
        "attractions": [
            {"name": "布达拉宫", "time": "4 小时", "price": 200, "area": "城关", "type": "历史"},
            {"name": "大昭寺", "time": "2 小时", "price": 85, "area": "城关", "type": "宗教"},
            {"name": "纳木错", "time": "8 小时", "price": 120, "area": "当雄", "type": "自然"},
            {"name": "八廓街", "time": "2 小时", "price": 0, "area": "城关", "type": "文化"},
            {"name": "色拉寺", "time": "2 小时", "price": 50, "area": "城关", "type": "宗教"},
        ],
        "food_cost": 80,
        "hotel_cost": 200,
        "best_season": "夏季 (6-9 月)",
        "tips": ["高原反应严重", "防晒必备", "尊重宗教习俗"]
    }
}

# ============================================================================
# 🎯 旅行模板库（10+ 类型）
# ============================================================================
TRAVEL_TEMPLATES = {
    "情侣游": {
        "description": "浪漫双人之旅",
        "pace": "慢",
        "budget_factor": 1.2,
        "focus": ["浪漫景点", "美食体验", "拍照打卡"],
        "tips": ["预订景观房", "安排烛光晚餐", "准备惊喜"]
    },
    "亲子游": {
        "description": "带娃家庭之旅",
        "pace": "慢",
        "budget_factor": 1.5,
        "focus": ["乐园", "动物园", "互动体验"],
        "tips": ["带儿童用品", "行程宽松", "备常用药"]
    },
    "背包客": {
        "description": "经济穷游",
        "pace": "快",
        "budget_factor": 0.6,
        "focus": ["免费景点", "青旅", "当地体验"],
        "tips": ["住青旅", "公共交通", "自带干粮"]
    },
    "豪华游": {
        "description": "高端享受之旅",
        "pace": "慢",
        "budget_factor": 2.5,
        "focus": ["五星酒店", "私人导游", "高端餐饮"],
        "tips": ["提前预订", "VIP 通道", "专车接送"]
    },
    "摄影游": {
        "description": "拍照创作之旅",
        "pace": "慢",
        "budget_factor": 1.0,
        "focus": ["最佳拍摄点", "日出日落", "特色建筑"],
        "tips": ["带三脚架", "查天气", "黄金时段拍摄"]
    },
    "美食游": {
        "description": "吃货寻味之旅",
        "pace": "慢",
        "budget_factor": 1.3,
        "focus": ["特色餐厅", "小吃街", "美食体验"],
        "tips": ["做美食攻略", "留足胃口", "带消食片"]
    },
    "文化游": {
        "description": "历史人文之旅",
        "pace": "中",
        "budget_factor": 1.0,
        "focus": ["博物馆", "古迹", "文化体验"],
        "tips": ["请讲解", "提前做功课", "带笔记本"]
    },
    "冒险游": {
        "description": "刺激挑战之旅",
        "pace": "快",
        "budget_factor": 1.2,
        "focus": ["户外运动", "极限体验", "探险"],
        "tips": ["买保险", "带装备", "注意安全"]
    },
    "养生游": {
        "description": "休闲放松之旅",
        "pace": "很慢",
        "budget_factor": 1.5,
        "focus": ["温泉", "SPA", "自然景观"],
        "tips": ["行程宽松", "预订 spa", "带泳衣"]
    },
    "毕业旅行": {
        "description": "青春纪念之旅",
        "pace": "中",
        "budget_factor": 0.8,
        "focus": ["打卡景点", "集体活动", "性价比"],
        "tips": ["团购优惠", "多拍照", "注意安全"]
    }
}

# ============================================================================
# 🧳 打包清单模板
# ============================================================================
PACKING_LISTS = {
    "通用": [
        "身份证/护照", "手机+充电器", "钱包+银行卡", "换洗衣物", "洗漱用品",
        "常用药品", "雨伞", "水杯", "纸巾", "充电宝"
    ],
    "海边": [
        "防晒霜", "泳衣", "太阳镜", "沙滩鞋", "遮阳帽", "防水袋", "墨镜"
    ],
    "山区": [
        "登山鞋", "冲锋衣", "手电筒", "创可贴", "防蚊液", "保温杯"
    ],
    "冬季": [
        "羽绒服", "保暖内衣", "手套", "围巾", "帽子", "暖宝宝", "润唇膏"
    ],
    "夏季": [
        "短袖", "短裤", "凉鞋", "防晒霜", "藿香正气水", "小风扇"
    ],
    "商务": [
        "西装", "领带", "皮鞋", "笔记本电脑", "名片", "文件夹"
    ]
}

# ============================================================================
# 📊 预算计算器
# ============================================================================
def calculate_budget(destination, days, template="标准"):
    """详细预算计算"""
    if destination not in DESTINATIONS:
        return None
    
    dest = DESTINATIONS[destination]
    tmpl = TRAVEL_TEMPLATES.get(template, TRAVEL_TEMPLATES["标准"])
    factor = tmpl.get("budget_factor", 1.0)
    
    # 基础费用
    food = dest["food_cost"] * days * factor
    hotel = dest["hotel_cost"] * (days - 1) * factor
    
    # 门票（按每天 2 个景点计算）
    attractions = dest["attractions"][:days * 2]
    tickets = sum([a["price"] for a in attractions])
    
    # 交通
    transport = 100 * days  # 市内交通
    
    # 购物备用
    shopping = 500 * factor
    
    total = food + hotel + tickets + transport + shopping
    
    return {
        "餐饮": round(food),
        "住宿": round(hotel),
        "门票": round(tickets),
        "交通": round(transport),
        "购物": round(shopping),
        "总计": round(total),
        "人均": round(total / 2) if template in ["情侣游", "豪华游"] else round(total)
    }

# ============================================================================
# 📅 行程规划器
# ============================================================================
def plan_itinerary(destination, days, template="标准"):
    """智能行程规划"""
    if destination not in DESTINATIONS:
        return None
    
    dest = DESTINATIONS[destination]
    tmpl = TRAVEL_TEMPLATES.get(template, {})
    pace = tmpl.get("pace", "中")
    focus = tmpl.get("focus", [])
    
    # 根据节奏调整每天景点数
    attractions_per_day = {"慢": 1, "中": 2, "快": 3}.get(pace, 2)
    
    itinerary = []
    used_attractions = set()
    
    for day in range(1, days + 1):
        day_plan = {"day": day, "attractions": [], "meals": [], "notes": ""}
        
        # 选择景点
        available = [a for a in dest["attractions"] if a["name"] not in used_attractions]
        selected = available[:attractions_per_day]
        
        for attr in selected:
            day_plan["attractions"].append(attr)
            used_attractions.add(attr["name"])
        
        # 添加用餐建议
        day_plan["meals"] = [
            f"早餐：酒店附近",
            f"午餐：{selected[0]['area'] if selected else '景区'}附近",
            f"晚餐：{selected[-1]['area'] if selected else '市区'}特色餐厅"
        ]
        
        itinerary.append(day_plan)
    
    return itinerary

# ============================================================================
# 🧳 生成打包清单
# ============================================================================
def generate_packing_list(destination, season="通用", special=None):
    """生成个性化打包清单"""
    base_items = PACKING_LISTS["通用"].copy()
    
    # 添加季节物品
    if season in PACKING_LISTS:
        base_items.extend(PACKING_LISTS[season])
    
    # 添加特殊需求
    if special == "摄影":
        base_items.extend(["相机", "三脚架", "备用电池", "存储卡"])
    elif special == "商务":
        base_items.extend(["笔记本电脑", "名片", "正装"])
    elif special == "海边":
        base_items.extend(PACKING_LISTS["海边"])
    
    return list(set(base_items))  # 去重

# ============================================================================
# 💬 格式化输出
# ============================================================================
def format_itinerary(itinerary, destination, budget, template="标准"):
    """格式化行程输出"""
    tmpl = TRAVEL_TEMPLATES.get(template, {})
    response = f"✈️ **{destination} {len(itinerary)}日游** ({tmpl.get('description', '标准版')})\n\n"
    
    for day_plan in itinerary:
        response += f"📅 **Day {day_plan['day']}**\n"
        if day_plan['attractions']:
            for attr in day_plan['attractions']:
                response += f"  - {attr['name']} ({attr['time']}, ¥{attr['price']}, {attr['type']})\n"
        else:
            response += "  - 自由活动时间\n"
        
        response += f"  🍽️ 用餐：{', '.join(day_plan['meals'])}\n\n"
    
    if budget:
        response += "💰 **预算明细**（元）\n"
        response += f"  - 餐饮：¥{budget['餐饮']}\n"
        response += f"  - 住宿：¥{budget['住宿']}\n"
        response += f"  - 门票：¥{budget['门票']}\n"
        response += f"  - 交通：¥{budget['交通']}\n"
        response += f"  - 购物：¥{budget['购物']}\n"
        response += f"  - **总计：¥{budget['总计']}**"
        if budget.get('人均'):
            response += f"（人均 ¥{budget['人均']}）\n"
    
    return response

def format_packing_list(items, title="打包清单"):
    """格式化打包清单"""
    response = f"🧳 **{title}**\n\n"
    for i, item in enumerate(items, 1):
        response += f"□ {item}\n"
    response += f"\n共 {len(items)} 项物品"
    return response

def format_tips(destination):
    """显示旅行贴士"""
    if destination not in DESTINATIONS:
        return ""
    
    dest = DESTINATIONS[destination]
    response = f"💡 **{destination} 旅行贴士**\n\n"
    response += f"🌤️ 最佳季节：{dest['best_season']}\n\n"
    response += "⚠️ 注意事项：\n"
    for tip in dest.get("tips", []):
        response += f"- {tip}\n"
    return response

# ============================================================================
# 🎯 主函数
# ============================================================================
def main(query):
    """主函数 - 支持多种命令"""
    query_lower = query.lower()
    
    # 检测目的地
    for dest in DESTINATIONS.keys():
        if dest in query:
            # 检测天数
            days_match = re.search(r'(\d+) 天', query)
            days = int(days_match.group(1)) if days_match else 3
            
            # 检测旅行模板
            template = "标准"
            for tmpl in TRAVEL_TEMPLATES.keys():
                if tmpl in query:
                    template = tmpl
                    break
            
            # 生成行程
            itinerary = plan_itinerary(dest, days, template)
            budget = calculate_budget(dest, days, template)
            
            response = format_itinerary(itinerary, dest, budget, template)
            
            # 如果询问打包清单
            if "打包" in query or "行李" in query:
                season = "通用"
                if any(s in query for s in ["夏", "热"]): season = "夏季"
                elif any(s in query for s in ["冬", "冷"]): season = "冬季"
                elif any(s in query for s in ["海", " beach"]): season = "海边"
                
                packing = generate_packing_list(dest, season)
                response += "\n\n" + format_packing_list(packing, f"{dest} 打包清单")
            
            # 如果询问贴士
            if "贴士" in query or "注意" in query or "攻略" in query:
                response += "\n\n" + format_tips(dest)
            
            return response
    
    # 显示所有目的地
    if "哪里" in query or "推荐" in query:
        response = "🌍 **推荐目的地**\n\n"
        for dest, info in DESTINATIONS.items():
            response += f"- **{dest}**: {info['best_season']} | 日均¥{info['food_cost']+info['hotel_cost']}\n"
        return response
    
    # 显示模板
    if "模板" in query or "类型" in query:
        response = "🎯 **旅行模板**\n\n"
        for name, tmpl in TRAVEL_TEMPLATES.items():
            response += f"- **{name}**: {tmpl['description']} (预算 x{tmpl['budget_factor']})\n"
        return response
    
    # 默认回复
    return """✈️ 旅行规划助手 v2.0

**功能**：
1. 行程规划 - "帮我规划 3 天的北京旅行"
2. 模板选择 - "情侣游去三亚 5 天"、"亲子游去上海"
3. 预算估算 - "去成都玩 5 天要多少钱"
4. 打包清单 - "去海边要带什么"
5. 旅行贴士 - "去拉萨注意事项"

**支持目的地**：北京、上海、杭州、成都、西安、三亚、厦门、丽江、桂林、张家界、九寨沟、拉萨

**旅行模板**：情侣游、亲子游、背包客、豪华游、摄影游、美食游、文化游、冒险游、养生游、毕业旅行

告诉我你想去哪里玩？👻"""

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(main("帮我规划 3 天的北京旅行，情侣游"))
