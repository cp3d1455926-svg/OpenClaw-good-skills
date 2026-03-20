#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Horoscope - 星座运势
每日/每周运势查询、星座配对、幸运数字
"""

import random
from datetime import datetime
from typing import Dict, List

# 星座日期范围
ZODIAC_DATES = {
    '白羊座': ((3, 21), (4, 19)),
    '金牛座': ((4, 20), (5, 20)),
    '双子座': ((5, 21), (6, 21)),
    '巨蟹座': ((6, 22), (7, 22)),
    '狮子座': ((7, 23), (8, 22)),
    '处女座': ((8, 23), (9, 22)),
    '天秤座': ((9, 23), (10, 23)),
    '天蝎座': ((10, 24), (11, 22)),
    '射手座': ((11, 23), (12, 21)),
    '摩羯座': ((12, 22), (1, 19)),
    '水瓶座': ((1, 20), (2, 18)),
    '双鱼座': ((2, 19), (3, 20))
}

# 运势类型
FORTUNE_TYPES = ['overall', 'love', 'career', 'health', 'money']

# 运势描述模板
FORTUNE_TEMPLATES = {
    'overall': {
        'good': ['今天运势极佳，诸事顺利！', '能量满满，把握机会！', '好运连连，心情美丽！'],
        'medium': ['运势平稳，按部就班就好。', '不好不坏的一天，保持平常心。', '平平淡淡才是真。'],
        'bad': ['运势稍低，谨慎行事。', '可能会遇到小挫折，加油！', '注意休息，不要太拼。']
    },
    'love': {
        'good': ['桃花运旺盛，单身者有机会邂逅！', '感情甜蜜，适合约会表白！', '魅力四射，异性缘佳！'],
        'medium': ['感情平稳，多沟通会更好。', '适合维系现有关系。', '爱情需要耐心经营。'],
        'bad': ['感情易有波折，避免争吵。', '单身者不宜急于求成。', '给彼此一些空间。']
    },
    'career': {
        'good': ['事业运上升，易获领导赏识！', '工作效率高，适合推进项目！', '有贵人相助，把握机会！'],
        'medium': ['工作平稳，完成分内事即可。', '适合学习和积累。', '按部就班，不要急躁。'],
        'bad': ['工作压力大，注意调节。', '易遇小人，谨言慎行。', '不宜做重大决策。']
    },
    'health': {
        'good': ['精力充沛，适合运动！', '身体状况良好，保持作息！', '气色不错，心情愉悦！'],
        'medium': ['身体状况一般，注意休息。', '适当运动，增强体质。', '饮食清淡些更好。'],
        'bad': ['容易疲劳，多休息。', '注意保暖，预防感冒。', '身体发出警报，要重视！']
    },
    'money': {
        'good': ['财运亨通，有意外之财！', '适合投资理财！', '收入增加，钱包鼓鼓！'],
        'medium': ['财运平稳，收支平衡。', '不宜大额消费。', '理性消费，做好规划。'],
        'bad': ['财运不佳，避免冲动消费。', '小心破财，看好钱包。', '投资需谨慎！']
    }
}


def get_zodiac(month: int, day: int) -> str:
    """根据出生日期获取星座"""
    for zodiac, ((start_month, start_day), (end_month, end_day)) in ZODIAC_DATES.items():
        if (month == start_month and day >= start_day) or \
           (month == end_month and day <= end_day):
            return zodiac
    return '未知'


def get_lucky_numbers() -> List[int]:
    """生成幸运数字"""
    return random.sample(range(1, 50), 6)


def get_lucky_color() -> str:
    """生成幸运颜色"""
    colors = ['红色', '蓝色', '绿色', '黄色', '紫色', '粉色', '黑色', '白色', '金色', '银色']
    return random.choice(colors)


def get_fortune(zodiac: str, fortune_type: str = 'overall') -> str:
    """获取运势"""
    # 根据日期和星座生成固定的运势（同一天同一星座运势相同）
    today = datetime.now().strftime('%Y-%m-%d')
    seed = hash(f"{today}-{zodiac}-{fortune_type}")
    random.seed(seed)
    
    # 随机选择运势等级
    level = random.choice(['good', 'medium', 'bad'])
    
    # 获取运势描述
    templates = FORTUNE_TEMPLATES.get(fortune_type, FORTUNE_TEMPLATES['overall'])
    fortunes = templates.get(level, templates['medium'])
    
    return random.choice(fortunes)


def get_today_fortune(zodiac: str) -> Dict:
    """获取今日完整运势"""
    return {
        'zodiac': zodiac,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'overall': get_fortune(zodiac, 'overall'),
        'love': get_fortune(zodiac, 'love'),
        'career': get_fortune(zodiac, 'career'),
        'health': get_fortune(zodiac, 'health'),
        'money': get_fortune(zodiac, 'money'),
        'lucky_numbers': get_lucky_numbers(),
        'lucky_color': get_lucky_color(),
        'rating': random.randint(1, 5)
    }


def get_compatibility(zodiac1: str, zodiac2: str) -> Dict:
    """获取星座配对"""
    # 简单的配对算法（实际应该有更详细的配对表）
    seed = hash(f"{zodiac1}-{zodiac2}")
    random.seed(seed)
    
    score = random.randint(60, 100)
    
    if score >= 90:
        comment = '天作之合，非常匹配！'
    elif score >= 80:
        comment = '很不错的组合！'
    elif score >= 70:
        comment = '需要互相理解和包容。'
    else:
        comment = '需要更多努力经营。'
    
    return {
        'zodiac1': zodiac1,
        'zodiac2': zodiac2,
        'score': score,
        'comment': comment
    }


def run(command: str = '', args: List[str] = None) -> str:
    """主入口"""
    args = args or []
    
    if command == 'today' or command == '今日':
        if not args:
            return "❌ 请提供星座，如：今日 白羊座"
        
        zodiac = args[0]
        if zodiac not in ZODIAC_DATES.keys():
            return f"❌ 未知星座 '{zodiac}'\n可用：{', '.join(ZODIAC_DATES.keys())}"
        
        fortune = get_today_fortune(zodiac)
        
        return f"""
🔮 {zodiac} · 今日运势
📅 {fortune['date']}

综合运势：{'⭐' * fortune['rating']}

💕 爱情：{fortune['love']}
💼 事业：{fortune['career']}
💪 健康：{fortune['health']}
💰 财运：{fortune['money']}

🍀 幸运数字：{', '.join(map(str, fortune['lucky_numbers']))}
🎨 幸运颜色：{fortune['lucky_color']}
        """.strip()
    
    elif command == 'zodiac' or command == '查星座':
        if len(args) < 2:
            return "❌ 用法：zodiac [月] [日]\n例如：zodiac 3 21"
        
        try:
            month = int(args[0])
            day = int(args[1])
            zodiac = get_zodiac(month, day)
            
            return f"📅 {month}月{day}日 是 ♈ {zodiac}"
        except ValueError:
            return "❌ 月份和日期必须是数字"
    
    elif command == 'love' or command == '配对':
        if len(args) < 2:
            return "❌ 用法：love [星座 1] [星座 2]\n例如：love 白羊座 天秤座"
        
        zodiac1 = args[0]
        zodiac2 = args[1]
        
        if zodiac1 not in ZODIAC_DATES.keys():
            return f"❌ 未知星座 '{zodiac1}'"
        if zodiac2 not in ZODIAC_DATES.keys():
            return f"❌ 未知星座 '{zodiac2}'"
        
        result = get_compatibility(zodiac1, zodiac2)
        
        return f"""
💕 星座配对

{result['zodiac1']} ♓ {result['zodiac2']}

匹配度：{result['score']}%
{result['comment']}
        """.strip()
    
    elif command == 'list' or command == '列表':
        zodiacs = list(ZODIAC_DATES.keys())
        
        lines = ["♈ 十二星座列表:"]
        for i, z in enumerate(zodiacs, 1):
            dates = ZODIAC_DATES[z]
            lines.append(f"{i:2d}. {z} ({dates[0][0]}.{dates[0][1]:02d} - {dates[1][0]}.{dates[1][1]:02d})")
        
        return '\n'.join(lines)
    
    elif command == 'help' or command == '帮助':
        return """
🔮 Horoscope - 星座运势

可用命令:
  today/今日 [星座]           - 今日运势
  zodiac/查星座 [月] [日]      - 查询星座
  love/配对 [星座 1] [星座 2]   - 星座配对
  list/列表                  - 十二星座列表
  help/帮助                  - 显示帮助

示例:
  今日运势：today 白羊座
  查星座：zodiac 3 21
  配对：love 白羊座 天秤座
  
十二星座:
白羊座 (3.21-4.19) | 金牛座 (4.20-5.20)
双子座 (5.21-6.21) | 巨蟹座 (6.22-7.22)
狮子座 (7.23-8.22) | 处女座 (8.23-9.22)
天秤座 (9.23-10.23)| 天蝎座 (10.24-11.22)
射手座 (11.23-12.21)| 摩羯座 (12.22-1.19)
水瓶座 (1.20-2.18) | 双鱼座 (2.19-3.20)
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
